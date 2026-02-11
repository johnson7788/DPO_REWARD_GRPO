# Copyright (c) Microsoft. All rights reserved.

"""使用VERL算法训练Calc-X智能体的辅助脚本。

使用示例：

```bash
python train_calc_agent.py --train-file data/train.parquet --val-file data/test.parquet --llm-proxy
```

要使用外部存储，请先运行存储服务器：

```bash
agl store --port 45993
```

然后使用外部存储地址运行训练脚本：

```bash
AGL_MANAGED_STORE=0 python train_calc_agent.py --external-store-address http://localhost:45993
```

或者，如果需要，您也可以分别运行算法和执行器：

```bash
AGL_MANAGED_STORE=0 AGL_CURRENT_ROLE=algorithm python train_calc_agent.py --external-store-address http://117.133.60.219:45993
AGL_MANAGED_STORE=0 AGL_CURRENT_ROLE=runner python train_calc_agent.py --external-store-address http://117.133.60.219:45993
```
Qwen/Qwen2.5-0.5B-Instruct
Qwen/Qwen3-0.5B
Qwen/Qwen3-4B
"""

import argparse
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, cast

from calc_agent import MathProblem, calc_agent
from datasets import Dataset as HuggingFaceDataset

import agentlightning as agl
from agentlightning.env_var import LightningEnvVar, resolve_bool_env_var, resolve_str_env_var


def verl_default_config() -> Dict[str, Any]:
    config = {
        "algorithm": {
            "adv_estimator": "grpo",
            "use_kl_in_reward": False,
        },
        "data": {
            "train_batch_size": 32,
            "max_prompt_length": 4096,
            "max_response_length": 2048,
        },
        "actor_rollout_ref": {
            "rollout": {
                "tensor_model_parallel_size": 1,
                "n": 6,
                "log_prob_micro_batch_size_per_gpu": 4,
                "multi_turn": {"format": "hermes"},
                "name": "vllm",
                "gpu_memory_utilization": 0.6,
                "engine_kwargs": {
                    "vllm": {
                        "enable_auto_tool_choice": True,
                        "tool_call_parser": "hermes",
                    }
                },
            },
            "actor": {
                "ppo_mini_batch_size": 32,
                "ppo_micro_batch_size_per_gpu": 4,
                "optim": {"lr": 1e-6},
                "use_kl_loss": True,
                "kl_loss_coef": 0.01,
                "entropy_coeff": 0,
                "clip_ratio_low": 0.2,
                "clip_ratio_high": 0.3,
                "fsdp_config": {
                    "param_offload": True,
                    "optimizer_offload": True,
                },
            },
            "ref": {
                "log_prob_micro_batch_size_per_gpu": 8,
                "fsdp_config": {"param_offload": True},
            },
            "model": {
                "path": "Qwen/Qwen3-4B",
                "use_remove_padding": True,
                "enable_gradient_checkpointing": True,
            },
        },
        "trainer": {
            "n_gpus_per_node": 1,
            "val_before_train": True,
            "critic_warmup": 0,
            "logger": ["console", "wandb"],
            "project_name": "AgentLightning",
            "experiment_name": "calc_x",
            "nnodes": 1,
            "save_freq": 64,
            "test_freq": 32,
            "total_epochs": 2,
        },
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
    external_store_address: str,
):
    """使用VERL算法训练Calc-X智能体的入口函数。

    参数:
        train_file: 训练数据parquet文件的路径。
        val_file: 验证数据parquet文件的路径。
        model: HF模型ID或路径，用于覆盖默认模型。
        llm_proxy: 是否启用LLM代理跟踪/适配器。
        ci: 是否运行最小化的CI风格训练循环。
        n_runners: 训练器的执行器数量。
        ci_fast: 是否将训练循环限制为单步（隐含CI开关）。
        external_store_address: 连接到外部存储而不是在内存中创建新存储。
    """
    # Load datasets (respect CLI file paths)
    train_dataset = cast(agl.Dataset[MathProblem], HuggingFaceDataset.from_parquet(train_file).to_list())  # type: ignore
    val_dataset = cast(agl.Dataset[MathProblem], HuggingFaceDataset.from_parquet(val_file).to_list())  # type: ignore

    print("First 5 rows of train dataset:")
    print(train_dataset[:5])  # type: ignore
    print("First 5 rows of val dataset:")
    print(val_dataset[:5])  # type: ignore

    config = verl_default_config()

    if model:
        config["actor_rollout_ref"]["model"]["path"] = model

    # CI toggle keeps everything else the same but you can tweak the lightweight bits here if desired
    if ci or ci_fast:
        # Config the experiment name and project name so that they are available to CI
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = uuid.uuid4().hex[:8]
        EXPERIMENT_NAME = f"calc_x_{timestamp}_{random_suffix}"

        PROJECT_NAME = "AgentLightningCI"

        # Skip this step if AGL_CURRENT_ROLE is runner
        agl_current_role = resolve_str_env_var(LightningEnvVar.AGL_CURRENT_ROLE)

        if agl_current_role != "runner":
            # Simulate writing to $GITHUB_OUTPUT if it’s set
            github_output = os.getenv("GITHUB_OUTPUT")
            if github_output:
                with open(github_output, "a") as f:
                    f.write(f"project_name={PROJECT_NAME}\n")
                    f.write(f"run_name={EXPERIMENT_NAME}\n")

            print("Set environment variables:")
            print(f"PROJECT_NAME={PROJECT_NAME}")
            print(f"EXPERIMENT_NAME={EXPERIMENT_NAME}")

        # Keep it tiny/light without adding new knobs
        config["actor_rollout_ref"]["rollout"]["gpu_memory_utilization"] = 0.8
        config["trainer"]["total_epochs"] = 1
        config["trainer"]["total_training_steps"] = 20
        config["trainer"]["test_freq"] = 20
        config["trainer"]["experiment_name"] = EXPERIMENT_NAME
        config["trainer"]["project_name"] = PROJECT_NAME
        config["trainer"].pop("save_freq", None)

        if ci_fast:
            # Extra fast CI toggle for testing purposes.
            config["actor_rollout_ref"]["rollout"]["gpu_memory_utilization"] = 0.8
            config["trainer"]["total_training_steps"] = 1
            config["trainer"]["test_freq"] = 1

    algorithm = agl.VERL(config)

    if external_store_address:
        store: Optional[agl.LightningStore] = agl.LightningStoreClient(external_store_address)
    else:
        store = None

    if llm_proxy:
        tracer = agl.OtelTracer()  # dummy tracer for LLM Proxy
        adapter = agl.LlmProxyTraceToTriplet()
        trainer = agl.Trainer(algorithm=algorithm, n_runners=n_runners, store=store, tracer=tracer, adapter=adapter)
    else:
        trainer = agl.Trainer(algorithm=algorithm, n_runners=n_runners, store=store)

    trainer.fit(calc_agent, train_dataset, val_dataset=val_dataset)


def main():
    parser = argparse.ArgumentParser(description="使用Agent-lightning + VERL训练数学计算智能体。")
    parser.add_argument("--train-file", type=str, default="data/train.parquet", help="训练数据parquet文件的路径")
    parser.add_argument("--val-file", type=str, default="data/test.parquet", help="验证数据parquet文件的路径")
    parser.add_argument("--model", type=str, default=None, help="HF模型ID或路径（可选）")
    parser.add_argument("--llm-proxy", action="store_true", help="启用LLM代理跟踪/适配器")
    parser.add_argument("--ci", action="store_true", help="运行最小化的CI风格训练循环")
    parser.add_argument(
        "--ci-fast", action="store_true", help="将训练循环限制为单步（隐含--ci）"
    )
    parser.add_argument("--n-runners", type=int, default=10, help="训练器的执行器数量")
    parser.add_argument(
        "--external-store-address",
        type=str,
        default="",
        help="连接到外部存储而不是在内存中创建新存储",
    )
    parser.add_argument("--debug", action="store_true", help="启用调试日志")

    args = parser.parse_args()

    if args.external_store_address:
        print(f"Connecting to external store at: {args.external_store_address}")
        if resolve_bool_env_var(LightningEnvVar.AGL_MANAGED_STORE, fallback=True):
            raise ValueError(
                "When using an external store, please set the environment variable AGL_MANAGED_STORE=0. "
                "Otherwise the trainer will still try to manage the store lifecycle for you!"
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
        external_store_address=args.external_store_address,
    )


if __name__ == "__main__":
    main()
