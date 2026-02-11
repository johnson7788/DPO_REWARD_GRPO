# Copyright (c) Microsoft. All rights reserved.

"""Examples to serve an LLM proxy for a vLLM server or an OpenAI service.
用于为 vLLM 服务器或 OpenAI 服务提供 LLM 代理的示例。

Usage: run one of the following commands to start a server.
用法：运行以下命令之一启动服务器。

```bash
python llm_proxy.py vllm Qwen/Qwen2.5-0.5B-Instruct
```

Use the following command to test the LLM proxy.
使用以下命令测试 LLM 代理。

```bash
python llm_proxy.py test Qwen/Qwen2.5-0.5B-Instruct
```

You can also test the OpenAI Proxy path (`OPENAI_API_KEY` environment variable is required).
您也可以测试 OpenAI 代理路径（需要设置 `OPENAI_API_KEY` 环境变量）。

```bash
dotenv run python llm_proxy.py openai gpt-4.1-mini
```
"""

import argparse
import asyncio
import os
from typing import Sequence, no_type_check

import aiohttp
from portpicker import pick_unused_port
from rich.console import Console
from vllm_server import vllm_server

import agentlightning as agl

console = Console()


async def serve_llm_proxy_with_vllm(model_name: str, store_port: int = 43887):
    """Serve an LLM proxy for a vLLM server.
    为 vLLM 服务器提供 LLM 代理服务。
    """
    # Create a store to store the traces
    # 创建一个存储来保存追踪信息
    store = agl.InMemoryLightningStore()
    store_server = agl.LightningStoreServer(store, "127.0.0.1", store_port)
    await store_server.start()

    # Create a vLLM server
    # 创建 vLLM 服务器
    vllm_port = pick_unused_port()
    with vllm_server(model_name, vllm_port) as vllm_endpoint:
        # Server is up.
        # 服务器已启动

        # Create an LLM proxy to guard the vLLM server and catch the traces
        # 创建一个 LLM 代理来保护 vLLM 服务器并捕获追踪信息
        llm_proxy = agl.LLMProxy(
            port=43886,
            model_list=[
                {
                    "model_name": model_name,
                    "litellm_params": {
                        "model": f"hosted_vllm/{model_name}",
                        "api_base": vllm_endpoint,
                    },
                }
            ],
            store=store_server,
        )

        try:
            await llm_proxy.start()

            # Wait forever
            # 永远等待
            await asyncio.sleep(float("inf"))

        finally:
            # Stop the LLM proxy and the store server
            # 停止 LLM 代理和存储服务器
            await llm_proxy.stop()
            await store_server.stop()


async def serve_llm_proxy_with_openai(model_name: str, store_port: int = 43887):
    """Serve an LLM proxy for an OpenAI server.
    为 OpenAI 服务器提供 LLM 代理服务。
    """
    # Create a store to store the traces
    # 创建一个存储来保存追踪信息
    store = agl.InMemoryLightningStore()
    store_server = agl.LightningStoreServer(store, "127.0.0.1", store_port)
    await store_server.start()

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")
        # OPENAI_API_KEY 环境变量未设置

    # Create an LLM proxy to guard the OpenAI server and catch the traces
    # 创建一个 LLM 代理来保护 OpenAI 服务器并捕获追踪信息
    llm_proxy = agl.LLMProxy(
        port=43886,
        model_list=[
            {
                "model_name": model_name,
                "litellm_params": {
                    "model": "openai/" + model_name,
                    # Must have OpenAI API key set in the environment variable
                    # 必须在环境变量中设置 OpenAI API 密钥
                },
            }
        ],
        store=store_server,
        callbacks=["opentelemetry"],
    )

    try:
        await llm_proxy.start()
        # Wait forever
        # 永远等待
        await asyncio.sleep(float("inf"))
    finally:
        # Stop the LLM proxy and the store server
        # 停止 LLM 代理和存储服务器
        await llm_proxy.stop()
        await store_server.stop()


async def test_llm_proxy(model_name: str, store_port: int = 43887):
    """Test the LLM proxy by sending a request to the proxy and checking the response.
    通过向代理发送请求并检查响应来测试 LLM 代理。

    We do it via aiohttp here. This can also be done with OpenAI client.
    我们在这里通过 aiohttp 来实现。这也可以通过 OpenAI 客户端完成。
    """
    # We first connect to the store server and start a rollout.
    # 我们首先连接到存储服务器并开始一次 rollout。
    store = agl.LightningStoreClient(f"http://localhost:{store_port}")
    rollout = await store.start_rollout(input={"origin": "test_llm_proxy"})

    # The chat completion URL is simply /v1/chat/completions under the namespace of current rollout and attempt.
    # This ensures the traces are properly put into the correct bucket.
    # 聊天完成 URL 是当前 rollout 和 attempt 命名空间下的 /v1/chat/completions。
    # 这确保了追踪信息被正确地放入正确的存储桶中。
    chat_completion_url = (
        f"http://localhost:43886/rollout/{rollout.rollout_id}/attempt/{rollout.attempt.attempt_id}/v1/chat/completions"
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(
            chat_completion_url,
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": "Hello, what's your name?"}],
            },
        ) as response:
            response_body = await response.json()
            console.print("Response body:", response_body)
            _verify_response_body(response_body, model_name)

    spans = await store.query_spans(rollout_id=rollout.rollout_id, attempt_id=rollout.attempt.attempt_id)
    for span in spans:
        console.print("Span:", span)
    _verify_span(spans)

    await store.close()


@no_type_check
def _verify_response_body(response_body: dict, model_name: str):
    """Expect Response body to be something like this:
    期望响应体如下所示：

    ```python
    {
        'id': 'chatcmpl-996a90a8678e4ed0a0d2724df2c0bba5',
        'created': 1763178218,
        'model': 'hosted_vllm/Qwen/Qwen2.5-0.5B-Instruct',
        'object': 'chat.completion',
        'choices': [
            {
                'finish_reason': 'stop',
                'index': 0,
                'message': {
                    'content': 'Hello! I am Qwen, an AI language model created by Alibaba Cloud. My name is Qwen, and I can assist you with
    various tasks and provide information on a wide range of topics. How may I help you today?',
                    'role': 'assistant'
                },
                'provider_specific_fields': {
                    'stop_reason': None,
                    'token_ids': [9707, 0, ...],
                }
            }
        ],
        'usage': {'completion_tokens': 48, 'prompt_tokens': 36, 'total_tokens': 84},
        'prompt_token_ids': [151644, 8948, ...],
    }
    ```
    """
    if "qwen" in model_name.lower():
        assert "qwen" in response_body["choices"][0]["message"]["content"].lower()
        assert (
            "provider_specific_fields" in response_body["choices"][0]
        ), "provider_specific_fields not found in response body"
        # provider_specific_fields 在响应体中未找到
        assert (
            "token_ids" in response_body["choices"][0]["provider_specific_fields"]
        ), "token_ids not found in response body"
        # token_ids 在响应体中未找到
        assert "prompt_token_ids" in response_body, "prompt_token_ids not found in response body"
        # prompt_token_ids 在响应体中未找到
    else:
        assert "chatgpt" in response_body["choices"][0]["message"]["content"].lower()


def _verify_span(spans: Sequence[agl.Span]):
    """Only a few spans are checked here.
    这里只检查少数几个 spans。

    `raw_gen_ai_request` span:

    ```python
    Span(
        rollout_id='ro-4c68a7e686a1',
        attempt_id='at-308eb814',
        sequence_id=1,
        name='raw_gen_ai_request',
        attributes={
            'llm.hosted_vllm.messages': '[{\'role\': \'user\', \'content\': "Hello, what\'s your name?"}]',
            'llm.hosted_vllm.extra_body': "{'return_token_ids': True}",
            'llm.hosted_vllm.choices': '... \'token_ids\': [40, 1079, 1207, 16948, ...',
            'llm.hosted_vllm.model': 'Qwen/Qwen2.5-0.5B-Instruct',
            'llm.hosted_vllm.prompt_token_ids': '[151644, 8948, ...]',
        },
        resource=OtelResource(
            attributes={
                'agentlightning.rollout_id': 'ro-4c68a7e686a1',
                'agentlightning.attempt_id': 'at-308eb814',
                'agentlightning.span_sequence_id': 1
            },
        )
    )
    ```
    """

    assert len(spans) > 1
    has_raw_gen_ai_request = False
    for span in spans:
        if span.name == "raw_gen_ai_request":
            has_raw_gen_ai_request = True
            if "llm.hosted_vllm.messages" in span.attributes:
                assert "return_token_ids" in span.attributes["llm.hosted_vllm.extra_body"]  # type: ignore
                assert "token_ids" in span.attributes["llm.hosted_vllm.choices"]  # type: ignore
                assert span.attributes["llm.hosted_vllm.prompt_token_ids"]
        assert "agentlightning.rollout_id" in span.resource.attributes
        assert "agentlightning.attempt_id" in span.resource.attributes
        assert "agentlightning.span_sequence_id" in span.resource.attributes

    assert has_raw_gen_ai_request, "raw_gen_ai_request span not found"
    # 未找到 raw_gen_ai_request span


if __name__ == "__main__":
    agl.setup_logging()
    parser = argparse.ArgumentParser(description="LLM Proxy runner")
    # LLM 代理运行器
    parser.add_argument(
        "mode",
        choices=["vllm", "openai", "test"],
        help="Which function to run",
        # 运行哪个函数
    )
    parser.add_argument("model", type=str, help="Model name to serve.")
    # 要服务的模型名称

    args = parser.parse_args()

    if args.mode == "vllm":
        asyncio.run(serve_llm_proxy_with_vllm(args.model))
    elif args.mode == "openai":
        asyncio.run(serve_llm_proxy_with_openai(args.model))
    elif args.mode == "test":
        asyncio.run(test_llm_proxy(args.model))