#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/23 16:20
# @File  : create_question_real_data.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  :

import json
import uuid
import pandas as pd
import os
import logging

OUTPUT_DIR = "data"
TRAIN_FILE = "train.parquet"
DEV_FILE = "val.parquet"

RAW_FILE = "./data/qa_dataset.jsonl"  # 你的真实数据文件路径

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RealDataBuilder")


def load_real_questions(jsonl_path: str):
    """
    从 qa_dataset.jsonl 里读取真实问题和答案

    每行格式类似：
    {"qid": "...", "question": "...", "ground_truth": "...", ...}
    """
    data = []
    skipped_question_empty = 0
    skipped_answer_empty = 0
    skipped_missing_fields = 0

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                logger.warning(f"跳过无法解析的行 {line_idx}: {line[:100]} ...")
                continue

            # 验证 question 字段
            question = obj.get("question", "").strip() if obj.get("question") else ""
            if not question:
                skipped_question_empty += 1
                continue

            # 验证 ground_truth (answer) 字段
            answer = obj.get("ground_truth", "").strip() if obj.get("ground_truth") else ""
            if not answer:
                skipped_answer_empty += 1
                logger.warning(f"跳过第 {line_idx} 行: answer (ground_truth) 为空, question: {question[:50]}...")
                continue

            # 保留 qid 作为原始标识
            qid = obj.get("qid", None)
            task_type = obj.get("task_type", None)

            data.append({
                "id": f"real_nav_{uuid.uuid4().hex[:8]}",
                "question": question,
                "answer": answer,
                "qid": qid,
                "task_type": task_type
            })

    logger.info(f"✅ 从 {jsonl_path} 读取到 {len(data)} 条有效问题")
    if skipped_question_empty > 0:
        logger.warning(f"⚠️ 跳过 {skipped_question_empty} 条空 question 记录")
    if skipped_answer_empty > 0:
        logger.warning(f"⚠️ 跳过 {skipped_answer_empty} 条空 answer (ground_truth) 记录")
    if skipped_missing_fields > 0:
        logger.warning(f"⚠️ 跳过 {skipped_missing_fields} 条缺失字段的记录")

    return data


def build_and_save_dataset():
    # 1. 加载真实问题
    data_list = load_real_questions(RAW_FILE)
    if not data_list:
        logger.warning("没有有效数据，终止。")
        return

    # 2. 转成 DataFrame
    df = pd.DataFrame(data_list)

    # 保留 id, question, answer, qid, task_type
    df = df[["id", "question", "answer", "qid", "task_type"]]

    # 3. Train / Val 划分（9:1）
    if len(df) > 10:
        df_val = df.sample(frac=0.1, random_state=42)
        df_train = df.drop(df_val.index)
    else:
        df_train = df
        df_val = df.iloc[0:0]

    # 4. 保存
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    train_path = os.path.join(OUTPUT_DIR, TRAIN_FILE)
    val_path = os.path.join(OUTPUT_DIR, DEV_FILE)

    df_train.to_parquet(train_path, index=False)
    df_val.to_parquet(val_path, index=False)

    logger.info(f"✅ 保存训练集: {len(df_train)} 条 -> {train_path}")
    logger.info(f"✅ 保存验证集: {len(df_val)} 条 -> {val_path}")


if __name__ == "__main__":
    build_and_save_dataset()
