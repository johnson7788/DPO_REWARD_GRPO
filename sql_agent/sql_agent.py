from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import math
import httpx
from typing import Any, Dict, List, Optional, cast

import dotenv
from litellm import completion, acompletion

from agentlightning import (
    LLM,
    LitAgent,
    NamedResources,
    Trainer,
    setup_logging,
)
from agentlightning.types import Rollout, AttemptedRollout
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
from agents.model_settings import ModelSettings
from agents.lifecycle import RunHooks

from tools import query_database_by_sql

# 外部奖励模型 API 配置
REWARD_MODEL_URL = os.getenv("REWARD_MODEL_URL", "http://117.50.48.176:8400/score")

dotenv.load_dotenv()
setup_logging()

# ============================================================================
# 基础配置
# ============================================================================
MAX_COMPLETION_TOKENS = 768  # Qwen2.5-7B-Instruct 上下文充足，max_response_length 需 >= 此值
TEACHER_API_KEY = os.getenv("TEACHER_API_KEY")
TEACHER_MODEL = os.getenv("TEACHER_MODEL")
TEACHER_BASE_URL = os.getenv("TEACHER_BASE_URL")

if not TEACHER_MODEL.startswith("openai/"):
    TEACHER_MODEL = "openai/deepseek-chat"

# ============================================================================
# 日志：写到本地文件
# ============================================================================

log_file = "sql_agent_training.log"

logger = logging.getLogger("sql_agent_training")
logger.setLevel(logging.INFO)

if not logger.handlers:
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    # 同时在控制台打印
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)


# ============================================================================
# Reward 计算
# ============================================================================

# 搜索 Agent 的系统 Prompt
sql_agent_prompt = """
按需使用sql进行query_database_by_sql执行查询，然后回答用户的问题。
表结构如下:
# drugs_info药品表
[
    'id', 'med_name', 'med_name_initial', 'med_barcode', 'med_approval',
    'component', 'form', 'dosage', 'indication', 'adverse_reactions',
    'contraindications', 'precautions', 'company_name', 'description',
    'mechanism_action', 'cate_name', 'drug_interactions', 'storage',
    'pack', 'period', 'approve_code', 'status', 'created_at'
]

# disease疾病表
[
    'id', 'disease_name', 'overview', 'clinical_manif', 'complication',
    'epidemiology', 'examination', 'treatment', 'cause', 'diagnosis',
    'differ_diag', 'prevention', 'prognosis','create_at', 'update_at'
]
"""

# ============================================================================
# Reward 计算：规则评估 + 大模型评估
# ============================================================================
async def compute_sql_agent_reward(question: str, answer: str, tool_calls: List[Dict[str, Any]], enable_rule_based: bool = True,
                             enable_llm_based: bool = True) -> float:
    """
    计算 SQL Agent 的综合奖励分数

    奖励来源：
    1. 规则评估：正确执行 SQL 查询给少量分数 (0.1)
    2. 大模型评估：基于问题和回答质量评估 (0.0 - 0.9)
    """
    total_reward = 0.0

    # 1. 规则评估：检查是否执行了 SQL
    if enable_rule_based:
        for tool_call in tool_calls:
            if tool_call.get("name") == "query_database_by_sql":
                executed_sql = tool_call.get("args", {}).get("sql", "")
                if executed_sql:
                    total_reward += 0.1  # 只要执行了 SQL 就给 0.1 分
                    logger.info(f"[规则奖励]发现执行了SQL: {executed_sql}")
                break

    # 2. 大模型评估：评估回答质量
    if enable_llm_based:
        try:
            # 可以使用不同的奖励模型
            llm_reward = await SQLTeacher.score_by_reward_model(question, answer)
            # llm_reward = await SQLTeacher.score_sql_answer(question, answer)
            total_reward += llm_reward
            logger.info(f"[LLM奖励] 回答质量奖励: {llm_reward:.3f}")
        except Exception as e:
            logger.error(f"[LLM奖励错误] LLM调用失败: {e}")
            total_reward += 0.5  # 失败时给默认分数

    return total_reward


class SQLTeacher:
    """DeepSeek 负责对 SQL Agent 的回答进行评估"""

    @staticmethod
    async def score_sql_answer(question: str, final_answer: str) -> float:
        """DeepSeek 打分：仅根据问题和回答质量进行评估"""
        prompt = f"""你是一个严格的"医学问答质量评估专家"。请对以下SQL Agent的回答进行评分 (0.0 - 1.0)。

用户问题: {question}
助手最终回答: {final_answer}

评分标准：
1. 准确性: 回答内容是否准确、无幻觉
2. 完整性: 是否完整回答了用户的问题
3. 清晰性: 回答是否条理清晰、易于理解
4. 专业性: 医学表述是否专业、规范

请输出一个浮点数分数（0.0-1.0），不要解释。

分数:"""
        try:
            resp = await acompletion(
                model=TEACHER_MODEL,
                messages=[{"role": "user", "content": prompt}],
                api_key=TEACHER_API_KEY,
                base_url=TEACHER_BASE_URL,
                temperature=0.0,
                max_tokens=16,
            )
            content = resp.choices[0].message.content.strip()
            m = re.search(r"(\d+(\.\d+)?)", content)
            if not m:
                return 0.5
            score = float(m.group(1))
            score = max(0.0, min(1.0, score))
            return score
        except Exception as e:
            logger.error(f"[Teacher Error] score_sql_answer failed: {e}")
            return 0.5

    @staticmethod
    async def score_by_reward_model(question: str, answer: str) -> float:
        """调用外部奖励模型 API 进行评分"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    REWARD_MODEL_URL,
                    json={"prompt": question, "response": answer},
                    headers={"Content-Type": "application/json"}
                )
                resp.raise_for_status()
                result = resp.json()
                score = result.get("score", 0.5)
                logger.info(f"[外部奖励模型] 评分: {score}")
                return float(score)
        except Exception as e:
            logger.error(f"[外部奖励模型 Error] 调用失败: {e}")
            return 0.5


# ============================================================================
# Hook & State Management
# ============================================================================

class NavHooks(RunHooks[Any]):
    def __init__(self):
        self.tool_calls = []

    async def on_tool_end(self, context, agent, tool, result: str):
        try:
            args = json.loads(context.tool_arguments)
        except:
            args = {"raw": context.tool_arguments}
        self.tool_calls.append({
            "name": getattr(tool, "name", "unknown"),
            "args": args,
            "result": {"raw_result": result}
        })


# ============================================================================
# Agent Implementation
# ============================================================================

class SQLSearchAgent(LitAgent[Any]):
    def __init__(self, trained_agents=None):
        super().__init__(trained_agents=trained_agents)

    async def training_rollout_async(
        self,
        task: Dict[str, Any],
        resources: NamedResources,
        rollout: Rollout,
    ) -> float | None:
        llm = cast(LLM, resources.get("main_llm"))
        rollout = cast(AttemptedRollout, rollout)
        base_url = llm.get_base_url(rollout.rollout_id, rollout.attempt.attempt_id)

        question = task.get("question", "")
        # Tools
        tools = [query_database_by_sql]

        logger.info(f"--- Q: {question} ---")

        # 拼接 Prompt
        hooks = NavHooks()
        agent = Agent(
            model=LitellmModel(model="hosted_vllm/" + llm.model, base_url=base_url, api_key=llm.api_key),
            model_settings=ModelSettings(max_tokens=MAX_COMPLETION_TOKENS, temperature=0.7, max_completion_tokens=MAX_COMPLETION_TOKENS),
            name="sql_agent",
            instructions=sql_agent_prompt,
            tools=tools
        )

        max_retries = 3
        answer = None
        for attempt in range(max_retries):
            try:
                res = await Runner.run(agent, question, max_turns=2, hooks=hooks)
                answer = res.final_output
                break
            except Exception as e:
                logger.warning(f"Run failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))
                    hooks = NavHooks()  # 重置 hooks 避免状态污染

        if not answer:
            logger.warning(f"Agent 重试 {max_retries} 次后仍失败，跳过此 rollout: {question}")
            return None
        
        # 计算奖励
        reward = await compute_sql_agent_reward(question, answer, hooks.tool_calls)
        logger.info(f"问题: {question}的答案\n{answer}对应的轮次奖励: {reward}")
        logger.info(
            f"Stop multi-turn: reward={reward:.3f}, "
        )
        return float(reward)

    async def validation_rollout_async(
        self,
        task: Dict[str, Any],
        resources: NamedResources,
        rollout: Rollout,
    ) -> float | None:
        """验证 rollout 使用与训练相同的逻辑。"""
        llm = cast(LLM, resources.get("main_llm"))
        rollout = cast(AttemptedRollout, rollout)

        # 设置 temperature
        val_resources: NamedResources = {
            "main_llm": LLM(
                endpoint=llm.get_base_url(rollout.rollout_id, rollout.attempt.attempt_id),
                model=llm.model,
                sampling_parameters={"temperature": 0.7},
            )
        }

        return await self.training_rollout_async(task, val_resources, rollout)


if __name__ == "__main__":
    Trainer(n_workers=12).fit_v0(SQLSearchAgent(), "http://localhost:9999/")