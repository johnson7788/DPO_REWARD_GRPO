#!/usr/bin/env python3
"""
将 Agent DPO 数据集从当前格式转换为标准 reward 模型训练格式
当前格式: {"messages": [...], "chosen_messages": [...], "rejected_messages": [...], "metadata": {...}}
标准格式: {"chosen": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}], "rejected": [...]}
"""

import json
import argparse
from pathlib import Path


def convert_agent_dpo_format(input_path: str, output_path: str) -> None:
    """转换 Agent DPO 数据集格式"""
    converted_data = []
    skipped_count = 0
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"警告: 第 {line_idx} 行无法解析，跳过")
                skipped_count += 1
                continue
            
            # 获取 chosen（messages）和 rejected 对话
            chosen_messages = data.get("messages", [])
            rejected_messages = data.get("rejected_messages", [])
            
            if not chosen_messages or not rejected_messages:
                print(f"警告: 第 {line_idx} 行缺少 chosen 或 rejected 消息，跳过")
                skipped_count += 1
                continue
            
            # 构建标准格式
            # 过滤掉 tool_call/tool_response 角色，只保留 user 和 assistant
            def filter_messages(messages):
                filtered = []
                for msg in messages:
                    role = msg.get("role", "")
                    content = msg.get("content", "")
                    if role in ["user", "assistant"] and content:
                        filtered.append({
                            "role": role,
                            "content": content
                        })
                return filtered
            
            chosen_filtered = filter_messages(chosen_messages)
            rejected_filtered = filter_messages(rejected_messages)
            
            if len(chosen_filtered) < 2 or len(rejected_filtered) < 2:
                print(f"警告: 第 {line_idx} 行过滤后消息不完整，跳过")
                skipped_count += 1
                continue
            
            converted_data.append({
                "chosen": chosen_filtered,
                "rejected": rejected_filtered
            })
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in converted_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"转换完成: {len(converted_data)} 条样本已保存到 {output_path}")
    if skipped_count > 0:
        print(f"跳过: {skipped_count} 条无效样本")


def main():
    parser = argparse.ArgumentParser(description="Agent DPO 数据集格式转换工具")
    parser.add_argument("-i", "--input", required=True, help="输入文件路径 (.jsonl)")
    parser.add_argument("-o", "--output", required=True, help="输出文件路径 (.jsonl)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return
    
    convert_agent_dpo_format(str(input_path), str(output_path))


if __name__ == "__main__":
    main()