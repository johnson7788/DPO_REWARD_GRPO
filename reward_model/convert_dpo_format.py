#!/usr/bin/env python3
"""
将DPO数据集从当前格式转换为标准格式
当前格式: {"prompt": "...", "chosen": "...", "rejected": "..."}
标准格式: {"chosen": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}], "rejected": [...]}
"""

import json
import argparse
from pathlib import Path


def convert_dpo_format(input_path: str, output_path: str) -> None:
    """转换DPO数据集格式"""
    converted_data = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"警告: 跳过无法解析的行")
                continue
            
            prompt = data.get("prompt", "")
            chosen_answer = data.get("chosen", "")
            rejected_answer = data.get("rejected", "")
            
            # 构建标准格式
            # chosen: user的prompt + assistant的chosen回答
            chosen_messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": chosen_answer}
            ]
            
            # rejected: user的prompt + assistant的rejected回答
            rejected_messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": rejected_answer}
            ]
            
            converted_data.append({
                "chosen": chosen_messages,
                "rejected": rejected_messages
            })
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in converted_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"转换完成: {len(converted_data)} 条样本已保存到 {output_path}")


def main():
    parser = argparse.ArgumentParser(description="DPO数据集格式转换工具")
    parser.add_argument("-i", "--input", required=True, help="输入文件路径 (.jsonl)")
    parser.add_argument("-o", "--output", required=True, help="输出文件路径 (.jsonl)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return
    
    convert_dpo_format(str(input_path), str(output_path))


if __name__ == "__main__":
    main()
