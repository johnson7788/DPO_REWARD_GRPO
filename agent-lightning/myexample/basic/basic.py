#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/12/1 10:32
# @File  : basic.py.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  :

import asyncio
import agentlightning as agl
from agentlightning.store import InMemoryLightningStore

# 1）启动了LightningStore，Tracer执行追踪
async def main():
    # 1. 初始化存储和追踪器
    store = InMemoryLightningStore()
    tracer = agl.OtelTracer()

    # 2. 开始一次 rollout（训练回合）
    rollout = await store.start_rollout(input={"query": "2+2 等于多少？"})

    # 3. 追踪你的 agent 执行
    with tracer.lifespan(store):
        async with tracer.trace_context(
                "math_agent",
                store=store,
                rollout_id=rollout.rollout_id,
                attempt_id=rollout.attempt.attempt_id
        ) as tracer:
            # 你的 agent 逻辑
            with tracer.start_as_current_span("calculation"):
                result = {"answer": 4}  # 你的 agent 输出
                agl.emit_message("answer", result)
                agl.emit_reward(1.0)  # 完美得分！


if __name__ == "__main__":
    asyncio.run(main())