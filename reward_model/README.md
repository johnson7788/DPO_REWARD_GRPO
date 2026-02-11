# 使用trl训练奖励模型
# Full training:
python examples/scripts/reward_modeling.py \
    --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
    --dataset_name trl-lib/ultrafeedback_binarized \
    --output_dir Qwen2-0.5B-Reward \
    --per_device_train_batch_size 8 \
    --num_train_epochs 1 \
    --gradient_checkpointing True \
    --learning_rate 1.0e-5 \
    --eval_strategy steps \
    --eval_steps 50 \
    --max_length 2048

LoRA:
python examples/scripts/reward_modeling.py \
    --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
    --dataset_name trl-lib/ultrafeedback_binarized \
    --output_dir Qwen2-0.5B-Reward-LoRA \
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


# 数据集格式
参考： https://huggingface.co/datasets/trl-lib/ultrafeedback_binarized/viewer/default/train?row=0&views%5B%5D=train&sql=--+The+SQL+console+is+powered+by+DuckDB+WASM+and+runs+entirely+in+the+browser.%0A--+Get+started+by+typing+a+query+or+selecting+a+view+from+the+options+below.%0ASELECT+*+FROM+train+LIMIT+1%3B
数据集每条样本包含 2 个字段：
{"chosen":chosen的message格式, "rejected":rejected的message格式}
chosen: list[ {role, content}, ... ]（一段对话消息序列，通常是 user→assistant）
rejected: list[ {role, content}, ... ]（同一个 user 提示下的另一段 assistant 回复）

# 转换数据集
python convert_dpo_format.py --input=dpo_answer.jsonl --output=dpo_answer_converted.jsonl

# 训练奖励模型
export WANDB_BASE_URL=xxxx
export WANDB_API_KEY=local-
wandb login
swanlab login -k xxx

# 多卡训练，否则会报CUDA out of memory， 4096长度就OOM
CUDA_VISIBLE_DEVICES=0,1 \
accelerate launch --num_processes 2 --mixed_precision bf16 \
reward_modeling.py \
  --dataset_name ./dpo_answer_converted.jsonl \
  --model_name_or_path /workspace/post_train/post_train/Qwen2.5-7B-Instruct \
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

显存占用
root@10-60-167-56:~# nvidia-smi
Fri Jan 23 16:09:37 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.153.02             Driver Version: 570.153.02     CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4090        On  |   00000000:00:03.0 Off |                  Off |
|100%   79C    P2            402W /  450W |   42374MiB /  49140MiB |     68%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   1  NVIDIA GeForce RTX 4090        On  |   00000000:00:04.0 Off |                  Off |
|100%   77C    P2            423W /  450W |   40518MiB /  49140MiB |     84%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

# 合并模型
swift export \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapters ./reward_model_output \
  --merge_lora true \
  --output_dir modelzhang/DPO_Reward  


## 奖励模型的测试和API
python inference.py   # 测试

python inference_api.py  # 启动API
# 单个评分
curl -X POST "http://localhost:8400/score" \
 -H "Content-Type: application/json" \
 -d '{"prompt": "对比胆囊息肉和巨乳头性结膜炎的临床表现？有什么不同？", "response": "胆囊息肉和巨乳头性结膜炎是两种完全不同的疾病，分别属于消化系统和眼部疾病。它们在临床上的表现有着明显的差异，下面我将为您详细对比这两种疾病的临床表现。胆囊息肉是一种胆囊黏膜上的良性肿瘤，通常不会引起明显的症状，但部分患者可能会出现腹痛、消化不良、黄疸和发热等表现。巨乳头性结膜炎是一种常见的眼部炎症，通常与长期使用隐形眼镜或眼部过敏有关，表现为眼睛红肿、异物感、分泌物增多、畏光，严重时可出现视力模糊。胆囊息肉通过腹部超声检查发现，而巨乳头性结膜炎需要通过眼部检查诊断，出现相关症状建议及时就医。"}'

# Pair 对比评分
curl -X POST "http://localhost:8400/score-pair" \
 -H "Content-Type: application/json" \
 -d '{"prompt": "你的问题", "chosen": "好的回答", "rejected": "差的回答"}'