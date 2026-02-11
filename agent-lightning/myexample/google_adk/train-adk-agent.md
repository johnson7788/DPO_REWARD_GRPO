# 使用 Agent-lightning 和 VERL 训练 ADK Agent

本教程仅保留使 ADK 驱动的 agent 对 Agent-lightning 训练器可见并启动 VERL 训练所需的步骤。要获取端到端参考实现，请在跟随本教程的同时打开 [`examples/google_adk`](../examples/google_adk)。

## 1. 先决条件

- 安装包含 ADK 封装器和 VERL 运行器的依赖项：

  ```bash
  pip install "agentlightning[verl,adk]" "google-adk>=0.3.0"
  ```

- 在 `examples/google_adk/data` 下准备两个 Parquet 文件：`train.parquet` 和 `test.parquet`。运行 `uv run python prepare_dataset.py --download --outdir examples/google_adk` 来拉取我们在 SQL 教程中重用的 Spider 数据集，或者通过 `--train` / `--test` 提供你自己的 JSON/CSV。
- 导出将支持 ADK agent 的 OpenAI 兼容端点（原生 OpenAI、Azure 或本地 vLLM 代理）：

  ```bash
  export OPENAI_API_BASE=http://localhost:8000/v1
  export OPENAI_API_KEY=<redacted>
  export OPENAI_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
  export HF_TOKEN=<VERL 用于下载权重的令牌>
  ```

## 2. 封装 ADK agent

[`examples/google_adk/adk_agent.py`]({{ src("examples/google_adk/adk_agent.py") }}) 定义了 `LitAdkAgent`，这是 [`agl.LitAgent`][agentlightning.LitAgent] 的一个简单子类。其职责包括：

- 拉取 VERL 注入到每个 rollout 中的 `"main_llm"` 资源。
- 使用该 LLM 端点构建 ADK 编排器（Agent + Orchestrator 或任何自定义逻辑）。
- 在回答任务时通过 ADK 的追踪钩子自动发出跨度。
- 从 `rollout(...)` 返回标量奖励。返回值时**不要**调用 [`emit_reward`][agentlightning.emit_reward]。

由于 `LitAdkAgent` 已经实现，你只需要验证 ADK 端的计划/执行逻辑是否从提供的 `agl.LLM` 中查找基础 URL 和凭证。这就是使 agent "对训练器可用" 的关键——不需要额外的注册层。

## 3. 向训练器提供资源

使 ADK agent 在训练期间可用的关键是向训练器提供初始的 `"main_llm"` 资源并将其指向 `LitAdkAgent`。下面的代码片段与 `train_adk.py` 所做的匹配：

```python
import agentlightning as agl
from examples.google_adk.adk_agent import LitAdkAgent

verl_config = {
    "algorithm": {"adv_estimator": "grpo"},
    "data": {"train_batch_size": 32, "max_prompt_length": 4096, "max_response_length": 2048},
    "actor_rollout_ref": {
        "rollout": {"name": "vllm", "n": 4, "multi_turn": {"format": "hermes"}},
        "actor": {"ppo_mini_batch_size": 32, "optim": {"lr": 1e-6}},
        "model": {"path": "meta-llama/Meta-Llama-3-8B-Instruct"},
    },
    "trainer": {"n_gpus_per_node": 1, "val_before_train": True, "test_freq": 32, "save_freq": 64},
}

trainer = agl.Trainer(
    n_runners=10,
    algorithm=agl.VERL(verl_config),
    adapter={"agent_match": "LitAdkAgent"},
    initial_resources={
        "main_llm": agl.LLM(
            endpoint=os.environ["OPENAI_API_BASE"],
            model=os.environ["OPENAI_MODEL"],
            api_key=os.environ["OPENAI_API_KEY"],
            sampling_parameters={"temperature": 0.0},
        )
    },
)

agent = LitAdkAgent()
train_data = pd.read_parquet("data/train.parquet").to_dict("records")
val_data = pd.read_parquet("data/test.parquet").to_dict("records")
trainer.fit(agent, train_dataset=train_data, val_dataset=val_data)
```

关键要点：

- 一旦你将 agent 传递给 `trainer.fit(...)`，它就对 VERL 可见。
- `"main_llm"` 键是一个约定——在训练器配置和 agent 的 rollout 之间保持一致使用。
- `adapter.agent_match` 过滤跨度，以便 VERL 只消费 ADK agent 的追踪。

## 4. 启动打包脚本

上面所有的连接已经捆绑在 [`examples/google_adk/train_adk.py`]({{ src("examples/google_adk/train_adk.py") }}) 内部。从示例目录中运行：

```bash
python train_adk.py \
  --train-file data/train.parquet \
  --val-file data/test.parquet \
  --model ${OPENAI_MODEL:-meta-llama/Meta-Llama-3-8B-Instruct} \
  --endpoint ${OPENAI_API_BASE:-http://localhost:8000/v1}
```

有用的标志：

- `--ci` 或 `--ci-fast` 来减少运行器数量 + 数据集切片。
- 如果你需要 W&B 日志记录，可以使用 `--wandb-project` / `--wandb-run-name`。
- `--external-store-address` 连接到现有的 LightningStore（在运行之间重用追踪）。

使用 `python adk_debug.py --file data/test.parquet` 进行快速试运行，在不启动 VERL 的情况下测试 agent。

## 5. 示例训练结果

一个代表性的 CI-fast 运行（1 个运行器，通过 `prepare_dataset.py --download` 下载的 Spider 衍生数据集，单个 A100-40GB 上的 vLLM 后端）产生了：

| 步骤 | 平均奖励 | 备注 |
| ---- | -------- | ---- |
| 0    | 0.08     | 更新前的随机 rollout |
| 32   | 0.31     | GRPO 更新后的首次验证通过 |
| 64   | 0.47     | 检查点已保存 (`ckpt-00064`) |
| 96   | 0.52     | 平台期；跨度显示稳定的 ADK 编排 |

你的数值会因模型选择和数据集而异，但看到验证奖励超过随机基线并看到跨度流入 LightningStore 确认了 ADK agent 已正确连接到 Agent-lightning 的训练堆栈。