#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/4 13:54
# @File  : myapi_search.py.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  : 搜索接口示例

import asyncio
import logging
from typing import List, Union, Dict, Any, Tuple

import aiohttp

logger = logging.getLogger(__name__)

async def search_document_db(
    keywords: Union[List[str], str],
    limit: int = 4,
    near_month: int = 60,
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    异步搜索医学数据库。
    参数:
        keywords: 关键词列表或空格分隔的字符串。关键词必须是英文。
        limit: 每个关键词返回的结果数量。
        near_month: 过滤最近几个月的数据。

    返回:
        contents: 匹配句子组成的格式化字符串。
        data: 合并后的结果项列表（根据ID去重），每个项包含标题、关键字、ID、匹配句子、URL和匹配关键词。
    """
    logger.info(f"查询系统评价关键词 (Async): {keywords}")
    url: str = "https://api.infox-med.com/search/home/keywords"
    category = 3  # 3 为综合搜索，不区分临床和指南
    timeout_s =30  #请求超时时间（秒）。
    doc_publish_types = []
    headers = {"Content-Type": "application/json"}
    keywords_string = " ".join(keywords)
    data_body = {
        "keywords": keywords_string,
        "category": category,
        "pageNum": 1,
        "pageSize": limit,
        "nearMonth": near_month,
        "docPublishTypes": doc_publish_types,
        "sort": "docPublishTime",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=timeout_s)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data_body, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()

        if result.get("msg") != "success":
            return []
        print("result:", result)
        query_result = result.get("data", {}).get("records", [])
    except Exception as e:
        logger.error(f"systematic query failed for kw {keywords}: {e}")
        return []

    results: List[Tuple[str, Dict[str, Any], str]] = []
    for hit in query_result:
        _id = hit.get("id", "")
        if not _id:
            continue

        pdf_name = hit.get("docTitle", "") or ""
        abstract = hit.get("docAbstractZh", "") or hit.get("docAbstract", "") or ""

        item_url = hit.get("qiniuUrl", "")
        item = {
            "title": pdf_name.title(),
            "id": _id,
            "docPublishTime": hit.get("docPublishTime", ""),
            "abstract": abstract,
            "url": item_url,
        }
        results.append(item)

    logger.info(f"搜索数据库完成，返回 {len(results)} 条结果")
    return results

async def main():
    contents = await search_document_db(["diabetes", "metformin"])
    print(contents)

if __name__ == "__main__":
    asyncio.run(main())
