#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/15 13:08
# @File  : check_env.py.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  : 检查环境是否安装完成

import sys
import torch
import importlib

print(f"=== 环境诊断开始 ===")
print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA Version: {torch.version.cuda}")

print("\n--- 1. 检测 Flash Attention ---")
try:
    import flash_attn

    print(f"✅ Flash Attention 导入成功. 版本: {flash_attn.__version__}")
except ImportError as e:
    print(f"❌ Flash Attention 导入失败: {e}")
except Exception as e:
    print(f"❌ Flash Attention 发生异常: {e}")

print("\n--- 2. 检测 vLLM (原生) ---")
try:
    import vllm
    from vllm import LLM

    print(f"✅ vLLM 原生导入成功. 版本: {vllm.__version__}")
    print(f"   LLM 类位置: {LLM}")
except ImportError as e:
    print(f"❌ vLLM 导入失败: {e}")
except Exception as e:
    print(f"❌ vLLM 运行时异常: {e}")

print("\n--- 3. 检测 verl 兼容层 (关键故障点) ---")
try:
    # 尝试手动导入 verl 的 vllm 包装层，捕获详细错误
    import verl.third_party.vllm

    print(f"ℹ️  verl.third_party.vllm 模块已加载")

    # 检查里面有什么
    attributes = dir(verl.third_party.vllm)
    print(f"   模块内含属性: {[a for a in attributes if not a.startswith('__')]}")

    if 'LLM' in attributes:
        print(f"✅ verl.third_party.vllm.LLM 存在")
    else:
        print(f"❌ 错误: verl.third_party.vllm 加载了，但里面没有 'LLM' 类！")
        print("   原因推测: verl 可能不识别 vllm 0.6.3，导致初始化逻辑被跳过。")

        # 打印文件位置，方便修改
        print(f"   文件路径: {verl.third_party.vllm.__file__}")

except ImportError as e:
    print(f"❌ verl.third_party.vllm 导入直接崩溃: {e}")
except Exception as e:
    print(f"❌ verl.third_party.vllm 发生其他异常: {e}")

print("\n=== 诊断结束 ===")