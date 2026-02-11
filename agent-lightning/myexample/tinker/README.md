# Tinker + Agent-lightning 集成

本示例展示了如何使用 [Tinker 的强化学习基础设施](https://tinker-docs.thinkingmachines.ai/) 作为 Agent-lightning 编写代理的微调后端。您可以按照部署代理的方式编写代理，而桥接代码会从 Agent-lightning 跟踪中重建与 Tinker 兼容的轨迹。

**注意：该示例经过测试且兼容 Agent-lightning v0.2.x 版本，但由于运行 Tinker 训练服务的成本原因，尚未在 CI 中维护。**

## 这与原始 Tinker Cookbook RL 配方的不同之处

现实世界的代理应用会在熟悉的框架（CrewAI、LangChain、AutoGen、OpenAI Agents 等）中编排逻辑，或通过调用 OpenAI 兼容的 REST API。一个简单的数字猜测代理可能看起来像这样：

```python
def guess_number_agent():
    client = openai.OpenAI()
    messages = [{"role": "user", "content": "猜一个 1 到 100 之间的数字。"}]
    for _ in range(MAX_TURNS):
        response = client.chat.completions.create(model="gpt-4.1", messages=messages)
        response_content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_content})
        guessed_number = extract_number(response_content)
        if guessed_number == gold_answer:
            return 1.0
        elif guessed_number < gold_answer:
            messages.append({"role": "user", "content": "太小了"})
        else:
            messages.append({"role": "user", "content": "太大了"})
    return 0.0
```

然而，参考的 [Tinker Cookbook 示例](https://github.com/thinking-machines-lab/tinker-cookbook/tree/51d9e8226f2dcf82ceac272c734a5f6e3b4f0203/tinker_cookbook/recipes/multiplayer_rl/guess_number) 期望您将相同的逻辑重写为回调风格的 `Env`，并创建一个简单的循环在语言模型 (`TokenCompleter`) 和 `Env` 之间迭代。

```python
class GuessNumberEnv:
    def __init__(self, gold_answer: int):
        self.system_prompt: Message = {"role": "system", "content": SYSTEM_PROMPT}
        self.turns: list[Message] = []
        self.gold_answer: int = gold_answer

    async def initial_observation(self) -> list[int]:
        return message_to_tokens(self.system_prompt)

    async def step(self, action_tokens: list[int]) -> tuple[list[int], float, bool]:
        action_message = tokens_to_message(action_tokens)
        guessed_number = extract_number(action_message["content"])

        if guessed_number == self.gold_answer:
            text, reward = "正确", 1.0
        elif guessed_number < self.gold_answer:
            text, reward = "太小", 0.0
        else:
            text, reward = "太大", 0.0

        self.turns.append(action_message)
        self.turns.append({"role": "assistant", "content": text})
        episode_done = reward == 1 or len(self.turns) // 2 >= MAX_TURNS
        return message_to_tokens(self.turns), reward, episode_done
```

随着代理变得更加复杂，以回调风格编写变得越来越痛苦。每当需要 LLM 调用时，您必须中断控制流，这会使代码碎片化并难以维护。

Agent-lightning 隐藏了这一转换步骤：您可以保持第一种风格进行开发和生产，而框架会将任务排队到存储中，从跨度重建轨迹，并将它们提供给训练循环。此示例展示了如何使 Tinker 的原始训练循环与 Agent-lightning 协同工作。

## 包含的文件

| 路径 | 目的 |
| ---- | ------- |
| `hello.py` | 最小的端到端微调示例。训练模型重复小的身份字符串。 |
| `q20_agent.py` | 为 20 个问题玩家、回答者和模拟搜索工具提供支持的 CrewAI 流程。由训练和评估共享。**与 Agent-lightning 或 Tinker 无关。** |
| `q20_train.py` | 强化学习驱动程序，可将 Cookbook 循环适配到 Agent-lightning 回合中。支持空运行、分布式训练和搜索工具切换。**与 Agent-lightning 和 Tinker 都相关。** |
| `q20_evaluate.py` | 离线评估器，可重用 CrewAI 流程来对任何基于 OpenAI 或 Qwen 的模型进行基准测试。**仅与 Tinker 相关。** |
| `q20_nouns.csv` | 用于训练和验证的类别和答案。包含 `split` 和 `search_enabled` 元数据。 |
| `agl_tinker/` | 将 Agent-lightning 与 Tinker 集成的桥接包（见下文分解）。 |
| `tests/test_tinker_llm.py` | 自定义 LiteLLM 提供程序的健全性测试。使用 `pytest examples/tinker/tests` 运行。 |
| `.env.example` | LiteLLM、CrewAI 帮助程序和托管 Tinker 服务所需环境变量的模板。 |

`agl_tinker/` 组件：

| 路径 | 目的 |
| ---- | ------- |
| `agl_tinker/algo.py` | Agent-lightning `Algorithm` 封装器，将训练循环插入 `agl.Trainer`。 |
| `agl_tinker/env.py` | 虚拟环境和数据集构建器，将 Agent-lightning 任务适配到 Tinker 期望值。 |
| `agl_tinker/llm.py` | 由 Tinker 采样客户端支持的 LiteLLM 自定义提供程序。 |
| `agl_tinker/rollout.py` | 跨度到轨迹重建和回合批处理帮助程序。 |
| `agl_tinker/train.py` | 从 Tinker Cookbook 改编的 RL 训练循环。 |

## 设置

**1. 安装依赖项。** 从仓库根目录：

```bash
uv sync --frozen --extra apo --group dev --group agents --group tinker
```

如果您不使用 `uv`，请确保 `tinker`、`tinker_cookbook`、`litellm`、`crewai` 和 Agent-lightning 在同一环境中可用。

**2. 复制环境模板并填写凭据：**

```bash
cp examples/tinker/.env.example examples/tinker/.env
```

- `OPENAI_API_KEY` / `OPENAI_BASE_URL`：通过 LiteLLM 或 OpenAI 兼容的端点路由辅助代理（回答者、搜索、工具模拟）。
- `TINKER_API_KEY`：与托管的 Tinker 训练服务通信所必需。如果您只使用 OpenAI 模型，则可以跳过。
- `WANDB_API_KEY`：可选，当在 `q20_train.py` 中配置时启用 Weights & Biases 日志记录。
- `CREWAI_DISABLE_TELEMETRY=true`：防止 CrewAI 发出自己的遥测数据，以便 Agent-lightning 跟踪保持连贯。

3. 在运行命令之前加载环境，例如 `dotenv run -- <command>` 或手动导出变量。

## 运行 Hello 1024 示例

这是查看集成效果的最快方法。它会对 Qwen 模型进行微调，使其使用目标身份进行自我介绍。

**一键工作流程（在单个进程中生成存储、算法和运行器）**

```bash
dotenv run python hello.py oneclick
```

脚本将为 LiteLLM 代理和 Agent-lightning 存储选择空闲端口，然后遍历身份的综合数据集。

**分布式工作流程（有助于检查每个组件）**

```bash
agl store --port 4747
dotenv run python hello.py algo
dotenv run python hello.py runner
```

在单独的终端中启动命令。算法进程连接到现有存储，而运行器进程默认启动八个工作进程。日志写入 `examples/tinker/logs/hello`。

## 训练 20 个问题代理

20 个问题设置镜像官方 Cookbook 配方，但通过共享的 CrewAI 流驱动回合。

**空运行（内存存储和 LiteLLM 代理）**

```bash
dotenv run python q20_train.py dryrun
```

在不接触托管的 Tinker 服务的情况下，在少量样本上验证 CrewAI 流、奖励发射和跨距重建是否成功，非常有用。

**完整的分布式训练**

```bash
agl store --port 4747
dotenv run python q20_train.py algo --model qwen30b --search --port 4747
dotenv run python q20_train.py runner --port 4747 --n-runners 4
```

`--model` 选择 Tinker 托管的检查点（`qwen4b` 或 `qwen30b`）。添加 `--search` 以启用模拟的搜索工具，该工具依赖于环境变量中定义的辅助 LLM（该示例使用 LLM 驱动的搜索模拟而不是真实 API）。训练指标和检查点记录在 `examples/tinker/logs/q20_*` 下。当 Tinker 服务不可用时，您也可以使用 `verl` 替代 `algo` 命令。

您可以随时运行额外的运行器进程；它们会向存储注册并立即开始取出任务。

## 在 20 个问题上评估模型

重用 CrewAI 流来对任何 OpenAI 兼容的模型（托管在 Tinker、OpenAI 或另一个 LiteLLM 后端上）进行基准测试：

```bash
dotenv run python q20_evaluate.py \
  --model Qwen/Qwen3-30B-A3B-Instruct-2507 \
  --output-file logs/twenty_questions_results.jsonl \
  --search
```

结果追加到指定的 JSONL 文件中，因此您可以稍后计算聚合统计数据。

## 桥接的工作原理

`agl_tinker` 包通过模拟 Tinker 期望的接口来保持其余 Tinker 或 Tinker Cookbook 代码库不变：

- `AGLDatasetBuilder` 和 `AGLDummyEnv` 封装普通的 Agent-lightning 数据集，以便批次仍能产生 Tinker `EnvGroupBuilder` 对象，即使回合远程运行。
- `do_group_of_group_rollouts`（在 [`rollout.py`](agl_tinker/rollout.py) 中）将任务排入 Agent-lightning 存储，等待运行器完成，然后从 `TracerTraceToTriplet` 收集的跨距三元组重建 `Trajectory` 对象。
- `TinkerLLM` 实现了 LiteLLM 的 `CustomLLM`，因此训练循环可以更新采样客户端并通过 OpenAI 兼容的端点公开它们，而无需重写代理代码。
- `agl_tinker.algo.Tinker` 满足 Agent-lightning 的 `Algorithm` 契约，这意味着您可以通过 `agl.Trainer` 启动训练，与其他算法、调度程序或资源一起启动。

由于跨度和奖励是由您将要部署的相同回合函数发出的，因此评估和生产保持同步——无需维护单独的模拟器代码路径。

## 故障排除提示

- 如果运行器日志显示 `Triplet has no token_ids`，请确保您的 LiteLLM 代理返回对数概率和令牌 ID，并且令牌 ID 存在于存储中。提供的适配器需要它们来重建轨迹。有关更多详细信息，请参阅调试教程。
- 必须禁用 CrewAI 遥测（请参阅 `.env.example`），以便 AgentOps 跟踪保持自包含；否则，您可能会看到格式错误的跟踪。
- 仔细调整 `learning_rate`、`batch_size` 和 `group_size`。训练对这些超参数很敏感。