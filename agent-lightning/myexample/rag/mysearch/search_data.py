#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/8 11:52
# @File  : search_data.py
# @Author: johnson
# @Desc    : InfoX-Med 高级搜索接口完整实现

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional, Union
from enum import Enum

import aiohttp

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# 1. 定义常量和枚举 (方便调用，防止拼写错误)
# -----------------------------------------------------------------------------

class SearchField(Enum):
    TITLE = "Title"
    MESH_TERMS = "MeSH Terms"
    TITLE_ABSTRACT = "Title/Abstract"
    AUTHOR = "Author"
    ABSTRACT = "Abstract"
    PUBLICATION_DATE = "Publication Date"
    JOURNAL = "Journal"
    AFFILIATION = "Affiliation"
    FIRST_AUTHOR = "First Author"
    LAST_AUTHOR = "Last Author"
    FIRST_AUTHOR_AFFILIATION = "First Author Affiliation"
    LAST_AUTHOR_AFFILIATION = "Last Author Affiliation"
    CORPORATE_AUTHOR = "Corporate Author"


class LogicOp(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


# -----------------------------------------------------------------------------
# 2. 查询构造器 (处理复杂的括号和逻辑关系)
# -----------------------------------------------------------------------------

class QueryBuilder:
    """
    用于构建如 (("A"[Title]) AND ("B"[Abstract])) 的查询字符串
    """

    def __init__(self):
        self.parts = []

    @staticmethod
    def term(value: str, field: Union[SearchField, str] = None) -> str:
        """创建一个带标签的术语，例如: "吴"[Author]"""
        clean_val = value.replace('"', '\\"')  # 简单转义
        field_str = field.value if isinstance(field, SearchField) else field
        if field_str:
            return f'"{clean_val}"[{field_str}]'
        return f'"{clean_val}"'

    @staticmethod
    def combine(items: List[str], operator: LogicOp = LogicOp.AND) -> str:
        """将多个部分用逻辑符连接，并加上括号"""
        if not items:
            return ""
        if len(items) == 1:
            return items[0]

        op_str = f" {operator.value} "
        # 核心：用括号包裹整体逻辑
        combined = op_str.join(items)
        return f"({combined})"


# -----------------------------------------------------------------------------
# 3. 筛选构造器 (处理 @@AND$$ 格式)
# -----------------------------------------------------------------------------

class FilterBuilder:
    """
    用于构建 filter 字符串，例如: @@AND$$doc_if$$10$$20...
    """

    def __init__(self):
        self.filters = []

    def add_range(self, key: str, start: Any, end: Any):
        """添加范围筛选，如日期或IF值: key$$start$$end"""
        self.filters.append(f"{key}$${start}$${end}")
        return self

    def add_value(self, key: str, value: Any):
        """添加单值筛选: key$$value"""
        self.filters.append(f"{key}$${value}")
        return self

    def add_list(self, key: str, values: List[Any]):
        """
        添加多值筛选。
        根据curl示例，多个Mesh Terms是重复key的:
        @@AND$$doc_mesh_terms$$Humans@@AND$$doc_mesh_terms$$Female
        """
        for v in values:
            self.filters.append(f"{key}$${v}")
        return self

    def build(self) -> str:
        if not self.filters:
            return ""
        # 必须以 @@AND 开头 (根据 curl 示例)
        return "@@AND$$" + "@@AND$$".join(self.filters)


# -----------------------------------------------------------------------------
# 4. 核心搜索函数
# -----------------------------------------------------------------------------

async def search_infox_advanced(
        query_string: str,
        filter_string: str = "",
        page_num: int = 1,
        page_size: int = 10,
        sort_field: str = "docPublishTime",
        token: str = "",  # 必须提供 Token
        timeout_s: int = 30
) -> Dict[str, Any]:
    """
    执行高级搜索
    """
    url = "https://api.infox-med.com/search/home/keywords"

    # 构建完全符合 Curl 的请求体
    payload = {
        "type": "doc",
        "pageNum": page_num,
        "pageSize": page_size,
        "keywords": query_string,
        "filter": filter_string,
        "sort": sort_field
    }

    # 请求头 (尽量模拟浏览器和 Curl 中的关键字段)
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Origin": "https://infox-med.com",
        "token": token  # 鉴权 Token
    }

    logger.info(f"正在请求 API...")
    logger.info(f"Keywords: {query_string}")
    logger.info(f"Filter:   {filter_string}")

    try:
        timeout = aiohttp.ClientTimeout(total=timeout_s)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()

                if result.get("code") != 200 and result.get("msg") != "success":
                    logger.warning(f"API 返回非成功状态: {result.get('msg')}")

                return result

    except Exception as e:
        logger.error(f"请求失败: {e}")
        return {}


# -----------------------------------------------------------------------------
# 5. 使用示例 (Main)
# -----------------------------------------------------------------------------

async def main():
    # 你的 Token (从 curl 中获取，实际使用时可能需要动态获取或配置)
    my_token = "e3f62087e126439aa12ad4637cf4f12b|1106970"

    # ==========================
    # 步骤 1: 构建复杂的 Keywords
    # 目标: ((("吴"[Author]) AND ("Hospital to Home Transition"[MeSH Terms])) AND ("疾病"[Abstract])) AND ("Last"[Last Author Affiliation])
    # ==========================

    # 1.1 构建各个子条件
    q1 = QueryBuilder.term("王", SearchField.AUTHOR)
    q2 = QueryBuilder.term("Hospital to Home Transition", SearchField.MESH_TERMS)
    q3 = QueryBuilder.term("疾病", SearchField.ABSTRACT)
    q4 = QueryBuilder.term("Last", SearchField.LAST_AUTHOR_AFFILIATION)
    q5 = QueryBuilder.term("2134", SearchField.LAST_AUTHOR_AFFILIATION)

    # 1.2 组合逻辑 (可以无限嵌套)
    # (q1 AND q2)
    part_a = QueryBuilder.combine([q1, q2], LogicOp.AND)

    # ((q1 AND q2) AND q3)
    part_b = QueryBuilder.combine([part_a, q3], LogicOp.AND)

    # (((q1 AND q2) AND q3) AND q4)
    part_c = QueryBuilder.combine([part_b, q4], LogicOp.AND)
    #
    # 最终加上 q5
    final_query = QueryBuilder.combine([part_c, q5], LogicOp.AND)
    #
    # ==========================
    # 步骤 2: 构建 Filter 字符串
    # 目标: 日期范围, 只有摘要, IF 10-20, MeSH Terms (Human, Female, Adult)
    # ==========================

    # 计算最近5年的日期 (模拟 curl 中的 2020-12-08 到 2025-12-08)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

    fb = FilterBuilder()

    # 2.1 添加日期范围
    fb.add_range("doc_publish_time", start_date, end_date)

    # 2.2 添加是否有摘要/全文 (Curl中是 qiniu_url$$0)
    # fb.add_value("qiniu_url", "0")

    # 2.3 添加影响因子范围 (IF 10-20)
    # fb.add_range("doc_if", 10, 20)

    # 2.4 添加 MeSH 筛选 (多选)
    # fb.add_list("doc_mesh_terms", ["Humans", "Female", "Adult"])

    # 2.5 (可选) 添加文档类型筛选
    # 注意：虽然 curl filter 字符串里没明确看到 doc_publish_type，但通常是在 filter 里
    # 如果接口支持，可以这样加：
    # fb.add_list("doc_publish_type", ["Meta-Analysis", "Randomized Controlled Trial"])

    final_filter = fb.build()

    # ==========================
    # 步骤 3: 发起请求
    # ==========================
    result = await search_infox_advanced(
        query_string=part_a,
        filter_string=final_filter,
        token=my_token,
        page_size=10
    )

    # ==========================
    # 步骤 4: 处理结果
    # ==========================
    data = result.get("data", {})
    records = data.get("records", [])
    total = data.get("total", 0)

    print(f"\n搜索完成! 找到总数: {total}")
    print("-" * 50)

    for idx, item in enumerate(records):
        title = item.get("docTitle", "No Title")
        journal = item.get("docJournal", "No Journal")
        pub_date = item.get("docPublishTime", "")
        # 获取匹配的高亮片段 (通常在 highlight 字段或 abstract 中)
        print(f"[{idx + 1}] {title}")
        print(f"    Journal: {journal} | Date: {pub_date}")
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())