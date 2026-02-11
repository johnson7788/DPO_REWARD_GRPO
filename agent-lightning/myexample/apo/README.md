# APO Example

三种 use case（这是 README 的核心）
| 用例               | 实际学到的能力                       |
| ---------------- | ----------------------------- |
| Built-in APO     | **Prompt 是怎么被自动优化的**          |
| Custom Algorithm | **Agent-Lightning 的训练接口长什么样** |
| Debugging        | **为什么 agent 做错了 & 如何定位**      |


# 一句话总览（先给你一个 mental model）

> **examples/apo** 这个目录不是一个 demo，而是一个 **“APO 教学合集”**：
>
> * **Sample 1**：教你 *如何用现成 APO 算法训练 prompt*
> * **Sample 2**：教你 *如果 APO 不够用，怎么自己写训练算法*
> * **Sample 3**：教你 *agent 表现不对时怎么 debug*

**唯一真正“跑模型训练”的是 Sample 1，其余都是方法论与工程示例。**

---

## 2️⃣ Overview：三种 use case（这是 README 的核心）

```md
three distinct use cases:
- built-in APO
- custom training algorithms
- debugging agents
```

### 翻译成“你在学什么”

| 用例               | 实际学到的能力                       |
| ---------------- | ----------------------------- |
| Built-in APO     | **Prompt 是怎么被自动优化的**          |
| Custom Algorithm | **Agent-Lightning 的训练接口长什么样** |
| Debugging        | **为什么 agent 做错了 & 如何定位**      |

👉 **README 在刻意告诉你**：

> “不要把 APO 当成黑盒，我们连黑盒怎么造都教你。”

---

## 3️⃣ Requirements：为什么强调 OpenAI-compatible

```md
All examples also require an OpenAI-compatible API service.
```

### 背后原因

* APO 本身要用 **LLM 来改 prompt**

  * 一个 LLM 做 rollout
  * 一个（或同一个）LLM 做 *gradient / critique / edit*
* 只要是 **OpenAI API 协议兼容** 就行

  * Azure OpenAI
  * vLLM + OpenAI shim
  * 其他兼容服务

---

## 4️⃣ Included Files：这是整个 examples/apo 的“地图”

### 重点文件逐个对齐你现在的理解

| 文件                                | 真正用途                                              |
| --------------------------------- | ------------------------------------------------- |
| `room_selector.py`                | **Agent 本体**（rollout + function calling + grader） |
| `room_selector_apo.py`            | **Sample 1：APO 训练入口**                             |
| `room_tasks.jsonl`                | **监督数据 + reward 真值**                              |
| `apo_custom_algorithm.py`         | 自己写 APO / RL / 搜索算法                               |
| `apo_custom_algorithm_trainer.py` | 把自定义算法塞进 Trainer                                  |
| `apo_debug.py`                    | trace / replay / step-by-step debug               |
| `legacy_*`                        | 历史包袱，**可以忽略**                                     |

👉 **重要认知**：
**Sample 1 ≠ Sample 2**

* Sample 1：你是“算法使用者”
* Sample 2：你是“算法作者”

---

## 5️⃣ Sample 1：Built-in APO（你现在正在看的主线）

```md
room_selector_apo.py
```

### README 表面说了什么

> 用内置 APO 算法
> 优化 room booking agent 的 prompt
> 算法自动管理训练循环、梯度、prompt 更新

### 实际发生了什么（关键）

APO 在这里做的是：

```
Prompt_0
  ↓ rollout on room_tasks.jsonl
  ↓ reward (expected_choice)
  ↓ LLM 写“为什么错了”
  ↓ LLM 按批评改 prompt
  ↓ beam search 选更好的 prompt
Prompt_1
```

**你并没有：**

* 写 loss
* 写 backward
* 写 optimizer

但你仍然在做一种 **prompt-level policy optimization**。

README 强调这一点，是为了告诉你：

> “这是工程化可复现的，不是 prompt 魔法。”

---

## 6️⃣ Sample 2：Custom Algorithms（为什么要有这一部分）

```md
apo_custom_algorithm.py
apo_custom_algorithm_trainer.py
```

### 为什么 README 要花这么多字讲它？

因为 APO 不是万能的：

* 你可能想：

  * 非 0/1 reward
  * 多目标 reward
  * curriculum
  * offline replay
  * 自己的 search / RL 算法

Sample 2 教你 **Agent-Lightning 的核心抽象**：

```
Algorithm
   ↕
Trainer
   ↕
Runner (rollout executor)
```

### 两种运行方式的含义

#### Option A：algo / runner 分离

```bash
agl store
python apo_custom_algorithm.py algo
python apo_custom_algorithm.py runner
```

这是：

* **分布式 / 可扩展**模式
* 算法和 rollout 可独立扩容

#### Option B：Trainer 集成

```bash
python apo_custom_algorithm_trainer.py
```

这是：

* **单机教学模式**
* 用来理解接口最清晰

---

## 7️⃣ Sample 3：Debugging（为什么这是一个“sample”）

```md
apo_debug.py
```

这说明一个事实：

> **Agent-Lightning 认为：调 agent ≠ 调 prompt**

Debug 示例通常展示：

* rollout replay
* span / trace
* 中间工具调用
* reward 计算过程

👉 **这和 APO 强相关**：
如果你不知道 agent 为什么错，APO 也会学错。

---

## 8️⃣ Appendix：Dataset Format（为什么放在最后）

```md
Appendix: Dataset Format
```

### 隐含的信息

* **APO 不关心你数据语义**
* 只要你能：

  1. 把 `task_input` 喂给 agent
  2. 用 `expected_choice` 算 reward

所以这个 appendix 是在说：

> “room booking 只是一个例子，不是限制。”

---

## 9️⃣ 把 README 和你现在的理解对齐成一张图

```
room_tasks.jsonl
        ↓
room_selector.py (agent + grader)
        ↓
room_selector_apo.py
   - Trainer
   - APO (beam search + LLM edits)
        ↓
Best Prompt Template
```

**整个 README 就是在教你这条链路 + 如何改写其中任何一环。**

---

## 10️⃣ 如果你继续往下学，推荐顺序

既然你已经看了数据集，我建议你：

1️⃣ 看 `room_selector.py`
→ 明确：**reward 是怎么给的**

2️⃣ 再看 `room_selector_apo.py`
→ 明确：**APO 每个参数在控制什么**

3️⃣ 最后看 `apo_debug.py`
→ 学会 **prompt 学坏时怎么抓证据**

---

## 1️⃣ 整体结构：一行 = 一个可评测的任务（JSONL）

`room_tasks.json`（准确说是 `.jsonl`）是 **JSON Lines** 格式：

* 每一行是一个 **独立的 meeting room 选择任务**
* APO 会把它当成 **监督式环境 + reward 函数**

通用结构是：

```json
{
  "id": "s01",
  "task_input": { ... },
  "expected_choice": "No Room"
}
```

---

## 2️⃣ 字段逐个解释

### 🆔 `id`

```json
"id": "s01"
```

* 任务的唯一标识
* 主要用于：

  * debug / 日志
  * rollout trace 可视化
  * 错误样本定位
* **不参与 reward 计算**

---

### 📥 `task_input`（Agent 的“观察”）

这是 **agent 在 rollout 时看到的全部输入信息**。

```json
"task_input": {
  "date": "2025-10-13",
  "time": "16:30",
  "duration_min": 30,
  "attendees": 12,
  "needs": ["projector", "confphone"],
  "accessible_required": true
}
```

逐项说明：

#### 📅 `date`

* 会议日期（通常只影响 availability lookup）
* 在示例中多半是 **常量**，主要是让 prompt 更真实

#### ⏰ `time`

* 会议开始时间
* agent 通常要判断：

  * 是否与房间占用时间冲突
  * 是否跨越已有 booking

#### ⏱ `duration_min`

* 会议持续分钟数
* 与 `time` 组合 → `[start, end)` 时间段

#### 👥 `attendees`

* 参会人数
* 用于判断：

  * 房间容量是否 ≥ attendees

#### 🧰 `needs`

```json
["projector", "confphone"]
```

* 设备需求列表
* 常见值：

  * `projector`
  * `whiteboard`
  * `confphone`
* **必须全部满足**，否则该房间无效

#### ♿ `accessible_required`

* 是否必须是无障碍房间
* 如果为 `true`：

  * 非 accessible 的房间必须排除

👉 **关键点**：
`task_input` 是 **prompt 模板 format 时直接插进去的变量**，例如：

```text
The meeting requires:
- 12 attendees
- projector, confphone
- accessibility: required
```

---

### 📤 `expected_choice`（reward 的唯一真值）

```json
"expected_choice": "No Room"
```

这是 **grader 用来打分的“标准答案”**。

可取值通常包括：

* 具体房间名：`"Nova"`, `"Lyra"`, `"Atlas"`, `"Pulse"`, `"Quark"`
* 特殊值：`"No Room"`

---

## 3️⃣ “No Room” 的语义（非常重要）

`"No Room"` **不是失败**，而是一种**正确决策**。

它表示：

> 在所有房间中，没有任何一个同时满足
> **时间 + 容量 + 设备 + 无障碍** 的约束

例如 s01：

```json
{
  "attendees": 12,
  "needs": ["projector", "confphone"],
  "accessible_required": true,
  "time": "16:30"
}
```

可能的真实情况是：

* 能坐 12 人的房间只有 Nova
* Nova 在 16:30 已被占用
* 或 Nova 没有 projector
  👉 所以正确输出是 `"No Room"`

**这点对 prompt 非常关键**：
APO 会学会 **什么时候要“拒绝给房间”**，而不是瞎选一个。

---

## 4️⃣ 数据集在 APO 训练中扮演的角色

### (1) Rollout 阶段

对每一条数据：

```
task_input
   ↓
PromptTemplate.format(task_input)
   ↓
LLM + tools
   ↓
agent_choice
```

---

### (2) Grader / Reward 计算

本示例几乎一定是 **exact match reward**：

```python
reward = 1.0 if agent_choice == expected_choice else 0.0
```

（有时会允许大小写 / 同义词，但本例一般是严格匹配）

---

### (3) APO 学到的“知识”不是数据，而是决策逻辑

APO 不会记住：

> “s05 → Lyra”

它学到的是：

* 容量优先级
* 设备是 hard constraint
* accessible_required = true 时不能选普通房
* 冲突时间一定要拒绝
* **No Room 是合法输出**

这些规则会**被编码进 prompt 结构和指令措辞中**。

---

## 5️⃣ 从这 10 条样本能推断出的隐含规则

你给的片段里已经能看出一些设计意图：

| 规则              | 证据                         |
| --------------- | -------------------------- |
| 房间有不同容量         | 8 人选 Quark，10 人选 Lyra      |
| accessible 是硬条件 | s04 不要求 accessible → Quark |
| 同一房间不同时间可/不可用   | Nova 有时可选，有时不可             |
| 设备必须全匹配         | 缺一个 → No Room              |
| 不要“将就”          | s01 / s03 明确 No Room       |

这些都是 **APO 要通过 reward 反推出来的**。

---

## 6️⃣ 你读代码时的对照重点（强烈建议）

当你再看 `room_selector.py` / `room_selector_apo.py`，重点对照：

1️⃣ prompt 里有没有明确写：

* “If no room satisfies all constraints, answer **No Room**”

2️⃣ grader 是否是：

```python
choice == expected_choice
```

3️⃣ APO 的 validation set 是否 **包含 No Room 样本**
→ 否则 prompt 会学坏（总想选一个）


# 