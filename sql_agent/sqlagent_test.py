#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : rag_test.py
# @Desc  : 真实运行 Agent 的测试脚本 (使用 DeepSeek API)
import time
import traceback
import asyncio
import os
import sys
import dotenv
# 导入真实依赖
from agentlightning import LLM
from agentlightning.types import Rollout, AttemptedRollout, Attempt
from sql_agent import SQLSearchAgent
dotenv.load_dotenv()
# ================= DeepSeek 配置区域 =================
# 1. DeepSeek 官方 API 地址
# REAL_LLM_ENDPOINT = "https://api.deepseek.com/v1"

# 1. 本地 vLLM API 地址 (对应 start_vllm.sh 中的端口)
REAL_LLM_ENDPOINT = "http://117.50.163.230:8400/v1"
# 2. 模型名称 (对应 start_vllm.sh 中的 --served-model-name)
# REAL_MODEL_NAME = "local_agent_model"

REAL_MODEL_NAME = "local_agent_model"
MODEL_PREFIX="openai/"

# 3. API KEY 设置
# 建议在系统环境变量中设置: export DEEPSEEK_API_KEY='sk-xxxx'
# 或者为了测试方便，你可以在这里临时填入字符串，但不要提交到代码仓库
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "xxx")
print(f"DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY}")

# ====================================================

async def main():
    print("====== 开始 RAGAgent 真实环境测试 ======")

    # 1. 初始化 Agent
    # RAGAgent 内部已经写死了 MCP URL (http://127.0.0.1:8099/sse)
    # 请确保 mcp_search.py 已经运行在 8099 端口
    agent = SQLSearchAgent()

    # 2. 准备真实资源 (Resources)
    # 我们构造一个指向 DeepSeek 的 LLM 对象
    llm_resource = LLM(
        model=REAL_MODEL_NAME,
        endpoint=REAL_LLM_ENDPOINT,
        api_key=DEEPSEEK_API_KEY,
        # DeepSeek 有时需要显式指定为 openai 兼容模式，
        # 但 agentlightning/litellm 通常能通过 endpoint 自动识别
    )

    resources = {
        "main_llm": llm_resource
    }
    print(f"LLM 资源配置完成: {REAL_MODEL_NAME} @ DeepSeek API")

    # 3. 定义测试任务
    # DeepSeek 的指令遵循能力很强
    task = {
        "question": "药品开胸顺气丸的可以用来治什么？",
        "answer": "xxx"
    }

    rollout_id = "deepseek_run_001"

    # 4. 构造 Rollout 对象
    # Rollout 需要 rollout_id, input, start_time
    # AttemptedRollout 还需要 attempt
    attempt = Attempt(
        rollout_id=rollout_id,
        attempt_id=f"{rollout_id}_attempt_1",
        sequence_id=1,
        start_time=time.time(),
    )
    rollout = AttemptedRollout(
        rollout_id=rollout_id,
        input=task,
        start_time=time.time(),
        attempt=attempt,
    )

    print(f"\n>>> 正在提问: {task['question']}")
    print(">>> 等待 DeepSeek 思考与工具调用 (请观察 ToolLoggingHooks 输出)...\n")

    try:
        # 5. 执行真实的 Rollout
        # 注意：rag_agent.py 中使用了 "hosted_vllm/" 前缀，
        # LiteLLM 通常会将 hosted_vllm 视为 OpenAI 兼容接口，
        # 参数顺序：task, resources, rollout
        reward = await agent.training_rollout_async(task, resources, rollout)

        print("\n====== 测试执行完成 ======")
        print(f"最终奖励得分 (Reward): {reward}")

    except Exception as e:
        print(f"\n[错误] 运行过程中发生异常: {e}")
        # 打印更详细的错误栈，方便调试 API 连接问题
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())