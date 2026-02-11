# 奖励模型训练

基于 TRL 库训练奖励模型（Reward Model），用于评估和排序模型 responses。

## 特性

- 支持全量训练和 LoRA 微调
- 支持多卡分布式训练
- 提供评分 API 服务
- 支持 Pair 对比评分

## 依赖安装

```bash
cd agent-lightning
uv pip install --system --no-cache-dir -e .[dev,agent,apo] \
  fastmcp==2.14.1 openai-agents==0.6.3 verl==0.5.0
```

## 快速开始

### 1. 数据格式

训练数据每条样本包含 2 个字段：

```python
{
  "chosen": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
  "rejected": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
}
```

`chosen` 和 `rejected` 是同一 user prompt 下的两个不同 assistant 回复。

### 2. 数据转换（如需要）

```bash
python convert_dpo_format.py --input=dpo_answer.jsonl --output=dpo_answer_converted.jsonl
```

### 3. 训练

**全量训练**：

```bash
python examples/scripts/reward_modeling.py \
  --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --output_dir ./reward_model_output \
  --per_device_train_batch_size 8 \
  --num_train_epochs 1 \
  --gradient_checkpointing True \
  --learning_rate 1.0e-5 \
  --eval_strategy steps \
  --eval_steps 50 \
  --max_length 2048
```

**LoRA 训练**：

```bash
python examples/scripts/reward_modeling.py \
  --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --output_dir ./reward_model_output \
  --per_device_train_batch_size 8 \
  --num_train_epochs 1 \
  --gradient_checkpointing True \
  --learning_rate 1.0e-4 \
  --eval_strategy steps \
  --eval_steps 50 \
  --max_length 2048 \
  --use_peft \
  --lora_task_type SEQ_CLS \
  --lora_r 32 \
  --lora_alpha 16
```

**多卡训练**（7B 模型）：

```bash
export WANDB_BASE_URL=xxxx
export WANDB_API_KEY=local-
wandb login
swanlab login -k xxx

CUDA_VISIBLE_DEVICES=0,1 \
accelerate launch --num_processes 2 --mixed_precision bf16 \
reward_modeling.py \
  --dataset_name ./dpo_answer_converted.jsonl \
  --model_name_or_path /path/to/Qwen2.5-7B-Instruct \
  --output_dir ./reward_model_output \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 8 \
  --num_train_epochs 3 \
  --max_length 3000 \
  --learning_rate 1e-6 \
  --use_peft \
  --lora_task_type SEQ_CLS \
  --lora_r 16 --lora_alpha 32 --lora_dropout 0.05 \
  --load_in_8bit
```

### 4. 合并 LoRA 模型

```bash
swift export \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapters ./reward_model_output \
  --merge_lora true \
  --output_dir ./DPO_Reward
```

## 测试与推理

### 本地测试

```bash
python inference.py
```

### 启动 API 服务

```bash
python inference_api.py
```

### API 调用

**单个评分**：

```bash
curl -X POST "http://localhost:8400/score" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你的问题", "response": "回答内容"}'
```

**Pair 对比评分**：

```bash
curl -X POST "http://localhost:8400/score-pair" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你的问题", "chosen": "好的回答", "rejected": "差的回答"}'
```

## 项目结构

```
reward_model/
├── reward_modeling.py       # 训练脚本
├── inference.py             # 本地推理测试
├── inference_api.py         # API 服务
├── convert_dpo_format.py    # 数据格式转换
├── convert_agent_dpo_format.py
├── dpo_answer_converted.jsonl
├── filter_dpo_dataset.jsonl
└── requirements.txt
```

## 显存参考

| 模型 | 配置 | 显存占用 |
|------|------|----------|
| Qwen2.5-7B | 2x RTX 4090, bf16, batch=1 | ~40GB/卡 |
