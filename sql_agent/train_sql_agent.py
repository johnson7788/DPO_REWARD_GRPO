#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SQL Agent 训练脚本，使用 VERL 算法。

使用示例：

```bash
python train_sql_agent.py --train-file data/train.parquet --val-file data/val.parquet
```

使用外部存储时，先启动存储服务：

```bash
agl store --port 9999
```

然后使用外部存储地址运行训练脚本：

```bash
AGL_MANAGED_STORE=0 python train_sql_agent.py --external-store-address http://localhost:9999
```

也可以分别运行算法和 runner：

```bash
AGL_MANAGED_STORE=0 AGL_CURRENT_ROLE=algorithm python train_sql_agent.py --external-store-address http://localhost:9999
AGL_MANAGED_STORE=0 AGL_CURRENT_ROLE=runner python train_sql_agent.py --external-store-address http://localhost:9999
```
"""

import argparse
import os
import dotenv
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, cast

from sql_agent import SQLSearchAgent
from tools import query_database_by_sql
from datasets import Dataset as HuggingFaceDataset

import agentlightning as agl
from agentlightning.env_var import LightningEnvVar, resolve_bool_env_var, resolve_str_env_var
dotenv.load_dotenv()

def verl_default_config() -> Dict[str, Any]:
    config = {
        "algorithm": {
            "adv_estimator": "grpo",
            "use_kl_in_reward": False,
        },
        "data": {
            "train_batch_size": 2,
            "max_prompt_length": 2048,
            "max_response_length": 768,
        },
        "actor_rollout_ref": {
            "rollout": {
                "tensor_model_parallel_size": 1,
                "ulysses_sequence_parallel_size": 1,
                "n": 4,
                "log_prob_micro_batch_size_per_gpu": 1,
                "multi_turn": {"format": "hermes", "max_turns": 2},
                "name": "vllm",
                "gpu_memory_utilization": 0.35,
                "engine_kwargs": {
                    "vllm": {
                        "enable_auto_tool_choice": True,
                        "tool_call_parser": "hermes",
                    }
                },
            },
            "actor": {
                "ppo_mini_batch_size": 2,
                "ppo_micro_batch_size_per_gpu": 1,
                "optim": {"lr": 1e-6},
                "use_kl_loss": False,
                "kl_loss_coef": 0.0,
                "entropy_coeff": 0,
                "clip_ratio_low": 0.2,
                "clip_ratio_high": 0.3,
                "fsdp_config": {
                    "param_offload": True,
                    "optimizer_offload": True,
                },
            },
            "ref": {
                "log_prob_micro_batch_size_per_gpu": 1,
                "fsdp_config": {"param_offload": True},
            },
            "model": {
                "path": "Qwen/Qwen3-0.6B-Instruct",
                "use_remove_padding": False,
                "enable_gradient_checkpointing": True,
            },
        },
        "trainer": {
            "n_gpus_per_node": 1,  # 修改为你的 GPU 数量
            "val_before_train": True,
            "critic_warmup": 0,
            "logger": ["console", "wandb"],
            "project_name": "AgentLightning",
            "experiment_name": "sql_agent",
            "nnodes": 1,
            "save_freq": 20,
            "test_freq": 20,
            "total_epochs": 2,
        },
        "checkpoint": {
            "enable": True,  # 启用检查点功能
            "max_num_checkpoints": 2,  # 最多保留 2 个检查点
        }
    }
    return config


def train(
    *,
    train_file: str,
    val_file: str,
    model: Optional[str],
    llm_proxy: bool,
    ci: bool,
    ci_fast: bool,
    n_runners: int,
    n_gpus: int,
    external_store_address: str,
    trajectory_level: bool = False,
    weave: bool,
    mongo_uri: Optional[str],
    resume_checkpoint: Optional[str] = None,
):
    """SQL Agent 训练入口函数，使用 VERL 算法。

    参数:
        train_file: 训练数据集的 parquet 文件路径。
        val_file: 验证数据集的 parquet 文件路径。
        model: HuggingFace 模型 ID 或本地路径，用于覆盖默认模型。
        llm_proxy: 是否启用 LLM Proxy 追踪/适配器。
        ci: 是否运行最小化的 CI 风格训练循环。
        n_runners: Trainer 的 runner 数量。
        ci_fast: 是否将训练循环限制为单步执行（隐含 --ci）。
        external_store_address: 连接外部存储而非创建内存存储。
        trajectory_level: 是否在 trace aggregator 中启用轨迹级别。
        weave: 是否启用 Weave 追踪。
        mongo_uri: 用于存储的 MongoDB URI。
    """
    # 加载数据集（遵循 CLI 文件路径）
    train_dataset = cast(agl.Dataset[Dict[str, Any]], HuggingFaceDataset.from_parquet(train_file).to_list())  # type: ignore
    val_dataset = cast(agl.Dataset[Dict[str, Any]], HuggingFaceDataset.from_parquet(val_file).to_list())  # type: ignore

    print("训练数据集前 5 行：")
    print(train_dataset[:5])  # type: ignore
    print("验证数据集前 5 行：")
    print(val_dataset[:5])  # type: ignore

    config = verl_default_config()

    # 使用命令行参数覆盖默认 GPU 配置
    if n_gpus > 1:
        config["trainer"]["n_gpus_per_node"] = n_gpus
        # 调整 batch size 以适应多卡训练
        # 并行模型设置
        config["actor_rollout_ref"]["rollout"]["tensor_model_parallel_size"] = n_gpus
        config["actor_rollout_ref"]["rollout"]["ulysses_sequence_parallel_size"] = n_gpus

        # 固定微批次
        config["actor_rollout_ref"]["rollout"]["log_prob_micro_batch_size_per_gpu"] = 1
        config["actor_rollout_ref"]["actor"]["ppo_micro_batch_size_per_gpu"] = 1
        config["actor_rollout_ref"]["ref"]["log_prob_micro_batch_size_per_gpu"] = 1

        # CPU Offload on FSDP
        config["actor_rollout_ref"]["actor"]["fsdp_config"]["param_offload"] = True
        config["actor_rollout_ref"]["actor"]["fsdp_config"]["optimizer_offload"] = True

        # 可选：按 GPU 数线性扩增全局 batch
        config["data"]["train_batch_size"] = 1 * n_gpus

        print(f"启用多卡训练: {n_gpus} GPUs, tensor_model_parallel_size={n_gpus}, ulysses_sequence_parallel_size={n_gpus}")
        print(f"Train batch per step = {config['data']['train_batch_size']}, micro-batch per GPU = 1")

    if model:
        config["actor_rollout_ref"]["model"]["path"] = model

    if resume_checkpoint is not None:
        if resume_checkpoint == "latest":
            print("🔁 从最近一次 checkpoint 恢复训练")
            config["trainer"]["load_checkpoint"] = True
        else:
            print(f"🔁 从指定 checkpoint 恢复训练: {resume_checkpoint}")
            config["trainer"]["load_checkpoint"] = resume_checkpoint

    if trajectory_level:
        config["agentlightning"] = {
            "trace_aggregator": {
                "level": "trajectory",
                "trajectory_max_prompt_length": 2048,
                "trajectory_max_response_length": 8192,
            }
        }
        print("已在 trace aggregator 中启用轨迹级别。")

    # CI 开关保持其他设置不变，但可以调整轻量级参数
    if ci or ci_fast:
        # 配置实验名称和项目名称，以便 CI 使用
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = uuid.uuid4().hex[:8]
        EXPERIMENT_NAME = f"sql_agent_{timestamp}_{random_suffix}"

        PROJECT_NAME = "AgentLightningCI"

        # 如果 AGL_CURRENT_ROLE 是 runner 则跳过此步骤
        agl_current_role = resolve_str_env_var(LightningEnvVar.AGL_CURRENT_ROLE)

        if agl_current_role != "runner":
            # 模拟写入 $GITHUB_OUTPUT（如果设置了的话）
            github_output = os.getenv("GITHUB_OUTPUT")
            if github_output:
                with open(github_output, "a") as f:
                    f.write(f"project_name={PROJECT_NAME}\n")
                    f.write(f"run_name={EXPERIMENT_NAME}\n")

            print("设置环境变量：")
            print(f"PROJECT_NAME={PROJECT_NAME}")
            print(f"EXPERIMENT_NAME={EXPERIMENT_NAME}")

        # 保持轻量级，不添加新参数
        config["actor_rollout_ref"]["rollout"]["gpu_memory_utilization"] = 0.3
        config["trainer"]["total_epochs"] = 1
        config["trainer"]["total_training_steps"] = 20
        config["trainer"]["test_freq"] = 20
        config["trainer"]["experiment_name"] = EXPERIMENT_NAME
        config["trainer"]["project_name"] = PROJECT_NAME
        config["trainer"].pop("save_freq", None)

        if ci_fast:
            # 用于测试的超快 CI 开关
            config["actor_rollout_ref"]["rollout"]["gpu_memory_utilization"] = 0.3
            config["trainer"]["total_training_steps"] = 1
            config["trainer"]["test_freq"] = 1

    algorithm = agl.VERL(config)

    if external_store_address:
        store: Optional[agl.LightningStore] = agl.LightningStoreClient(external_store_address)
    elif mongo_uri:
        from agentlightning.store.mongo import MongoLightningStore

        store = MongoLightningStore(mongo_uri=mongo_uri)
    else:
        store = None

    if llm_proxy:
        tracer = agl.OtelTracer()  # LLM Proxy 的虚拟 tracer
        adapter = agl.LlmProxyTraceToTriplet()
        trainer = agl.Trainer(algorithm=algorithm, n_runners=n_runners, store=store, tracer=tracer, adapter=adapter)
    elif weave:
        # 应始终延迟/按条件导入（在功能标志后面），以避免在未显式启用 weave 时干扰
        # 其他库（如 LiteLLM/OpenTelemetry）。
        from agentlightning.tracer.weave import WeaveTracer

        tracer = WeaveTracer()
        trainer = agl.Trainer(algorithm=algorithm, n_runners=n_runners, store=store, tracer=tracer)
    else:
        print(f"不进行训练，因为没有开启 --llm-proxy 或 --weave 选项。")
        trainer = agl.Trainer(algorithm=algorithm, n_runners=n_runners, store=store)

    trainer.fit(SQLSearchAgent(), train_dataset, val_dataset=val_dataset)


def main():
    # 设置 CUDA 内存配置，避免碎片化导致 OOM
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

    parser = argparse.ArgumentParser(description="使用 Agent-lightning + VERL 训练 SQL Agent。")
    parser.add_argument("--train-file", type=str, default="data/train.parquet", help="训练数据集的 parquet 文件路径")
    parser.add_argument("--val-file", type=str, default="data/val.parquet", help="验证数据集的 parquet 文件路径")
    parser.add_argument("--model", type=str, default=None, help="HuggingFace 模型 ID 或本地路径（可选）")
    parser.add_argument("--llm-proxy", action="store_true", help="启用 LLM Proxy 追踪/适配器")
    parser.add_argument("--weave", action="store_true", help="启用 Weave 追踪")
    parser.add_argument("--ci", action="store_true", help="运行最小化的 CI 风格训练循环")
    parser.add_argument(
        "--ci-fast", action="store_true", help="将训练循环限制为单步执行（隐含 --ci）"
    )
    parser.add_argument("--n-runners", type=int, default=4, help="Trainer 的 runner worker数量")
    parser.add_argument("--n-gpus", type=int, default=1, help="每个节点的 GPU 数量")
    parser.add_argument(
        "--external-store-address",
        type=str,
        default="",
        help="连接外部存储而非创建内存存储",
    )
    parser.add_argument("--debug", action="store_true", help="启用调试日志")
    parser.add_argument(
        "--trajectory-level",
        action="store_true",
        help="在 trace aggregator 中启用轨迹级别。",
    )
    parser.add_argument(
        "--mongo-uri",
        type=str,
        default=None,
        help="用于存储的 MongoDB URI。",
    )
    parser.add_argument(
        "--resume_checkpoint",
        type=str,
        default=None,
        nargs="?",
        const="latest",
        help=(
            "从 checkpoint 恢复训练。"
            "不传值表示从最近一次 checkpoint 恢复，"
            "传路径表示从指定 checkpoint 恢复。"
        ),
    )

    args = parser.parse_args()

    if args.external_store_address:
        print(f"正在连接到外部存储：{args.external_store_address}")
        if resolve_bool_env_var(LightningEnvVar.AGL_MANAGED_STORE, fallback=True):
            raise ValueError(
                "使用外部存储时，请设置环境变量 AGL_MANAGED_STORE=0。"
                "否则 Trainer 仍会尝试管理存储的生命周期！"
            )

    if args.ci_fast:
        args.ci = True

    agl.setup_logging("DEBUG" if args.debug else "INFO")

    train(
        train_file=args.train_file,
        val_file=args.val_file,
        model=args.model,
        llm_proxy=args.llm_proxy,
        ci=args.ci,
        ci_fast=args.ci_fast,
        n_runners=args.n_runners,
        n_gpus=args.n_gpus,
        external_store_address=args.external_store_address,
        trajectory_level=args.trajectory_level,
        weave=args.weave,
        mongo_uri=args.mongo_uri,
        resume_checkpoint=args.resume_checkpoint
    )


if __name__ == "__main__":
    main()
