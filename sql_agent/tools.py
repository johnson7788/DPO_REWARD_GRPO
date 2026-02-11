#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/8 11:52
# @File  : mcp_search.py
# @Author: johnson
# @Desc : InfoX-Med 高级搜索接口 MCP 版 (带输入校验)

import asyncio
import logging
import re  # 引入正则进行格式校验
from enum import Enum
import aiohttp
import os
import time
from datetime import datetime
import requests
import dotenv
import json
import uuid
from itertools import combinations
from datetime import datetime, timezone, timedelta
from typing import List, Union, Dict, Any, Tuple, Optional
from agents import function_tool
from google.adk.tools import ToolContext
import sqlite3

dotenv.load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# 1. 定义常量和枚举 (保持不变)
# -----------------------------------------------------------------------------

DATABASE_PATH = "medical_data.db"

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class MockToolContext:
    """模拟 Google ADK 的 ToolContext，用于本地测试"""
    def __init__(self):
        # 初始化 state，模拟 ADK 中的 state 字典
        self.state = {
            "search_dbs": [],
            "latest_guideline_date": None
        }


async def execute_sql_query(sql: str) -> List[Dict[str, Any]]:
    """
    表结构如下：
    # drugs_info药品表
    [
        'id', 'med_name', 'med_name_initial', 'med_barcode', 'med_approval',
        'component', 'form', 'dosage', 'indication', 'adverse_reactions',
        'contraindications', 'precautions', 'company_name', 'description',
        'mechanism_action', 'cate_name', 'drug_interactions', 'storage',
        'pack', 'period', 'approve_code', 'status', 'created_at'
    ]

    # disease疾病表
    [
        'id', 'disease_name', 'overview', 'clinical_manif', 'complication',
        'epidemiology', 'examination', 'treatment', 'cause', 'diagnosis',
        'differ_diag', 'prevention', 'prognosis','create_at', 'update_at'
    ]
    Args:
        sql: SQL查询语句
    Returns:
        查询结果列表，每个元素是一个字典
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        # 获取列名
        columns = [description[0] for description in cursor.description]
        # 获取所有结果
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    except sqlite3.Error as e:
        logger.error(f"SQL执行错误: {e}")
        raise
    finally:
        conn.close()

MAX_TOTAL_LENGTH = 1000  # 返回结果的总字符上限，防止上下文溢出


def _truncate_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """截断记录，确保序列化后总长度不超过 MAX_TOTAL_LENGTH"""
    import json
    total = json.dumps(records, ensure_ascii=False)
    if len(total) <= MAX_TOTAL_LENGTH:
        return records

    # 逐条保留，直到总长度接近上限
    truncated = []
    current_len = 0
    for row in records:
        row_str = json.dumps(row, ensure_ascii=False)
        if current_len + len(row_str) > MAX_TOTAL_LENGTH:
            # 剩余空间不够放完整行，截断当前行的长文本字段
            remaining = MAX_TOTAL_LENGTH - current_len
            if remaining > 50:  # 至少留 50 字符才值得加
                new_row = {}
                budget = remaining - 20  # 预留 key 和格式字符
                for k, v in row.items():
                    v_str = str(v) if not isinstance(v, str) else v
                    if budget <= 0:
                        break
                    if len(v_str) > budget:
                        new_row[k] = v_str[:budget] + "..."
                        budget = 0
                    else:
                        new_row[k] = v
                        budget -= len(v_str)
                truncated.append(new_row)
            break
        truncated.append(row)
        current_len += len(row_str)
    return truncated


@function_tool
async def query_database_by_sql(sql: str) -> Dict[str, Any]:
    """
    根据sql查询数据库
    Args:
        sql: SQL查询语句
    Returns:
        包含查询结果的字典，包含 status 和 records 字段
    """
    try:
        records = await execute_sql_query(sql)
        records = _truncate_records(records)

        result = {
            "status": "success",
            "records": records,
            "count": len(records)
        }

        return result

    except Exception as e:
        logger.error(f"数据库查询失败: {e}")
        return {
            "status": "error",
            "error": str(e),
            "records": [],
            "count": 0
        }


if __name__ == "__main__":
    async def my_test_meta():
        # 创建一个假的工具上下文（只需包含 state）
        print("开始测试 query_database_by_sql ...")
        mock_context = MockToolContext()

        # 测试SQL查询
        test_sql = "SELECT * FROM drugs_info LIMIT 5"
        result = await execute_sql_query(test_sql)

        print("\n===== 搜索结果 =====")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    # 运行异步测试函数
    asyncio.run(my_test_meta())