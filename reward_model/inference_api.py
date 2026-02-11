#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2026/1/26 15:02
# @File  : inference.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  : 奖励模型的推理 FastAPI 服务


import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer

app = FastAPI(
    title="奖励模型推理服务",
    description="提供单个 response 评分和 pair 对比评分接口",
    version="1.0.0"
)

# 模型配置
device = "cuda:0"
model_name = "DPO_Reward"

# 全局变量存储模型和分词器
rm = None
tokenizer = None


def load_model():
    """加载模型和分词器"""
    global rm, tokenizer
    if rm is None or tokenizer is None:
        rm = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map=device,
            attn_implementation="flash_attention_2",
            num_labels=1,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)


def get_score(prompt: str, response: str) -> float:
    """计算单个 prompt-response 的奖励分数"""
    conv = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
    conv_formatted = tokenizer.apply_chat_template(conv, tokenize=False)
    if tokenizer.bos_token is not None and conv_formatted.startswith(tokenizer.bos_token):
        conv_formatted = conv_formatted[len(tokenizer.bos_token):]
    conv_tokenized = tokenizer(conv_formatted, return_tensors="pt").to(device)

    with torch.no_grad():
        score = rm(**conv_tokenized).logits[0][0].item()
    return score


# 请求模型
class ScoreRequest(BaseModel):
    prompt: str
    response: str


class ScorePairRequest(BaseModel):
    prompt: str
    chosen: str
    rejected: str


class ScoreResponse(BaseModel):
    score: float


class ScorePairResponse(BaseModel):
    chosen_score: float
    rejected_score: float
    preference: str
    score_diff: float


@app.on_event("startup")
async def startup_event():
    """启动时加载模型"""
    load_model()
    print(f"模型 {model_name} 已加载到设备 {device}")


@app.get("/")
async def root():
    """健康检查"""
    return {"status": "ok", "message": "奖励模型推理服务运行中"}


@app.post("/score", response_model=ScoreResponse)
async def score_single(request: ScoreRequest):
    """
    对单个 prompt 和 response 进行评分

    - **prompt**: 用户输入的 prompt
    - **response**: 模型生成的 response
    """
    print(f"正在计算 \n{request.prompt} 和 \n{request.response} 的分数")
    score = get_score(request.prompt, request.response)
    return {"score": score}


@app.post("/score-pair", response_model=ScorePairResponse)
async def score_pair(request: ScorePairRequest):
    """
    对比两个 response 的分数 (chosen vs rejected)

    - **prompt**: 用户输入的 prompt
    - **chosen**: 较好的 response
    - **rejected**: 较差的 response
    """
    chosen_score = get_score(request.prompt, request.chosen)
    rejected_score = get_score(request.prompt, request.rejected)

    preference = "chosen" if chosen_score > rejected_score else "rejected"
    score_diff = chosen_score - rejected_score

    return {
        "chosen_score": chosen_score,
        "rejected_score": rejected_score,
        "preference": preference,
        "score_diff": score_diff
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8400)
