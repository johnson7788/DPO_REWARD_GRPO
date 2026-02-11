1. 数据文件与规模

你有两个文件：

train.parquet：7000 行

test.parquet：1034 行

每行都是一个样本（一个问句及其对应 SQL）。

这就是典型的训练/测试划分：训练集供模型学习，测试集评估泛化能力。

2. 列含义（3 列）

列名是：

question（object / 文本）

自然语言问题，比如：

“How many heads of the departments are older than 56 ?”

这相当于模型输入。

app_id（object / 类别）

指这个问句属于哪个“应用/数据库/场景”。

例子：

department_management

college_1, hr_1, soccer_2

在 Text-to-SQL 场景里，它通常对应 某个具体数据库 schema（表结构不同的那种）。

ground_truth（object / 文本）

目标 SQL（标准答案），比如：

SELECT count(*) FROM head WHERE age > 56

这就是模型要生成的输出。

3. 缺失值情况

所有列缺失值都是 0：

question：0

app_id：0

ground_truth：0

说明数据干净完整，不需要先做缺失值清理。

4. 数据类型统计

三列都是 object，也就是字符串/文本。

没有数值列，因此“数值列统计描述: (无)”是正常的。

5. 频率分布（Top 5 常见值）
5.1 question 的高频项

训练集中最常见的问题是：

“How many students are there?”（4 次）

“How many customers are there?”（4 次）

“Count the number of accounts.”（3 次）

等等

说明：

存在 重复或近重复问句

很多问题在问 COUNT/数量统计

模型会强烈学习到“how many / count” → SELECT count(*) ... 的映射

这种重复在 Text-to-SQL 数据里很常见（不同 app_id 下问法类似，但表不一样）。