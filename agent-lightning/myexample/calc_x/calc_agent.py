# Copyright (c) Microsoft. All rights reserved.

"""此示例代码演示了如何使用最新的 Agent-lightning API (v0.2+) 定义一个可训练的 Calc-X 智能体。"""

import asyncio
import os
import re
from typing import TypedDict, cast
import dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from agentlightning import AgentOpsTracer, LightningStoreClient
from eval_utils import evaluate

import agentlightning as agl
dotenv.load_dotenv()

class MathProblem(TypedDict):
    """此 TypedDict 定义了每个训练样本的结构。

    你的任务结构应该包含以下所有信息：

    - 智能体处理任务所需的信息 (例如，'question')
    - 评估所需的信息 (例如，'result' 用于真实答案)

    此类型是可选的。不是使示例工作所必需的。
    """

    # 字段来自数据集
    id: str
    question: str  # 智能体需要解决的数学问题
    chain: str  # 逐步解决方案（训练中未使用）
    result: str  # 用于评估的真实答案
    source: str


def autogen_assistant_agent(
    model: str, openai_base_url: str, temperature: float, workbench: McpWorkbench
) -> AssistantAgent:
    model_client = OpenAIChatCompletionClient(
        model=model,
        base_url=openai_base_url,
        api_key=os.environ.get("OPENAI_API_KEY", "token-abc123"),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": ModelFamily.UNKNOWN,
            "structured_output": False,
        },
        temperature=temperature,
    )

    calc_agent = AssistantAgent(
        name="calc",
        model_client=model_client,
        workbench=workbench,
        reflect_on_tool_use=True,
    )
    return calc_agent


@agl.rollout
async def calc_agent(task: MathProblem, llm: agl.LLM) -> None:
    """Calc-X 智能体 rollout 函数。

    它接收一个数学问题和一个大语言模型端点资源。
    预期返回 None，并通过 `agl.emit_reward` 发出奖励。
    也可以直接返回奖励而不使用 `agl.emit_reward`。
    您可以选择其中一种方式，但不能同时使用两种。
    """

    calculator_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-calculator"])

    async with McpWorkbench(calculator_mcp_server) as workbench:
        calc_agent = autogen_assistant_agent(
            llm.model,
            llm.endpoint,
            llm.sampling_parameters.get("temperature", 0.7),
            workbench,
        )
        try:
            output_format = "准备好时输出答案。答案应由三个井号(`###`)包围，格式为 ### ANSWER: <answer> ###。"
            prompt = task["question"] + " " + output_format
            # 有时 MCP 工具可能会超时。在这种情况下，整个智能体会被阻塞。
            # 因此我们设置 5 分钟的超时时间，以防止智能体无限期阻塞。
            result = await asyncio.wait_for(calc_agent.run(task=prompt), timeout=300.0)
            # 评估
            last_message = cast(str, result.messages[-1].content)  # type: ignore
            answer = re.search(r"###\s*ANSWER:\s*(.+?)(\s*###|$)", last_message)
            if answer:
                answer = answer.group(1)
            else:
                answer = last_message
        except asyncio.TimeoutError as e:
            print("发生超时。错误:", str(e))
            answer = "None"
        except Exception as e:
            print("失败:", str(e))
            answer = "None"
        reward = await evaluate(answer, str(task["result"]))
        agl.emit_reward(reward)  # 发出奖励用于追踪
        print("答案: {} 真实值: {} 奖励: {}".format(answer, task["result"], reward))


async def debug():
    """这里我们展示了一种更手动的调试方式，不使用训练器。

    我们自己获取数据样本，并使用 LitAgentRunner 运行智能体。
    您需要设置 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL` 环境变量
    才能运行此函数。
    """
    # 手动创建一个追踪器，因为 Runner 需要它。
    # 如果您除了奖励之外不需要追踪任何内容，请使用虚拟的 OtelTracer。
    tracer = agl.OtelTracer()
    # 运行器处理 MathProblem，这与智能体的任务类型匹配。
    runner = agl.LitAgentRunner[MathProblem](tracer)

    # 此处需要一个存储来保存收集的数据。
    # store = agl.InMemoryLightningStore()
    store = LightningStoreClient("http://localhost:45993")

    # 这是需要调优的部分（即大语言模型）
    resource = agl.LLM(
        endpoint=os.environ["OPENAI_BASE_URL"], model=os.environ["OPENAI_MODEL"], sampling_parameters={"temperature": 1.0}
    )

    made_up_task: MathProblem = {
        "id": "debug-1",
        "question": "What is 12 multiplied by 15?",
        "chain": "",
        "result": "180",
        "source": "debug",
    }

    another_made_up_task: MathProblem = {
        "id": "debug-2",
        "question": "What is the square root of 256?",
        "chain": "",
        "result": "16",
        "source": "debug",
    }

    # 此处的智能体必须与实际运行中使用的智能体相同。
    with runner.run_context(agent=calc_agent, store=store):
        await runner.step(
            made_up_task,
            resources={
                # 此处的键 "main_llm" 可以是任意的
                "main_llm": resource
            },
        )

        # 运行另一个任务
        await runner.step(
            another_made_up_task,
            resources={"main_llm": resource},
        )


if __name__ == "__main__":
    asyncio.run(debug())
