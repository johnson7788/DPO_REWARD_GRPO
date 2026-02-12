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
├── agent-lightning/     # 核心Agent训练框架 (Microsoft)
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

### 安装依赖

```bash
参考，使用容器进行准备训练环境。
[奖励模型训练.md](reward_model/%E5%A5%96%E5%8A%B1%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83.md)和[README.md](sql_agent/README.md)

# 安装奖励模型依赖
cd reward_model
pip install -r requirements.txt

# 安装sql_agent依赖
cd sql_agent
pip install -r requirements.txt
```

### 训练奖励模型
参考：[README.md](reward_model/README.md)

### 启动推理API
[inference_api.py](reward_model/inference_api.py)

### 训练Agent模型
参考[README.md](sql_agent/README.md)

## 架构图
1. 合成训练数据，生成DPO数据集
2. 根据DPO数据集生成奖励模型
3. 根据奖励模型训练Agent模型

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

## 📬 联系方式

如有问题，请联系作者：
![weichat.png](doc/weichat.png)
