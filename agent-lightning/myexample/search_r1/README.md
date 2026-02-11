# Search-R1 示例

## 概述

本示例在 Agent Lightning 中实现了 **Search R1**。它还作为 **无框架代理训练管道** 的演示，展示了如何在不依赖专用框架的情况下运行端到端的强化学习（RL）训练。**该示例已经过测试并与 Agent-lightning v0.1.x 兼容**。

该示例设计为在单个节点上运行，需要 8 个 GPU，每个 GPU 至少具有 40 GB 内存。

## 包含的文件

| 文件/目录 | 描述 |
|----------------|-------------|
| [data_process.sh](file:///Users/admin/git/agent-lightning/examples/search_r1/data_process.sh) | 准备维基百科语料库、数据集和 [retriever](file:///Users/admin/git/agent-lightning/examples/search_r1/retrieval_server.py#L380-L380) conda 环境 |
| [retrieval_launch.sh](file:///Users/admin/git/agent-lightning/examples/search_r1/retrieval_launch.sh) | 启动由处理后的语料库支持的检索服务 |
| [retrieval_server.py](file:///Users/admin/git/agent-lightning/examples/search_r1/retrieval_server.py) | 在训练期间提供文档检索功能的 FastAPI 服务器 |
| [search_r1_agent.py](file:///Users/admin/git/agent-lightning/examples/search_r1/search_r1_agent.py) | 实现 Search-R1 工作流程的 Agent-Lightning rollout 脚本 |
| [train.sh](file:///Users/admin/git/agent-lightning/examples/rag/train.sh) | 启动协调 GRPO 优化的 RL 训练服务器 |
| [qa_em.py](file:///Users/admin/git/agent-lightning/examples/search_r1/qa_em.py) | 用于验证模型预测的精确匹配评估工具 |

---

## 准备数据和环境

运行以下脚本一次以准备数据和检索器环境：

```bash
bash data_process.sh
```


此脚本执行以下步骤：

* 创建一个名为 **`retriever`** 的新 conda 环境。
* 下载用于构建检索数据库的 **维基百科数据**。
* 下载 **训练和测试数据集**。
* 将所有数据存储在新创建的 **`data/`** 目录下。

环境设置和数据处理逻辑改编自 [PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1)。

---

## 准备检索服务器

要启动检索服务器，请运行：

```bash
bash retrieval_launch.sh
```


此脚本会激活先前创建的 **[retriever](file:///Users/admin/git/agent-lightning/examples/search_r1/retrieval_server.py#L380-L380)** 环境，并使用下载的维基百科数据在 `http://127.0.0.1:8000` 启动一个 **检索服务器**。服务器接收用户查询并返回检索到的文本段落的排名列表。

检索服务器的实现基于 [`search_r1/search/retrieval_server.py`](https://github.com/PeterGriffinJin/Search-R1/blob/main/search_r1/search/retrieval_server.py)。

> ⚠️ **注意：** 在训练期间保持检索服务器运行（例如，在单独的 `tmux` 会话或终端窗口中）。

---

## 使用 Llama-3.2-3b-base 运行 RL 训练（GRPO）

1. **启动 Ray**

   ```bash
   bash ../../scripts/restart_ray.sh
   ```


   > 如果您计划使用 WandB 进行实验跟踪，请在启动 Ray 之前设置环境变量
   > `WANDB_API_KEY`。

2. **启动代理**

   ```bash
   python search_r1_agent.py
   ```


   此脚本默认自动启动 **128 个代理工作进程**。每个代理遵循 Search-R1 工作流程，从数据库中检索信息并相应地生成答案。

3. **启动训练服务器**
   在另一个终端中运行：

   ```bash
   bash train.sh
   ```


   此脚本启动 RL 训练服务器。

---

## 评估

评估脚本和基准测试结果将很快发布。