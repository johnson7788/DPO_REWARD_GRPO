#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/3 14:46
# @File  : check_data_file.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  : 检查数据文件


import os
import pandas as pd

def summarize_parquet(path, n_sample=5):
    print("=" * 80)
    print(f"文件: {path}")

    if not os.path.exists(path):
        print("❌ 文件未找到。")
        return

    # 读取 parquet
    try:
        df = pd.read_parquet(path)
    except Exception as e:
        print(f"❌ 读取 parquet 失败: {e}")
        return

    # 基本信息
    print(f"\n[基本信息]")
    print(f"形状 (行数, 列数): {df.shape}")
    print(f"列名 ({len(df.columns)}): {list(df.columns)}")

    print("\n数据类型:")
    # 用 to_string 避免过长被截断
    print(df.dtypes.to_string())

    # 缺失值统计
    print("\n各列缺失值统计:")
    miss = df.isna().sum()
    miss_rate = (miss / len(df) * 100).round(2) if len(df) else miss
    miss_df = pd.DataFrame({"缺失数量": miss, "缺失率_%": miss_rate})
    print(miss_df.to_string())

    # 数值列统计
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) > 0:
        print("\n数值列统计描述:")
        print(df[num_cols].describe().to_string())
    else:
        print("\n数值列统计描述: (无)")

    # 类别/文本列的简单统计
    cat_cols = df.select_dtypes(include=["object", "string", "category", "bool"]).columns
    if len(cat_cols) > 0:
        print("\n分类/文本列概览 (前5个最频繁的值):")
        for c in cat_cols:
            print(f"\n- 列名: {c}")
            vc = df[c].value_counts(dropna=False).head(5)
            print(vc.to_string())
    else:
        print("\n分类/文本列概览: (无)")

    # 示例数据
    print(f"\n[示例行: 前{min(n_sample, len(df))}行]")
    print(df.head(n_sample).to_string(index=False))

    print(f"\n[随机示例行 ({min(n_sample, len(df))})]")
    if len(df) > 0:
        print(df.sample(min(n_sample, len(df)), random_state=42).to_string(index=False))
    else:
        print("(空数据框)")
    # ==========================================
    # 新增：打印一条完整数据（垂直视图）
    # ==========================================
    print(f"\n[单条完整数据详细视图 (第一行)]")
    if len(df) > 0:
        # 获取第一行作为 Series，to_string() 会将其垂直打印，方便查看所有字段
        print(df.iloc[0].to_string())
    else:
        print("(空数据框)")


def check_empty_rows(path):
    df = pd.read_parquet(path)

    text_cols = [c for c in df.columns]
    print("text-like columns:", text_cols)

    for col in text_cols:
        print(f"\n检查列: {col}")
        empty_mask = df[col].isna() | (df[col].astype(str).str.strip() == "")
        empty_count = empty_mask.sum()
        print("空行数量:", empty_count)
        if empty_count > 0:
            print("⚠️  警告: 发现空行!")
        print(df[empty_mask].head())

def main():
    # 获取当前目录下所有以 .parquet 结尾的文件
    files = [f for f in os.listdir('.') if f.endswith('.parquet')]
    for f in files:
        summarize_parquet(f, n_sample=5)
        check_empty_rows(path=f)

if __name__ == "__main__":
    main()