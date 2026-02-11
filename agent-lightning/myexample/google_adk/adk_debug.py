# Copyright (c) Microsoft. All rights reserved.

from __future__ import annotations

import argparse
import os
from typing import Any, Dict, cast

import pandas as pd
from rich.console import Console

from agentlightning import LLM, configure_logger

from adk_agent import AdkTask, LitAdkAgent

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ADK代理健全性检查（单次运行，无训练）。")
    parser.add_argument("--file", type=str, default="data/test.parquet", help="Parquet文件路径。")
    parser.add_argument("--index", type=int, default=0, help="作为单个任务运行的行索引。")
    parser.add_argument(
        "--endpoint",
        type=str,
        default=os.environ.get("OPENAI_API_BASE", "http://localhost:8000/v1"),
        help="OpenAI兼容的基础URL。",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.environ.get("OPENAI_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct"),
        help="用于rollout的模型名称。",
    )
    return parser.parse_args()


def main() -> None:
    configure_logger()
    args = parse_args()

    if not os.path.exists(args.file):
        console.print(f"[red]未找到数据集文件：[/red] {args.file}")
        raise SystemExit(1)

    df = pd.read_parquet(args.file)
    if df.empty:
        console.print("[red]数据集文件为空。[/red]")
        raise SystemExit(1)

    row_idx = max(0, min(args.index, len(df) - 1))
    task: AdkTask = cast(AdkTask, df.iloc[row_idx].to_dict())

    resources: Dict[str, Any] = {
        "main_llm": LLM(endpoint=args.endpoint, model=args.model, sampling_parameters={"temperature": 0.0})
    }

    agent = LitAdkAgent()
    # Rollout的最小存根（通常由runner提供）
    class _R:
        pass

    reward = agent.rollout(task, resources, cast(Any, _R()))
    console.print(f"[bold]健全性检查奖励：[/bold] {reward}")


if __name__ == "__main__":
    main()