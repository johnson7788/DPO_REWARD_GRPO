# ADK 示例

本文件夹包含一个可运行的示例，该示例将ADK代理与Agent-lightning的VERL集成相结合。有关架构详细信息，请阅读[训练ADK代理操作指南](./train-adk-agent.md)。本README仅专注于安装依赖项和运行脚本。

## 安装

```bash
cd examples/google_adk
pip install "agentlightning[verl,adk]" "google-adk>=0.3.0"
# 或者: uv sync
```

您需要一台配备40GB GPU（A100或类似型号）的机器来进行完整训练；CPU和较小的GPU足以用于CI模式。

## 准备数据

创建符合`AdkTask`模式（`question`、`app_id`、`ground_truth`、可选的`meta`）的`data/train.parquet`和`data/test.parquet`文件。要下载并转换Spider数据集（与`examples/spider`相同）：

```bash
uv run python prepare_dataset.py --download
```

或者，使用`--train`和`--test`标志转换您自己的JSON/CSV文件。详见操作指南。

## 运行训练

```bash
python train_adk.py \
  --train-file data/train.parquet \
  --val-file data/test.parquet \
  --model ${OPENAI_MODEL:-meta-llama/Meta-Llama-3-8B-Instruct} \
  --endpoint ${OPENAI_API_BASE:-http://localhost:8000/v1}
```

有用的标志：

- `--ci` / `--ci-fast` 缩减运行器数量和数据集切片以进行冒烟测试。
- `--external-store-address` 连接到现有的LightningStore服务。
- `--wandb-project` / `--wandb-run-name` 启用Weights & Biases日志记录。

脚本读取的环境变量：

- `OPENAI_API_BASE`、`OPENAI_API_KEY`、`OPENAI_MODEL`
- `HF_TOKEN`（VERL检查点托管在Hugging Face上时必需）

## 快速调试循环

在使用GPU时间之前，请运行：

```bash
python adk_debug.py --file data/test.parquet --index 0
```

这将使用训练中相同的ADK连接执行单次演练，让您确认凭据、数据集行和跟踪发射，而无需启动VERL。使用`--model`和`--endpoint`覆盖指向不同的LLM后端。