# Calc-X 示例

[![calc_x CI status](https://github.com/microsoft/agent-lightning/actions/workflows/examples-calc-x.yml/badge.svg)](https://github.com/microsoft/agent-lightning/actions/workflows/examples-calc-x.yml)

本示例演示了如何使用 Agent-Lightning 和 VERL 算法以及 AutoGen 框架训练一个数学推理智能体。该智能体通过计算器工具使用模型上下文协议（MCP）解决数学问题。它与 Agent-lightning v0.2 或更高版本兼容。

## 要求

本示例需要单个节点至少配备一块 40GB 显存的 GPU。请按照[安装指南](../../docs/tutorials/installation.md)安装 Agent-Lightning 和 VERL 相关依赖项。

此外，请确保正确安装 `uv` 和 MCP 计算器服务器。智能体在解决问题过程中依赖 MCP 协议来访问计算器功能。

```bash
pip install "autogen-agentchat" "autogen-ext[openai]" "mcp>=1.10.0"
```

## 数据集

从[这里](https://drive.google.com/file/d/1FQMyKLLd6hP9dw9rfZn1EZOWNvKaDsqw/view?usp=sharing)下载 Calc-X 数据集的 parquet 格式文件，并将其解压到 `data` 文件夹：

```bash
unzip calc-x-data.zip -d data
```

数据集包含用于训练和评估的带真实解的数学问题。

## 包含的文件

| 文件/目录 | 描述 |
|----------------|-------------|
| `calc_agent.py` | 使用 AutoGen 和 MCP 计算器工具的数学问题解决智能体 |
| `train_calc_agent.py` | 使用 VERL 算法的训练脚本，具有可配置的超参数 |
| `eval_utils.py` | 用于评估智能体在数学问题上准确性的评估工具 |
| `data/` | 包含 parquet 格式训练和测试数据集的目录 |
| `tests/` | 测试文件，包括 MCP 计算器验证脚本 |
| `legacy_calc_agent.py` | 与 Agent-lightning v0.1.x 兼容的旧版智能体实现（已弃用） |
| `legacy_calc_agent_debug.py` | 与 Agent-lightning v0.1.x 兼容的旧版调试脚本（已弃用） |
| `legacy_train.sh` | 与 Agent-lightning v0.1.x 兼容的旧版训练脚本（已弃用） |

## 运行示例

### 训练

训练过程使用分布式 Ray 工作进程并行运行智能体 rollout，同时训练服务器优化模型。启动训练前先启动 Ray：

```bash
bash ../../scripts/restart_ray.sh
```

如果您想使用 Weights & Biases 跟踪实验，请在启动 Ray **之前**设置 `WANDB_API_KEY` 环境变量。

然后运行训练脚本：

```bash
python train_calc_agent.py --train-file data/train.parquet --val-file data/test.parquet
```

脚本会自动启动智能体工作进程和训练服务器。智能体工作进程使用 MCP 计算器执行数学问题 rollout，而训练服务器应用 VERL 算法根据奖励改进模型。

### 调试

要交互式地测试智能体而不进行训练：

```bash
python calc_agent.py
```

这将在示例问题上运行智能体，以验证 MCP 计算器集成和 AutoGen 设置是否正常工作。此测试依赖于可用的 OpenAI 服务。将 `OPENAI_API_KEY` 环境变量设置为 OpenAI 服务的 API 密钥；并将 `OPENAI_API_BASE` 环境变量设置为 OpenAI 服务的基础 URL。

一个常见的问题是如果环境未正确配置，智能体可能会无限期挂起。通过运行以下命令验证 `uv` 和 MCP 计算器服务器是否正确安装：

```bash
python tests/test_mcp_calculator.py
```


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
# 2. 重启RAY： 配置Wandb环境变量和重启ray
export VERL_USE_MODELSCOPE=True
export WANDB_BASE_URL=http://117.133.60.219:3005/
export WANDB_API_KEY=local-7869e4d78f84a511b65ffc6255d2402598edb5b5
wandb login
bash restart_ray.sh

AGL_MANAGED_STORE=0 python train_calc_agent.py --external-store-address http://117.133.60.219:45993
```

或者，如果需要，您也可以分别运行算法和执行器：

```bash
# 训练代码
AGL_MANAGED_STORE=0 AGL_CURRENT_ROLE=algorithm python train_calc_agent.py --external-store-address http://117.133.60.219:45993
# Agent推理代码
AGL_MANAGED_STORE=0 AGL_CURRENT_ROLE=runner python train_calc_agent.py --external-store-address http://117.133.60.219:45993
```
