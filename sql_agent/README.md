# SQL 搜索 Agent 的 GRPO 训练

基于强化学习的医学问答 Agent，通过 SQL 查询医学数据库回答用户问题。

## 准备环境
单张或者多张显卡的GPU服务器，然后确保硬盘大于500G，用于存储Checkpiont模型

## 训练框架

- **强化学习框架**: agent-lightning + verl (GRPO 算法)
- **Agent 框架**: openai-agents
- **基础模型**: Qwen/Qwen3-0.6B (可配置)

## 项目结构

## 环境准备
同步post_train代码到服务器，
cd post_train
# 获取镜像
docker pull modelscope-registry.us-west-1.cr.aliyuncs.com/modelscope-repo/modelscope:ubuntu22.04-cuda12.6.3-py311-torch2.7.1-vllm0.10.1.1-modelscope1.29.2-swift3.8.3

# 创建容器，如果只使用显卡1，不使用显卡0 --gpus "device=1"，如果公司的服务器，使用显卡1，并且swift更改名称，如果是云服务就不用更改这些命令
docker create \
  --runtime=nvidia --gpus all --net=host \
  --shm-size="10g" --cap-add=SYS_ADMIN \
  -v "$(pwd)":/workspace/post_train \
  -v "$HOME/.cache":/root/.cache \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  --name swift \
  modelscope-registry.us-west-1.cr.aliyuncs.com/modelscope-repo/modelscope:ubuntu22.04-cuda12.6.3-py311-torch2.7.1-vllm0.10.1.1-modelscope1.29.2-swift3.8.3 \
  sleep infinity

# 启动容器
docker start swift
docker exec -it swift bash

# 安装agent-lightning
克隆agent-lightning
```
cd agent-lightning
pip install uv
uv pip install --system  --no-cache-dir -e .[dev,agent,apo] fastmcp==2.14.1 openai-agents==0.6.3 vllm==0.10.1.1 verl==0.5.0 'litellm[proxy]>=1.78' 'agentops>=0.4.21' 'openai>=2.0.0'
```

## omegaconf验证
pip uninstall -y antlr4-python3-runtime
pip install antlr4-python3-runtime==4.9.3
python -c "import omegaconf; print('omegaconf import OK', omegaconf.__version__)"

# 检查安装配置信息
python utils/check_install.py

```
sql_agent/
├── sql_agent.py      # Agent 实现与奖励计算
├── tools.py          # 数据库查询工具
├── train.sh          # 训练启动脚本
├── sqlagent_test.py  # 独立测试脚本
└── data/
    ├── train.parquet     # 训练数据集
    ├── val.parquet       # 验证数据集
    └── qa_dataset.jsonl  # 原始问答数据
```



## 核心功能

### Agent 能力

通过 SQL 查询医学数据库回答用户问题，支持查询：

- **药品信息** (`drugs_info`): 药品名称、成分、适应症、不良反应、禁忌症等
- **疾病信息** (`disease`): 疾病名称、临床表现、并发症、诊断方法、治疗方案等

### 可用工具

`query_database_by_sql(sql: str)` - 执行 SQL 查询

根据自然语言问题生成 SQL 查询语句，查询药品或疾病数据库。

### 奖励机制

采用混合奖励策略：

1. **规则奖励** (0.1): 正确执行 SQL 查询即获得
2. **LLM 评估奖励** (0.0-1.0): 基于回答准确性、完整性、清晰性、专业性打分

## 快速开始

### 1. 安装依赖

```bash
cd agent-lightning
uv pip install --system  --no-cache-dir -e .[dev,agent,apo] fastmcp==2.14.1 openai-agents==0.6.3 vllm==0.10.1.1 verl==0.5.0 'litellm[proxy]>=1.78' 'agentops>=0.4.21' 'openai>=2.0.0'
```

### 2. 配置环境变量

```bash
cp env_template .env
```

### 3. 启动训练

```bash
cd sql_agent
# 配置WADDB，然后重启ray
WANDB_BASE_URL=http://xxxx
WANDB_API_KEY=local-xxxx
wandb login
swanlab login -k xxx
bash restart_ray.sh
# 单步测试
python train_sql_agent.py --ci-fast --model /workspace/post_train/post_train/sql_agent/Qwen3-0.6B
```

### 4. 测试运行

```bash
python sqlagent_test.py
```

### 5. 完整的训练命令
  第一步：先用 --ci-fast 验证流程跑通

  AGL_MANAGED_STORE=0 python train_sql_agent.py \
    --ci-fast \
    --llm-proxy \
    --model /workspace/post_train/post_train/sql_agent/Qwen2.5-7B-Instruct \
    --external-store-address http://117.133.60.219:45993

  这只跑 1 个训练步，目的是确认：triplets 能正常生成、训练步骤不崩溃。

  第二步：确认没问题后，正式训练

  AGL_MANAGED_STORE=0 python train_sql_agent.py \
    --llm-proxy \
    --model /workspace/post_train/post_train/sql_agent/Qwen2.5-7B-Instruct \
    --external-store-address http://117.133.60.219:45993

  去掉 --ci-fast 后走默认配置：2 个 epoch，每 20 步保存 checkpoint 和验证。

  各参数解释
  参数: AGL_MANAGED_STORE=0
  作用: 告诉框架不要自己管理 store 生命周期，因为你用了外部 store
  你的情况: 必须，配合 --external-store-address 使用
  ────────────────────────────────────────
  参数: --llm-proxy
  作用: 启用 OTel tracer + LlmProxyTraceToTriplet adapter，框架才能拦截 LLM 调用生成训练数据
  你的情况: 必须，之前漏了这个导致 0 triplets
  ────────────────────────────────────────
  参数: --model
  作用: 指定模型路径，覆盖默认的 Qwen3-0.6B
  你的情况: 指向你的 Qwen2.5-7B-Instruct
  ────────────────────────────────────────
  参数: --external-store-address
  作用: 连接外部存储服务，算法和 runner 之间交换数据
  你的情况: 你已有的外部 store
  ────────────────────────────────────────
  参数: --ci-fast
  作用: 只跑 1 步训练（测试用）
  你的情况: 调试时加，正式训练去掉
  ────────────────────────────────────────
  参数: --ci
  作用: 跑 20 步训练（轻量验证）
  你的情况: 介于调试和正式之间
  ────────────────────────────────────────
  参数: --n-runners
  作用: runner worker 数量，默认 4
  你的情况: 默认即可
  ────────────────────────────────────────
  参数: --debug
  作用: 打开 DEBUG 日志
  你的情况: 排查问题时可加
  另外注意



## 数据格式

训练数据为 Parquet 格式，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 样本唯一标识 |
| question | string | 用户问题 |
| answer | string | 标准答案 (训练时动态生成) |

## 配置说明

主要训练参数 (`train.sh`):

- `BASE_MODEL`: 基础模型路径
- `data.train_batch_size`: 训练批次大小
- `actor_rollout_ref.actor.optim.lr`: 学习率
- `actor_rollout_ref.rollout.n`: 每个问题的采样数
- `trainer.total_epochs`: 训练轮数


## 故障, 尝试更换modelscope-registry.us-west-1.cr.aliyuncs.com/modelscope-repo/modelscope:ubuntu22.04-cuda12.6.3-py311-torch2.7.1-vllm0.10.1.1-modelscope1.29.2-swift3.8.3为其它的镜像
如果出现容器内CUDA不可用，vllm加载失败，尝试升级下CUDA驱动sudo apt install nvidia-driver-590-server-open
root@10-60-176-80:/workspace/post_train/post_train# python utils/
chat_session_filter.py   filter_again.py          filter_with_llm.py       progress.json            xunzheng_question.jsonl
check_install.py         filtered_output.jsonl    open_evidence.json       README.md
.env                     filter_new_question.py   openevidence.py          reward_scale.py
root@10-60-176-80:/workspace/post_train/post_train# python utils/check_install.py
/usr/local/lib/python3.11/site-packages/torch/cuda/__init__.py:61: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
=== 环境诊断开始 ===
Python: 3.11.11 (main, Aug 15 2025, 16:18:34) [GCC 11.4.0]
PyTorch: 2.7.1+cu126
CUDA Available: False

--- 1. 检测 Flash Attention ---
✅ Flash Attention 导入成功. 版本: 2.7.4.post1

--- 2. 检测 vLLM (原生) ---
❌ vLLM 导入失败: Could not import module 'ProcessorMixin'. Are this object's requirements defined correctly?

--- 3. 检测 verl 兼容层 (关键故障点) ---
❌ verl.third_party.vllm 导入直接崩溃: Could not import module 'ProcessorMixin'. Are this object's requirements defined correctly?

=== 诊断结束 ===

## 注意
要注意sql_agent.py中的Agent执行轮次，max_turns和verl中训练的max_turns必须是一致的。

## 如果出现这个错误，大部分是连接不到AGL的store，可以暂时不用AGL_MANAGED_STORE=0
   Tracing: request failed: [Errno 101] Network is unreachable
   Set LightningStoreOTLPExporter endpoint to http://117.133.60.219:45993/v1/traces