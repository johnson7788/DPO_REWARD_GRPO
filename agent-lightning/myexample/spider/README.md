# Spider 示例

[![spider CI 状态](https://github.com/microsoft/agent-lightning/actions/workflows/examples-spider.yml/badge.svg)](https://github.com/microsoft/agent-lightning/actions/workflows/examples-spider.yml)

# 1）测试运行Agent
Will only select the trajectories related to write and rewrite.# For debug, use single process. # Enable the dev debug mode.

python sql_agent.py --litsqlagent.trained-agents write --trainer.n-workers 1 --trainer.dev true 

# 2）测试训练0.5B的模型
export WANDB_BASE_URL=http://xxxx
export WANDB_API_KEY=local-xxx
wandb login
swanlab login -k sVxxxx
bash restart_ray.sh
python train_sql_agent.py fast

# 更详细讲解
https://medium.com/@yugez/training-ai-agents-to-write-and-self-correct-sql-with-reinforcement-learning-571ed31281ad

此示例演示了如何使用 Agent-Lightning 和强化学习在 Spider 数据集上训练文本到 SQL 的智能体。它兼容 Agent-lightning v0.2 或更高版本。

## 要求

此示例依赖于 LangChain v0.x 和几个 SQL 相关库。使用以下命令安装所需的依赖项：

```bash
pip install "langgraph<1.0" "langchain[openai]<1.0" "langchain-community" "langchain-text-splitters<1.0" "sqlparse" "nltk"
```


此外，请按照 [安装指南](../../docs/tutorials/installation.md) 安装 Agent-Lightning 和 VERL 相关依赖项。

## 数据集

详细的数据集准备说明可在 [如何训练 SQL 智能体](../../docs/how-to/train-sql-agent.md) 指南中找到。

## 包含的文件

| 文件/目录 | 描述 |
|----------|------|
| [train_sql_agent.py](train_sql_agent.py) | SQL 智能体的训练脚本，支持多种模型配置（Qwen、LLaMA、CI 的快速模式） |
| [sql_agent.py](sql_agent.py) | 使用 LangGraph 和 LangChain 实现的 SQL 智能体，具有调试功能 |
| `data/` | 包含 Spider 数据集文件的目录 |
| `spider_eval/` | 用于评估 SQL 智能体性能的评估工具 |

## 运行示例

### 训练

使用以下命令通过 Qwen2.5-Coder-1.5B-Instruct 模型训练 SQL 智能体。这需要至少有一个 40GB GPU 的单节点：

```bash
python train_sql_agent.py qwen
```


如果您想使用 NPU 进行训练，请参考 [如何训练 SQL 智能体](../../docs/how-to/train-sql-agent.md) 中的 **使用 NPU 启动训练** 部分。

### 调试

要交互式地测试和调试 SQL 智能体：

```bash
python sql_agent.py
```


此命令需要一个与 OpenAI 兼容的 API 服务。请使用 `OPENAI_API_BASE` 和 [OPENAI_API_KEY](test_integration.py#L79-L79) 环境变量配置您的服务端点和凭证。