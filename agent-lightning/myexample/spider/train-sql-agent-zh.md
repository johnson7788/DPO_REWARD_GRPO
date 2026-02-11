# 使用 Agent-lightning 和 VERL 训练 SQL Agent

本指南基于 **Agent-lightning SQL Agent** 示例，解释了系统组件如何集成：一个包装为 [`LitAgent`][agentlightning.LitAgent] 的 **LangGraph-based SQL agent**，**[`VERL`][agentlightning.algorithm.verl.VERL] 强化学习 (RL) 算法**，以及协调训练和调试的 **[`Trainer`][agentlightning.Trainer]**。

命令行接口在 [`examples/spider/train_sql_agent.py`]({{ src("examples/spider/train_sql_agent.py") }}) 中提供了一个完整的可运行示例。但是，本文档专注于理解底层架构，这样您可以有效地将工作流适应到您自己的代理中。

## SQL 代理架构

Agent-lightning 与各种编排框架无缝集成，包括 [Agent Framework](https://github.com/microsoft/agent-framework)、[AutoGen](https://github.com/microsoft/autogen)、[CrewAI](https://www.crewai.com/)、[LangGraph](https://github.com/langchain-ai/langgraph) 和 [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)。它还可以与自定义 Python 逻辑互操作。

在这个示例中，**LangGraph** 定义了一个循环工作流，模仿分析师的迭代 SQL 开发过程。下面的图表（直接从 [`sql_agent.py`]({{ src("examples/spider/sql_agent.py") }}) 渲染）说明了代理如何起草、执行、评估和优化查询，直到获得满意的结果。

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph LR;
        __start__([<p>__start__</p>]):::first
        write_query(write_query)
        execute_query(execute_query)
        check_query(check_query)
        rewrite_query(rewrite_query)
        __end__([<p>__end__</p>]):::last
        __start__ --> write_query;
        check_query -.-> __end__;
        check_query -.-> rewrite_query;
        execute_query --> check_query;
        rewrite_query --> execute_query;
        write_query --> execute_query;
        classDef default fill:#f2f2f2,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#cccccc
```

!!! note

    工作流程经历以下阶段：

    1. **write_query** – 从用户的问题和数据库模式生成初始 SQL 查询。
    2. **execute_query** – 在目标数据库上执行生成的查询。
    3. **check_query** – 使用专门的提示（`CHECK_QUERY_PROMPT`）评估查询及其结果（或错误）来检测问题。
    4. **rewrite_query** – 如果发现问题，代理使用上一步的反馈重写查询并重新进入循环。
    5. **END** – 当查询被验证或达到最大迭代次数（`max_turns`）时，循环终止。每个*回合*包含一次完整的 `write_query`、`execute_query`、`check_query` 和（如果适用）`rewrite_query` 阶段循环。

在本教程中，**强化学习 (RL)** 用于优化 `write_query` 和 `rewrite_query` 阶段。虽然 `check_query` 步骤共享相同的底层 LLM 权重，但其跟踪数据不用于学习。

为了保持设计的模块化和可维护性，建议在单独的文件中定义 LangGraph-based SQL Agent，并通过构建器函数（如）公开它：

```python
def build_langgraph_sql_agent(
    database_path: str,
    openai_base_url: str,
    model: str,
    sampling_parameters: Dict[str, Any],
    max_turns: int,
    truncate_length: int
):
    builder = StateGraph(State)
    builder.add_node(write_query)
    ...

    builder.add_edge(START, "write_query")
    ...

    return builder.compile().graph()
```

这种方法将您的 LangGraph 逻辑与 Agent-lightning 版本更改隔离，提高了可读性和可调试性。

## 连接 LangGraph 和 Agent-lightning

!!! tip

    阅读此部分时，请在旁边打开 [`sql_agent.py`]({{ src("examples/spider/sql_agent.py") }})。这将帮助您了解此处显示的代码片段在实践中是如何工作的。

**`LitSQLAgent`** 类在 [`sql_agent.py`]({{ src("examples/spider/sql_agent.py") }}) 中定义，充当桥梁。它继承自 [`agl.LitAgent`][agentlightning.LitAgent]，允许运行器为每次 rollout 提供共享资源（例如，[LLMs][agentlightning.LLM]）。

以下是关键逻辑的简化说明（注意：这是概念伪代码；实际实现包括数据集特定细节）：

```python
class LitSQLAgent(agl.LitAgent[Dict[str, Any]]):

    def __init__(self, max_turns: int, truncate_length: int):
        # 每个回合在这里指代 write/exe/check/rewrite 的完整循环
        self.max_turns = max_turns
        self.truncate_length = truncate_length

    def rollout(
        self,
        task: Dict[str, Any],
        resources: agl.NamedResources,
        rollout: agl.Rollout
    ) -> float | None:
        llm: agl.LLM = resources["main_llm"]
        agent = build_langgraph_sql_agent(
            database_path="sqlite:///" + task["db_id"],
            max_turns=self.max_turns,
            truncate_length=self.truncate_length,
            openai_base_url=llm.get_base_url(rollout.rollout_id, rollout.attempt.attempt_id),
            model=llm.model,
            sampling_parameters=llm.sampling_parameters,
        )
        result = agent.invoke({"question": question}, {
            "callbacks": [self.tracer.get_langchain_handler()],
            "recursion_limit": 100,
        })
        reward = evaluate_query(result["query"], ground_truth, db_path, raise_on_error=False)
        return reward
```

`LitSQLAgent` 充当 LangGraph 代理的轻量级包装器，为 [`rollout`][agentlightning.LitAgent.rollout] 方法提供正确的接口。它构建 LangGraph 代理，调用它，并将评估结果作为奖励信号返回。

`"main_llm"` 资源键是代理和 [VERL][agentlightning.algorithm.verl.VERL] 之间的约定。它用于在 rollout 期间从 [VERL][agentlightning.algorithm.verl.VERL] 算法注入 OpenAI 兼容端点。支持两种方法来使用此 [agentlightning.LLM][] 资源：

1. **直接访问** – 使用 [`llm.endpoint`][agentlightning.LLM.endpoint] 进行简单集成（与 v0.1 示例相同）。
2. **上下文感知访问** – 使用 [`get_base_url`][agentlightning.ProxyLLM.get_base_url] 配合 [`rollout.rollout_id`][agentlightning.Rollout.rollout_id] 和 [`rollout.attempt.attempt_id`][agentlightning.Attempt.attempt_id]。
   这种方法启用了按调用者跟踪归属，在运行器端跟踪器不可用时改进每个 rollout 或尝试的跟踪收集。详情请参见 [处理跟踪](../tutorials/traces.md)。

## 奖励信号和评估

`evaluate_query` 函数为 RL 训练提供了奖励机制。在代理训练中，获取一致且有意义的奖励信号通常具有挑战性。幸运的是，使用 [**Spider 数据集**](https://yale-lily.github.io/spider) 时这会简化。该数据集包含约 8k 样本，包含自然语言问题、数据库模式和真实 SQL 查询。

使用 [**Spider 评估器**](https://github.com/taoyds/test-suite-sql-eval)，代理生成的查询在目标数据库上执行并与真实查询进行比较。如果两个查询产生相同的执行结果，则认为它们等价。

!!! attention

    在训练期间绝不应向代理暴露真实查询，以防止数据泄漏。

在此设置中，奖励直接从 [`rollout`][agentlightning.LitAgent.rollout] 方法返回，使运行器能够将其转发回 RL 算法。

!!! warning

    避免同时使用 [`emit_reward`][agentlightning.emit_reward] 和返回奖励值。这样做会导致算法接收重复的奖励信号，导致训练行为不一致。

## 配置 VERL 进行强化学习

查看 [`examples/spider/train_sql_agent.py`]({{ src("examples/spider/train_sql_agent.py") }}) 获取完整的强化学习配置，这是一个纯 Python 字典。它镜像（实际上就是）用于在 VERL 框架中启动训练的 [shell 参数](https://verl.readthedocs.io/en/latest/index.html)，但更容易编程调整：

```python
verl_config: Dict[str, Any] = {
    "algorithm": {"adv_estimator": "grpo", "use_kl_in_reward": False},
    "data": {
        # train_files 和 val_files 不再需要在此处
        # 因为数据在 agl.Trainer 中读取
        ...,
        # 控制每步池化的任务数量
        # （乘以 actor_rollout_ref.rollout.n）
        "train_batch_size": 32,
        # 大于这些长度的提示和响应会被截断
        "max_prompt_length": 4096,
        "max_response_length": 2048,
    },
    "actor_rollout_ref": {
        "rollout": {
            # 目前仅支持 vLLM
            "name": "vllm",
            # 等于 GRPO 的组大小
            "n": 4,
            # 用于在 vLLM 中启用工具调用解析器
            "multi_turn": {"format": "hermes"},
            ...
        },
        "actor": {"ppo_mini_batch_size": 32, "optim": {"lr": 1e-6}, ...},
        "model": {
            # 在此处配置您首选的 LLM
            "path": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
            ...
        },
    },
    "trainer": {
        "n_gpus_per_node": 1,
        # 训练开始前进行一次验证
        "val_before_train": True,
        # 每 N 个训练步骤进行一次验证
        "test_freq": 32,
        # 每 N 个训练步骤保存一次检查点
        "save_freq": 64,
        # 遍历训练数据集这么多次
        "total_epochs": 2
    },
}
```

这相当于以下 CLI 调用：

```bash
python3 -m verl.trainer.main_ppo \
    algorithm.adv_estimator=grpo \
    algorithm.use_kl_in_reward=False \
    data.train_batch_size=32 \
    data.max_prompt_length=4096 \
    data.max_response_length=2048 \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.n=4 \
    actor_rollout_ref.rollout.multi_turn.format=hermes \
    actor_rollout_ref.actor.ppo_mini_batch_size=32 \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.model.path=Qwen/Qwen2.5-Coder-1.5B-Instruct \
    trainer.n_gpus_per_node=1 \
    trainer.val_before_train=True \
    trainer.test_freq=32 \
    trainer.save_freq=64 \
    trainer.total_epochs=2
```

!!! warning
    我们过去在 v0.1 中提供了一个名为 `python -m agentlightning.verl` 的 CLI 来启动训练。这不再是推荐的方法。相反，使用 [`agl.Trainer`][agentlightning.Trainer] 一起运行 VERL 和代理运行器，或者如果您想要类似 v0.1 的隔离体验，请遵循 [调试教程](../tutorials/debug.md)。
## 使用 [`Trainer`][agentlightning.Trainer] 协调训练

[`Trainer`][agentlightning.Trainer] 是高级协调器，集成代理、算法、数据集和分布式运行器。使用 [`Trainer`][agentlightning.Trainer] 的主要好处是：

1. 它允许您用一行代码启动所有内容：`trainer.fit(...)`。
2. 它公开配置选项，如 `n_runners` 以控制并行度，以及 `adapter` 以定义算法如何解释代理生成的跟踪数据。

下面显示了一个使用示例：

```python
import agentlightning as agl

agent = LitSQLAgent()
algorithm = agl.VERL(verl_config)
trainer = agl.Trainer(
    n_runners=10,
    algorithm=algorithm,
    adapter={"agent_match": active_agent},
)
train_data = pd.read_parquet("data/train_spider.parquet").to_dict("records")
val_data = pd.read_parquet("data/test_dev_500.parquet").to_dict("records")
trainer.fit(agent, train_dataset=train_data, val_dataset=val_data)
```

首先，`agl.VERL(verl_config)` 启动 [`VERL`][agentlightning.algorithm.verl.VERL] 算法及其 OpenAI 兼容代理。[`VERL`][agentlightning.algorithm.verl.VERL] 接收 `train_data` 和 `val_data`，并将任务排队到由 [`LightningStore`][agentlightning.LightningStore] 管理的集中式任务队列中，所有运行器都可以访问。

当调用 [`Trainer.fit`][agentlightning.Trainer.fit] 时，它启动 10 个并发运行器（由 `n_runners=10` 指定）。每个运行器从集中式任务队列中拉取任务，执行代理的 [`rollout`][agentlightning.LitAgent.rollout] 方法，收集跟踪，并将奖励返回给 VERL 进行训练。

前面讨论过的 [`Adapter`][agentlightning.Adapter] 在算法端使用，接收由代理和运行器发出的跨度。`agent_match` 参数确保 [`VERL`][agentlightning.algorithm.verl.VERL] 只摄入来自您要优化的特定代理的跨度。
在上面的示例中，至少有三个代理——`write_query`、`rewrite_query` 和 `check_query`。通过将 `agent_match` 设置为正则表达式如 `"write"`，可以同时优化 `write_query` 和 `rewrite_query` 代理。如果需要，也可以将其设置为 `"write|check"` 或 `None` 以包含所有代理。

## 使用 [`Trainer.dev`][agentlightning.Trainer.dev] 进行试运行

在投入数小时 GPU 时间之前，您可以使用 [`Trainer.dev()`][agentlightning.Trainer.dev] 对代理进行**试运行**。此方法切换到轻量级 [`Baseline`][agentlightning.Baseline] 算法，排队最多十个任务，并打印代理发出的每个跨度。因为它使用与完整训练相同的运行器堆栈，所以非常适合验证数据库连接和 LangGraph 控制流。

首先，代理需要一个有效的 OpenAI 兼容端点，因为 VERL 在这种模式下不活跃。您可以使用 OpenAI 的官方 API 或您自己的本地 LLM 端点。如下包装：

```python
trainer = agl.Trainer(
    n_workers=1,
    initial_resources={
        "main_llm": agl.LLM(
            endpoint=os.environ["OPENAI_API_BASE"],
            model="gpt-4.1-nano",
            sampling_parameters={"temperature": 0.7},
        )
    },
)
```

然后，使用少量任务调用 [`trainer.dev(...)`][agentlightning.Trainer.dev]：

```python
dev_data = pd.read_parquet("data/test_dev_500.parquet").to_dict("records")[:10]
trainer.dev(agent, dev_dataset=dev_data)
```

在 Python 会话中运行此代码或将脚本适配为包含 `--dev` 标志。一旦跨度看起来健康且奖励非零，切换回 [`trainer.fit(...)`][agentlightning.Trainer.fit] 进行完整的 RL 训练。有关如何调试代理的更多提示，请参阅 [调试教程](../tutorials/debug.md)。

## 运行示例代码

以下教程说明如何在 [`examples/spider`]({{ src("examples/spider") }}) 中运行完整示例。

### 数据集

训练器期望在 `examples/spider/data` 内有三个 Parquet 文件：
`train_spider.parquet`、`test_dev_500.parquet` 和 `test_dev.parquet`。

下载随存储库提供的策划数据包：

```bash
cd examples/spider
pip install gdown  # 包含在 'experiment' 可选依赖项中
gdown --fuzzy https://drive.google.com/file/d/1oi9J1jZP9TyM35L85CL3qeGWl2jqlnL6/view
unzip -q spider-data.zip -d data
rm spider-data.zip
```

如果您更愿意自己生成文件，请下载 [Spider 1.0](https://yale-lily.github.io/spider) 并运行：

```bash
python spider_eval/convert_dataset.py
```

如果将数据集存储在默认 `data` 目录之外，请设置 `VERL_SPIDER_DATA_DIR`。

### 依赖项

创建一个干净的虚拟环境，激活它，并安装 Agent-lightning 所需的 VERL 额外组件，这些组件由 [本教程](../tutorials/installation.md) 要求。根据需要安装 LangChain 相关依赖项。

对于完整训练配置文件，计划使用至少 **40 GB** 内存的 GPU。

### 启动训练

从 [`examples/spider`]({{ src("examples/spider") }}) 开始，根据您的模型偏好运行以下助手脚本之一：

```bash
python train_sql_agent.py qwen   # 默认 Qwen-2.5-Coder-1.5B 运行
python train_sql_agent.py llama  # LLaMA-3.2-1B 与 llama3_json 工具解析器
```

该脚本实例化 `LitSQLAgent` 并启动 [`trainer.fit`][agentlightning.Trainer.fit]。
如果您只想训练图中的一个代理，请提供 `--active-agent my_agent_variant`。

对于 LLaMA 配置文件，在运行之前导出 `HF_TOKEN`，以便 VERL 可以下载模型权重。

!!! tip "故障排除"

    如果您在任一 `WANDB_API_KEY` 未设置、`HF_TOKEN` 未设置或数据未找到的 Ray 工作进程错误上遇到问题，请尝试使用助手脚本重启 Ray 集群：[scripts/restart_ray.sh]({{ src("scripts/restart_ray.sh") }})，这本质上会停止任何现有的 ray 集群，并启动一个新集群：

    ```bash
    env RAY_DEBUG=legacy HYDRA_FULL_ERROR=1 VLLM_USE_V1=1 ray start --head --dashboard-host=0.0.0.0
    ```

!!! note "使用 NPU 启动训练"

    该示例还支持使用 **华为昇腾 NPU** 运行。此功能由 [华为团队](https://github.com/microsoft/agent-lightning/pull/272) 贡献。要使用它，请求助于脚本中的 `config_train_npu` 函数。

    **硬件支持：** Atlas 200T A2 Box16、Atlas 900 A2 PODc、Atlas 800T A3。至少需要 **单个 40GB NPU** 来运行 **Qwen2.5-Coder-1.5B-Instruct** 模型。

    **环境设置：** Python 3.11.13、CANN 8.2.RC1、torch 2.7.1+cpu、torch_npu 2.7.1.dev20250724。有关基本环境准备，请参考此 [文档](https://gitcode.com/Ascend/pytorch)。

    在安装依赖项之前，配置以下 pip 镜像：

    ```bash
    pip config set global.index-url http://repo.huaweicloud.com/repository/pypi/simple
    pip config set global.extra-index-url "https://download.pytorch.org/whl/cpu/ https://mirrors.huaweicloud.com/ascend/repos/pypi"
    ```

    然后安装 vLLM、vLLM-Ascend 和 VERL：

    ```bash
    pip install vllm==0.10.0 --trusted-host repo.huaweicloud.com
    pip install vllm-Ascend==0.10.0rc1 --trusted-host repo.huaweicloud.com
    pip install verl==0.5.0
    ```

    为确保 VERL 框架在 NPU 上正确运行，请将以下行添加到 `verl/utils/vllm_utils.py`：

    ```python
    from vllm_ascend.patch import platform
    from vllm_ascend.patch import worker
    ```

    有关更多详细信息，请参阅以下参考资料：[https://github.com/vllm-project/vllm-ascend/issues/1776](https://github.com/vllm-project/vllm-ascend/issues/1776)。

    安装上述依赖项后，从 [`examples/spider`]({{ src("examples/spider") }}) 运行以下脚本命令：

    ```bash
    python train_sql_agent.py npu
    ```

### 在没有 VERL 的情况下调试代理

[`sql_agent.py`]({{ src("examples/spider/sql_agent.py") }}) 还提供了一个 `debug_sql_agent()` 助手，可在引入 VERL 之前直接对本地或托管的 OpenAI 兼容端点运行 LangGraph 工作流。

设置以下环境变量，然后执行该文件：

```bash
export OPENAI_API_BASE=<your_api_base>
export OPENAI_API_KEY=<your_api_key>
cd examples/spider
python sql_agent.py
```

这允许您在引入强化学习之前验证工作流和提示是否按预期工作。

### 评估

以下结果是通过在单个 80 GB GPU 上运行 `python train_sql_agent.py qwen` 获得的。
训练大约需要 **12 小时**完成。
以下训练曲线通过每 16 步聚合一次以更好地可视化。

额外的评估结果是使用旧版本收集的——Agent-lightning v0.1.1、`verl==0.5.0` 和 `vllm==0.10.0`。
您可以在以下文章中找到它们：[使用强化学习训练 AI 代理编写和自我修正 SQL](https://medium.com/@yugez/training-ai-agents-to-write-and-self-correct-sql-with-reinforcement-learning-571ed31281ad)


<div style="height:400px">
<canvas data-chart='{"type": "line", "data": {"labels": [0.0, 16.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0], "datasets": [{"label": "Training", "data": [0.4609375, 0.5041666666666667, 0.5790441176470589, 0.6015625, 0.6070772058823529, 0.6208333333333333, 0.6668198529411765, 0.66875, 0.6709558823529411, 0.6708333333333333, 0.6847426470588235, 0.6791666666666667, 0.6819852941176471, 0.690625, 0.7008272058823529, 0.7453125, 0.7398897058823529, 0.7119791666666667, 0.7224264705882353, 0.7114583333333333, 0.7431066176470589, 0.7427083333333333, 0.75, 0.7302083333333333, 0.7247242647058824, 0.7390625, 0.7463235294117647, 0.7376302083333334], "spanGaps": true}, {"label": "Validation", "data": [0.342, null, 0.594, null, 0.642, null, 0.66, null, 0.676, null, 0.676, null, 0.694, null, 0.712, null, 0.702, null, 0.678, null, 0.702, null, 0.702, null, 0.674, null, 0.734, 0.722], "spanGaps": true}]}, "options": {"interaction": {"mode": "nearest", "intersect": false}, "plugins": {"legend": {"display": true, "position": "top"}, "title": {"display": true, "text": "SQL Agent Training Result (agent_match = write)"}}, "scales": {"x": {"title": {"display": true, "text": "Step (aggregated)"}}, "y": {"title": {"display": true, "text": "Accuracy"}}}}}'></canvas>
</div>

<div style="height:400px">
<canvas data-chart='{"type": "line", "data": {"labels": [0.0, 16.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0], "datasets": [{"label": "Training", "data": [0.4560546875, 0.578125, 0.6167279411764706, 0.6401041666666667, 0.6461397058823529, 0.6598958333333333, 0.6838235294117647, 0.69375, 0.6916360294117647, 0.6833333333333333, 0.6893382352941176, 0.6921875, 0.6838235294117647, 0.70625, 0.7045036764705882, 0.7442708333333333, 0.7288602941176471, 0.7317708333333334, 0.7311580882352942, 0.7286458333333333, 0.7316176470588235, 0.7359375, 0.7366727941176471, 0.7208333333333333, 0.7118566176470589, 0.7296875, 0.7389705882352942, 0.7350260416666666], "spanGaps": true}, {"label": "Validation", "data": [0.33, null, 0.62, null, 0.662, null, 0.682, null, 0.696, null, 0.7, null, 0.708, null, 0.692, null, 0.72, null, 0.7, null, 0.7, null, 0.702, null, 0.694, null, 0.702, 0.682], "spanGaps": true}]}, "options": {"interaction": {"mode": "nearest", "intersect": false}, "plugins": {"legend": {"display": true, "position": "top"}, "title": {"display": true, "text": "SQL Agent Training Result (agent_match = null)"}}, "scales": {"x": {"title": {"display": true, "text": "Step (aggregated)"}}, "y": {"title": {"display": true, "text": "Value"}}}}}'></canvas>
</div>