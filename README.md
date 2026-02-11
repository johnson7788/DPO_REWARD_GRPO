# AgentGRPO

基于强化学习（GRPO/DPO）的AI Agent训练项目，通过奖励模型优化Agent行为。

## 项目概述

本项目是一个端到端的AI Agent后训练平台，包含：

- **奖励模型训练**：使用TRL训练奖励模型，评估Agent回答质量
- **Agent强化学习**：使用agent-lightning框架进行GRPO训练
- **具体应用场景**：医学问答SQL Agent等垂直领域Agent

## 项目结构

```
AgentGRPO/
├── agent-lightning/     # 核心训练框架 (Microsoft)
├── reward_model/        # 奖励模型训练
├── sql_agent/           # SQL医学问答Agent
├── trl/                 # Hugging Face强化学习库
└── doc/                 # 项目文档
```
## 准备
GRPO训练7B模型，最好2张A800，训练奖励模型4090*48G即可。
准备wandb和swanlab

## 模块说明

### 1. agent-lightning

Microsoft开发的Agent强化学习训练框架。

**核心特性**：
- 支持多种Agent框架：LangChain、OpenAI Agent SDK、AutoGen、CrewAI
- 支持多种训练算法：RL、APO、SFT、GRPO
- 零代码改动集成现有Agent
- 支持多Agent系统选择性优化

**核心模块**：
```
agentlightning/
├── trainer/           # 训练器主逻辑
├── algorithm/         # 算法实现 (VERL/GRPO, APO)
├── runner/             # 执行引擎
├── tracer/             # 追踪和埋点
├── store/              # 数据存储 (Memory/Mongo/SQLite)
└── cli/                # 命令行工具 (agl)
```

### 2. reward_model

使用TRL训练奖励模型，用于评估Agent回答质量。

**核心文件**：
| 文件 | 功能 |
|------|------|
| `reward_modeling.py` | TRL奖励模型训练 |
| `inference_api.py` | 推理API服务（评分接口） |
| `convert_dpo_format.py` | DPO数据格式转换 |

**技术栈**：
- 训练框架：TRL (Transformer Reinforcement Learning)
- 基础模型：Qwen2-0.5B-Instruct / Qwen2.5-7B-Instruct
- 训练方法：Reward Modeling（对比学习）

**API接口**：
```python
# POST /score - 单个回答评分
# POST /score-pair - pair对比评分
```

### 3. sql_agent

基于强化学习的医学问答Agent，通过SQL查询数据库回答用户问题。

**技术栈**：
- 训练框架：agent-lightning + verl (GRPO算法)
- Agent框架：openai-agents
- 基础模型：Qwen3-0.6B / Qwen2.5-7B-Instruct
- 数据库：drugs_info（药品）+ disease（疾病）

**工作流程**：
```
用户问题 → Agent生成SQL → 执行查询 → 整理回答 → 奖励评估
```

### 4. trl

Hugging Face的Transformer强化学习库，用于奖励模型训练。

**核心Trainer**：
| Trainer | 用途 |
|---------|------|
| `SFTTrainer` | 监督微调 |
| `GRPOTrainer` | Group Relative Policy Optimization |
| `DPOTrainer` | Direct Preference Optimization |
| `RewardTrainer` | 奖励模型训练 |

## 快速开始

### 环境要求

- Python 3.10+
- CUDA GPU（推荐）
- MongoDB（可选，用于持久化存储）

### 安装依赖

```bash
# 安装agent-lightning
cd agent-lightning
uv sync --group dev

# 安装奖励模型依赖
cd reward_model
pip install -r requirements.txt

# 安装sql_agent依赖
cd sql_agent
pip install -r requirements.txt
```

### 训练奖励模型

```bash
cd reward_model

# 1. 准备DPO格式数据
python convert_dpo_format.py --input=raw.jsonl --output=converted.jsonl

# 2. 训练奖励模型
CUDA_VISIBLE_DEVICES=0,1 accelerate launch reward_modeling.py \
  --dataset_name ./converted.jsonl \
  --model_name_or_path Qwen/Qwen2.5-7B-Instruct

# 3. 合并LoRA权重
swift export --model Qwen/Qwen2.5-7B-Instruct \
  --adapters ./reward_model_output --merge_lora true
```

### 启动推理API

```bash
cd reward_model
python inference_api.py --model_path ./merged_model
```

### 训练SQL Agent

```bash
cd sql_agent

# 1. 启动外部存储服务
agl store --port 9999

# 2. 测试运行（1步）
AGL_MANAGED_STORE=0 python train_sql_agent.py --ci-fast

# 3. 完整训练
AGL_MANAGED_STORE=0 python train_sql_agent.py \
  --llm-proxy \
  --model /path/to/model \
  --external-store-address http://localhost:9999
```

## 架构图

```
                            ┌─────────────────┐
                            │   外部LLM API   │
                            │  (DeepSeek等)   │
                            └────────┬────────┘
                                     │
┌────────────────────────────────────┼────────────────────────────────────┐
│                                    │                                    │
│  ┌──────────────────┐     ┌───────┴───────┐     ┌──────────────────┐   │
│  │   reward_model   │────▶│  sql_agent    │◀────│      trl         │   │
│  │   (奖励模型)      │     │  (医学问答)    │     │  (训练工具库)     │   │
│  └────────┬─────────┘     └───────┬───────┘     └──────────────────┘   │
│           │                       │                                     
│           │                       │                                     
│           │                ┌──────┴──────┐                              
│           │                │ agent-      │                              
│           └───────────────▶│ lightning    │                              
│                            │ (核心框架)   │                              
│                            └─────────────┘                              
```

## 技术栈

| 层次 | 技术 |
|------|------|
| 强化学习框架 | agent-lightning, verl, trl |
| 训练算法 | GRPO, DPO, Reward Modeling |
| Agent框架 | openai-agents |
| 基础模型 | Qwen2.5-7B-Instruct, Qwen3-0.6B |
| 数据库 | SQLite |
| 推理引擎 | vLLM |
| 实验跟踪 | wandb, swanlab |

## 文档

- `doc/checkpoint_files.md` - 检查点文件结构说明
- `doc/merge_vllm.md` - VLLM模型合并文档
- `doc/reward_test.md` - 奖励模型测试记录
- `doc/train_result_test.md` - 训练结果测试记录

## 许可证

本项目遵循项目原有许可证。
