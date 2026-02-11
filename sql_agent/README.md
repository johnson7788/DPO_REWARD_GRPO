# SQL Agent GRPO 训练

基于强化学习（GRPO 算法）的医学问答 Agent，通过 SQL 查询医学数据库回答用户问题。

## 特性

- **Agent 能力**：通过 SQL 查询医学数据库回答用户问题
- **数据库**：支持药品信息、疾病信息查询
- **训练框架**：agent-lightning + verl (GRPO)
- **基础模型**：Qwen/Qwen3-0.6B（可配置）

## 快速开始

### 1. 安装依赖

```bash
cd agent-lightning
uv pip install --system --no-cache-dir -e .[dev,agent,apo] \
  fastmcp==2.14.1 openai-agents==0.6.3 vllm==0.10.1.1 verl==0.5.0 \
  'litellm[proxy]>=1.78' 'agentops>=0.4.21' 'openai>=2.0.0'
```

### 2. 验证安装

```bash
python utils/check_install.py
```

### 3. 启动训练

```bash
cd sql_agent

# 配置 wandb 和 swanlab
export WANDB_BASE_URL=http://xxxx
export WANDB_API_KEY=local-xxxx
wandb login
swanlab login -k xxx

# 重启 ray
bash restart_ray.sh

# 测试运行（1 步）
python train_sql_agent.py --ci-fast --model /path/to/Qwen3-0.6B

# 完整训练
python train_sql_agent.py \
  --llm-proxy \
  --model /path/to/Qwen2.5-7B-Instruct \
  --external-store-address http://xxx:45993
```

### 4. 测试 Agent

```bash
python sqlagent_test.py
```

## 项目结构

```
sql_agent/
├── sql_agent.py        # Agent 实现与奖励计算
├── tools.py            # 数据库查询工具
├── train_sql_agent.py  # 训练入口
├── restart_ray.sh      # 重启 ray 脚本
├── sqlagent_test.py    # 独立测试脚本
└── data/               # 训练数据
```

## 数据格式

训练数据为 Parquet 格式：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 样本唯一标识 |
| question | string | 用户问题 |
| answer | string | 标准答案 |

## 可用工具

`query_database_by_sql(sql: str)` - 执行 SQL 查询

根据自然语言问题生成 SQL 查询语句，查询药品或疾病数据库。

- **drugs_info**: 药品名称、成分、适应症、不良反应、禁忌症等
- **disease**: 疾病名称、临床表现、并发症、诊断方法、治疗方案等

## 奖励机制

1. **规则奖励** (0.1): 正确执行 SQL 查询即获得
2. **LLM 评估奖励** (0.0-1.0): 基于回答准确性、完整性打分

## 常见问题

**Q: CUDA 不可用？**
A: 尝试升级 CUDA 驱动：`sudo apt install nvidia-driver-590-server-open`

**Q: max_turns 不一致？**
A: 确保 `sql_agent.py` 中的 Agent 执行轮次与 verl 训练配置一致

**Q: Network is unreachable？**
A: 可暂时不使用 `AGL_MANAGED_STORE=0`，让框架使用默认 store
