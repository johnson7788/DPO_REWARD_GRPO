# 最小组件展示

`examples/minimal` 提供了小型程序，用于演示单个 Agent-lightning 构建块在隔离环境中的行为。

每个模块都在其模块级文档字符串中记录了其 CLI 使用方法。在将相同组件集成到更大的系统中时，请将此目录作为参考。

## 包含哪些内容？

| 组件 | 演示文件 | 亮点 |
| --- | --- | --- |
| LightningStore + OTLP 摄取 | [write_traces.py](file:///Users/admin/git/agent-lightning/examples/minimal/write_traces.py) | 展示了 [OtelTracer](file:///Users/admin/git/agent-lightning/agentlightning/tracer/otel.py#L29-L193) 和 [AgentOpsTracer](file:///Users/admin/git/agent-lightning/agentlightning/tracer/agentops.py#L30-L230) 如何开启 rollout、发出 span，并可选择将它们转发到远程存储客户端。 |
| LLM 代理 | [llm_proxy.py](file:///Users/admin/git/agent-lightning/agentlightning/llm_proxy.py) | 使用 [LLMProxy](file:///Users/admin/git/agent-lightning/agentlightning/llm_proxy.py#L987-L1346) 对 OpenAI 或本地 vLLM 部署进行保护，展示了请求如何通过 `/rollout/<id>/attempt/<id>` 命名空间路由并被捕获到存储中。 |
| vLLM 生命周期 | [vllm_server.py](file:///Users/admin/git/agent-lightning/examples/minimal/vllm_server.py) | 最小的上下文管理器，用于启动 `vllm serve` 进程，监控就绪状态，并安全地终止进程。 |

所有运行时指令（CLI 参数、必需的环境变量等）都直接嵌入在每个脚本的顶级文档字符串中，因此源代码保持自我文档化。

对于成熟的训练工作流或多组件实验，请浏览 `examples/` 下的其他子目录。这个 `minimal` 文件夹刻意将每个演示聚焦于单个组件，以便您可以独立理解和测试它们。


#  write_traces.py
[write_traces.py](write_traces.py)
会往rollouts中写入1条记录，同时往Traces中写入1条记录

# vllm_server.py 启动vllm

# llm_proxy.py
它是一个“把 vLLM 或 OpenAI 包一层代理（LLMProxy）并把每次调用的 trace/span 记录到 LightningStore 里”的可运行示例。