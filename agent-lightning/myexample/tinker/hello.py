# Copyright (c) Microsoft. All rights reserved.

"""使用 Agent-lightning 和 Tinker 进行训练的最小示例。

Hello agent 微调模型，使其重复您传入的任何身份字符串
（例如，`"Say you are 42" -> "I'm 42."`）。它镜像了 Tinker Cookbook RL recipes 的结构，
但通过 Agent-lightning 任务而不是 Tinker 内置环境来驱动 rollout。

环境设置：

1. 将 `examples/tinker/.env.example` 复制到 `examples/tinker/.env`。
2. 填写 `OPENAI_API_KEY` / `OPENAI_BASE_URL`，以便通过 LiteLLM 路由助手补全。
3. 如果计划针对托管的 Tinker 服务进行训练，请提供 `TINKER_API_KEY`。

此示例不支持 W&B 日志记录。

CLI 入口点：

```bash
# 集成运行，启动 store、algorithm 和 runners
python hello.py oneclick
```

跨三个终端的分布式工作流：

```bash
agl store  # <-- 期望 store 在端口 45993 上运行
python hello.py algo
python hello.py runner
```
"""

from __future__ import annotations

import argparse
import asyncio
import multiprocessing
import socket

from agl_tinker.algo import Tinker
from agl_tinker.env import AGLDatasetBuilder
from agl_tinker.train import Config
from agl_tinker.train import main as entrypoint
from openai import OpenAI
from rich.console import Console

import agentlightning as agl

console = Console()


def _find_available_port() -> int:
    """通过绑定到端口 0 来查找可用端口。

    Returns:
        可用的端口号。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@agl.rollout
def hello(task: str, llm: agl.LLM, rollout: agl.Rollout) -> None:
    """测试模型是否声明给定身份的 Agent rollout 函数。

    提示模型说出它是给定的任务/身份，并根据模型响应是否符合预期行为分配奖励。

    Args:
        task: 模型应该声明的身份字符串。
        llm: LLM 端点配置。
        rollout: 包含 rollout ID 和模式的 rollout 元数据。
    """
    openai_client = OpenAI(base_url=llm.endpoint, api_key="dummy")
    response = openai_client.chat.completions.create(
        model=llm.model,
        messages=[{"role": "user", "content": f"Let's play a game. Say you are {task}."}],
    )

    response_content = response.choices[0].message.content
    content_lower = response_content.lower() if response_content else ""
    if ("i am " + task) in content_lower or ("i'm " + task) in content_lower:
        rew = 1.0
    elif ("not " + task) in content_lower:
        rew = -1.0
    else:
        rew = 0.0

    console.print(
        f"[bold green]Runners ({rollout.rollout_id}, {rollout.mode}):[/bold green] "
        f"{task} -> {response_content} -> Reward: {rew}"
    )
    agl.emit_reward(rew)


def run_algo():
    """在独立模式下运行训练算法。

    启动连接到单独存储和 rollout runners 的 Tinker 训练算法。
    """
    config = Config(
        learning_rate=1e-5,
        dataset_builder=AGLDatasetBuilder(
            train_dataset=[str(i) for i in range(1000)],
            val_dataset=[str(i) for i in range(1000, 1024)],
            batch_size=32,
            shuffle=True,
            group_size=4,
            seed=42,
        ),
        renderer_name="qwen3_instruct",
        model_name="/data/server/models/Qwen3-0.6B",
        log_path="logs/hello",
        max_tokens=32,
        store_address="http://localhost:45993",
    )
    asyncio.run(entrypoint(config))


def run_rollout(*, worker_id: int) -> None:
    """Rollout runner，单进程。"""
    tracer = agl.AgentOpsTracer()

    runner = agl.LitAgentRunner[str](tracer=tracer)

    console.print(f"[bold green]Runners:[/bold green] Rollout runner {worker_id} started.")

    store = agl.LightningStoreClient("http://localhost:45993")
    with runner.run_context(agent=hello, store=store, worker_id=worker_id):
        asyncio.run(runner.iter())


def spawn_runners(*, n_runners: int) -> None:
    """在不同进程中生成一组 rollout runners。

    Args:
        n_runners: 要生成的 runners 数量。
    """

    runners = [
        multiprocessing.Process(target=run_rollout, kwargs={"worker_id": worker_id}) for worker_id in range(n_runners)
    ]
    for runner in runners:
        runner.start()

    for runner in runners:
        runner.join()


def oneclick(ci: bool = False):
    """在单个进程中运行集成训练，包括 algorithm 和 runners。

    这是运行示例的最简单方法，因为它会自动处理生成
    store、algorithm 和 runners。

    Args:
        ci: 是否在 CI 模式下运行。快速验证。
    """
    if ci:
        # 使用较小的批次大小和组大小以加快验证速度。
        batch_size = 4
        group_size = 2
    else:
        batch_size = 16
        group_size = 4

    config = Config(
        learning_rate=1e-5,
        dataset_builder=AGLDatasetBuilder(
            batch_size=batch_size,
            group_size=group_size,
            seed=42,
            n_epochs=1,
        ),
        renderer_name="qwen3_instruct",
        model_name="/data/server/models/Qwen3-0.6B",
        log_path="logs/hello",
        max_tokens=32,
        llm_proxy_port=_find_available_port(),
    )
    trainer = agl.Trainer(
        algorithm=Tinker(config),
        llm_proxy=agl.LLMProxy(
            port=12306,
            num_retries=3,
            # 必须在此处使用线程模式，否则 Tinker 采样客户端将挂起。
            launch_mode="thread",
        ),
        n_runners=8,
        port=_find_available_port(),
    )

    if ci:
        # 为了更快地验证，使用较小的数据集。
        train_dataset = [str(i) for i in range(16)]
        val_dataset = [str(i) for i in range(100, 108)]
    else:
        train_dataset = [str(i) for i in range(1000)]
        val_dataset = [str(i) for i in range(1000, 1024)]
    trainer.fit(hello, train_dataset=train_dataset, val_dataset=val_dataset)


def main():
    """hello 示例脚本的入口点。"""
    parser = argparse.ArgumentParser(description="使用 Agent-lightning + Tinker 训练一个 hello echo agent。")
    parser.add_argument("mode", type=str, choices=["algo", "runner", "oneclick"])
    parser.add_argument("--ci", action="store_true", help="在 CI 模式下运行。快速验证。")

    args = parser.parse_args()

    if args.ci:
        if args.mode != "oneclick":
            raise ValueError("CI 模式仅支持 oneclick 模式。")

    agl.setup_logging()
    if args.mode == "algo":
        run_algo()
    elif args.mode == "runner":
        spawn_runners(n_runners=8)
    elif args.mode == "oneclick":
        oneclick(ci=args.ci)


if __name__ == "__main__":
    main()