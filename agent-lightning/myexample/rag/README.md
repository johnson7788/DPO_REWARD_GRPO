# RAG Agent 示例

本示例演示了如何使用 Agent-Lightning 训练一个检索增强生成（RAG）智能体，该智能体具备从维基百科检索信息的能力。该智能体通过检索和推理维基百科段落来回答来自 MuSiQue 数据集的多跳问题。**此示例已在 Agent-lightning v0.1.x 版本上测试并兼容**。

## 概述

本示例最初在单个节点上运行，需要四个 GPU，每个 GPU 至少需要 40GB 内存。

1. 在 wiki_retriever_mcp 文件夹中准备 RAG 数据集。需要维基百科片段（`nq_list.pkl`）和 Faiss 索引（`nq_hnsw_faiss_n32e40.index`）。（完整的维基百科转储文件很大，稍后会提供更多信息）
2. 在 `data` 文件夹中准备训练数据。从[这里](https://drive.google.com/drive/folders/1hEqOY4EbplUB5ew-8UPFhV_5QU2j7WCN?usp=drive_link)下载。需要 `musique_train.parquet` 和 `musique_dev_128.parquet`。
3. 设置 wiki retriever MCP 的环境：`bash wiki_retriever_install.sh`。这将安装所需的包并为 wiki retriever MCP 设置环境。
4. 启动 wiki retriever MCP：`python wiki_retriever_mcp.py`。这将启动 wiki retriever MCP 服务器。
5. 启动 Ray：`bash ../../scripts/restart_ray.sh`。要使用 Wandb，您需要在启动 Ray 之前设置 WANDB_API_KEY 环境变量。
6. 运行智能体：`python rag_agent.py`。默认情况下，这将自动启动 12 个智能体工作进程。
7. 在另一个终端中，启动训练服务器：`bash train.sh`。

## 包含的文件

| 文件/目录 | 描述 |
|----------------|-------------|
| `rag_agent.py` | 运行 Agent-Lightning RAG 训练管道的入口点 |
| `train.sh` | 启动更新智能体的 GRPO 训练服务器 |
| `utils.py` | 用于精确匹配、F1 分数和响应解析的评分工具 |
| `wiki_retriever_mcp/` | 维基百科检索的设置脚本和 MCP 服务器（`wiki_retriever_install.sh`，`wiki_retriever_mcp.py`）|

## 准备检索语料库

为了使这个 mcp 服务器能够进行语义检索，我们需要两个文件：

1. **FAISS 索引文件**（`.index`）
2. **块列表文件**（`.pkl`）

这两个文件协同工作：FAISS 索引存储向量嵌入及其到整数 ID 的映射，而 pickle 文件存储实际的文本块。索引中的整数 ID 与块列表中的位置完全对应。

---

### 步骤 1. 收集文本块

首先需要一个文本段落（块）的集合。例如，您可以下载基于维基百科的数据集，如  中的 `wiki18_100w.zip`，或使用其他预分割的语料库。
https://huggingface.co/datasets/RUC-NLPIR/FlashRAG_datasets/commit/f2de0bd8153a00c9e51566e572734d761075983d
---

### 步骤 2. 创建 FAISS 索引（`nq_hnsw_faiss_n32e40.index`）

- 使用句子嵌入模型（例如，`BAAI/bge-large-en-v1.5`）将每个块编码为向量。
- 从这些向量构建 FAISS 索引。
- 在此示例中，我们使用**HNSW 索引**（分层可导航小世界图），它支持高效的近似最近邻搜索。
- 索引只存储嵌入和整数 ID（不存储原始文本）。

---

### 步骤 3. 创建块列表（`nq_list.pkl`）

- 将原始文本块存储在 Python 列表中。
- 使用 `pickle` 保存此列表。
- FAISS 返回的索引 ID 对应于此文件中的列表索引。例如，如果 FAISS 搜索返回 `I[0][i] = 12345`，则相应的文本块是 `chunks[12345]`。

---

### 示例架构

- **`nq_hnsw_faiss_n32e40.index`**
  - 类型：FAISS HNSW 索引
  - 包含：
    - 向量嵌入
    - 用于快速搜索的图结构
    - 映射到块位置的整数 ID

- **`nq_list.pkl`**
  - 类型：Pickled Python 列表
  - 元素类型：字符串（或包含文本+元数据的字典，取决于预处理）
  - 示例：
    ```python
    [
        "埃菲尔铁塔位于法国巴黎。",
        "阿尔伯特·爱因斯坦提出了相对论。",
        ...
    ]
    ```

---

### 步骤 4. 代码示例：构建索引和块列表
警告：以下示例仅演示了一个小规模的工作流程。在实践中，如果数据集很大，您应该批量编码文本并逐步将其添加到索引中。

```python
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# 1. 准备您的文本块（字符串列表）
chunk_texts = [
    "埃菲尔铁塔位于法国巴黎。",
    "阿尔伯特·爱因斯坦提出了相对论。",
    "Python 是一种流行的编程语言。",
    # ... 更多块
]

# 2. 加载嵌入模型
model = SentenceTransformer("BAAI/bge-large-en-v1.5")

# 3. 将文本块编码为嵌入
embeddings = model.encode(chunk_texts, normalize_embeddings=True)

# 4. 构建 FAISS HNSW 索引
dim = embeddings.shape[1]
index = faiss.IndexHNSWFlat(dim, 32)   # 默认 32 个邻居
index.hnsw.efConstruction = 40         # efConstruction 参数
index.add(embeddings)

# 5. 保存 FAISS 索引
faiss.write_index(index, "nq_hnsw_faiss_n32e40.index")

# 6. 保存块列表
with open("nq_list.pkl", "wb") as f:
    pickle.dump(chunk_texts, f)

print("索引和块列表保存成功。")
```

## 评估

结果即将推出。