#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/4 15:22
# @File  : build_data.py
# @Author: johnson
# @Desc  : 构建医疗领域的搜索数据集

import asyncio
import os
import uuid
import json
import random
import pandas as pd
from typing import List, Dict, Optional
from openai import OpenAI
import logging

# 引入你的搜索工具
# 请确保 search_systematic_db 返回的结果中包含 title 和 match_sentence (作为摘要)
from search_example import search_systematic_db

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ================= 配置区域 =================
# 输出文件路径
OUTPUT_TRAIN_FILE = "my_custom_train.parquet"
OUTPUT_DEV_FILE = "my_custom_dev.parquet"

# 生成数据的目标数量
TARGET_TRAIN_COUNT = 100
TARGET_DEV_COUNT = 10

# LLM 配置
LLM_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
LLM_BASE_URL = "https://api.openai.com/v1"
LLM_MODEL = "gpt-4o"

# 种子关键词列表 (已修改为中文，适配中文医疗检索)
SEED_KEYWORDS = [
    "糖尿病", "肾细胞癌", "二甲双胍", "高血压",
    "肺癌", "免疫疗法", "阿司匹林", "新冠肺炎",
    "心力衰竭", "肥胖症", "化疗", "哮喘",
    "中风", "阿尔茨海默病", "抑郁症", "贫血",
    "冠心病", "乙肝", "骨质疏松", "胃癌"
]
# ===========================================

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)


def generate_qa_from_content(abstract_text: str, source_title: str) -> Optional[Dict]:
    """
    使用 LLM 基于【标题】和【摘要】反向构建 Question 和 Answer。
    Prompt 已修改为中文，且强调只基于摘要信息。
    """
    prompt = f"""
    你是一位专业的医学数据标注专家。我将提供一篇医学文献的【标题】和【摘要】（不包含正文）。
    你的任务是完全基于这有限的摘要信息，构建一个高质量的问答对（Question-Answer Pair），用于训练 RAG（检索增强生成）模型。

    **输入信息：**
    文章标题: {source_title}
    文章摘要:
    {abstract_text[:3000]} (如果过长已截断)

    **生成要求：**
    1. **问题 (Question)**: 必须是一个复杂问题，需要根据摘要中的信息进行推理或检索才能回答。问题应模拟真实医生或患者的查询语气。
    2. **答案 (Answer)**: 答案必须简练且精准（如：实体名、日期、判断是/否、或简短的解释短语），内容必须直接来源于摘要，**不要编造摘要中不存在的信息**。
    3. **语言**: 问题和答案必须使用**中文**。
    4. **格式**: 必须输出合法的 JSON 格式。

    **输出 JSON 格式示例：**
    {{
        "question": "根据摘要，这种药物主要治疗什么疾病？",
        "answer": "2型糖尿病"
    }}
    """

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logger.error(f"LLM 生成失败: {e}")
        return None


async def build_dataset(target_count: int, filename: str):
    data_rows = []
    current_count = 0

    logger.info(f"开始构建数据集: {filename}, 目标数量: {target_count}")

    while current_count < target_count:
        # 1. 随机选择关键词
        keyword = random.choice(SEED_KEYWORDS)

        # 30% 的概率组合两个关键词，增加搜索特异性
        if random.random() > 0.7:
            keyword += " " + random.choice(SEED_KEYWORDS)

        logger.info(f"正在搜索关键词: {keyword}")

        # 2. 调用你的搜索接口
        try:
            # 这里的 limit=2 表示每次搜索取前2个结果
            # 假设 search_systematic_db 已经优化为只返回 title 和 match_sentence(abstract) 以加快速度
            contents_str, records = await search_systematic_db([keyword], limit=2)

            if not records:
                logger.warning(f"关键词 {keyword} 未搜索到结果，跳过")
                continue

            # 3. 处理搜索结果
            for record in records:
                if current_count >= target_count:
                    break

                # 提取摘要和标题 (根据你的描述，这里不需要正文)
                # 假设 record['match_sentence'] 存放的是摘要或相关片段
                abstract = record.get("match_sentence", "")
                title = record.get("title", "无标题")

                # 过滤掉太短的内容 (例如少于30个字可能无法生成有效问答)
                if len(abstract) < 30:
                    continue

                # 4. LLM 生成 QA
                qa_pair = generate_qa_from_content(abstract, title)

                if qa_pair and qa_pair.get("question") and qa_pair.get("answer"):
                    # 构建数据行
                    row = {
                        "id": f"{uuid.uuid4().hex[:8]}",
                        "question": qa_pair["question"],
                        "answer": qa_pair["answer"],
                        # 可选：保留原始文本作为 context，方便后续训练调试
                        # "context": f"标题：{title}\n摘要：{abstract}"
                    }
                    data_rows.append(row)
                    current_count += 1
                    logger.info(
                        f"[{current_count}/{target_count}] 生成成功: {row['question'][:30]}... -> {row['answer']}")
                else:
                    logger.warning("QA 生成失败或格式错误")

        except Exception as e:
            logger.error(f"处理关键词 {keyword} 时发生错误: {e}")
            await asyncio.sleep(1)  # 避免请求过快，简单限流

    # 5. 保存为 Parquet 文件
    if data_rows:
        df = pd.read_json(json.dumps(data_rows))
        # 确保列顺序
        df = df[["id", "question", "answer"]]

        # 打印统计信息
        print("\n" + "=" * 30)
        print(f"数据预览 ({filename}):")
        print(df.head())
        print(f"数据形状: {df.shape}")
        print("=" * 30 + "\n")

        df.to_parquet(filename, index=False)
        logger.info(f"文件已保存至: {filename}")
    else:
        logger.error("未生成任何数据！")


async def main():
    # 检查 data 目录是否存在
    if not os.path.exists("data"):
        os.makedirs("data")

    # 构建验证集 (Dev Set) - 数量少，用于评估
    await build_dataset(TARGET_DEV_COUNT, OUTPUT_DEV_FILE)

    # 构建训练集 (Train Set) - 数量多，用于训练
    await build_dataset(TARGET_TRAIN_COUNT, OUTPUT_TRAIN_FILE)


if __name__ == "__main__":
    asyncio.run(main())