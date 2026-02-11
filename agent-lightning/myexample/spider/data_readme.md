# Spider 数据集目录说明

## 概述

本目录包含 Spider 训练和开发数据集，用于 [EMNLP 2018 论文](https://aclanthology.org/D18-1245.pdf) 中描述的复杂跨域语义解析和 Text-to-SQL 任务。Spider 是一个大规模人工标注的数据集，包含复杂的 SQL 查询和多个数据库。

## 文件结构

```
data/
├── train_spider.json          # Spider 训练集（主训练数据）
├── train_others.json          # 其他领域训练数据
├── train_gold.sql             # 训练集标准答案 SQL
├── dev.json                   # 验证集
├── dev_gold.sql               # 验证集标准答案 SQL
├── test.json                  # 测试集
├── test_tables.json           # 测试集数据库模式
├── tables.json                # 所有数据库模式定义
├── train_others.json          # 其他来源的训练数据
├── README.txt                 # 原始数据集说明
├── dev.parquet                # 验证集（Parquet格式）
├── train_spider.parquet       # 训练集（Parquet格式）
├── test.parquet               # 测试集（Parquet格式）
├── test_dev.parquet           # 测试集采样（100条）
├── test_dev_500.parquet       # 测试集采样（500条）
└── database/                  # SQLite 数据库文件目录
    ├── academic/
    ├── concert_singer/
    ├── restaurant_1/
    ├── scholar/
    ├── imdb/
    ├── yelp/
    └── ... (共 166 个数据库)
```

## 数据集统计

| 文件 | 样本数 | 数据库数 | 用途 |
|------|--------|----------|------|
| train_spider.json | 7,000 | 140 | 主训练集 |
| train_others.json | 1,659 | 6 | 补充训练集 |
| train_gold.sql | 8,659 | - | 训练集标注SQL |
| dev.json | 1,034 | 20 | 验证/开发集 |
| dev_gold.sql | 1,034 | - | 验证集标注SQL |
| test.json | - | - | 测试集 |

**官方最终训练集** = train_spider.json + train_others.json = **8,659 条样本**

## 数据格式

### JSON 文件格式

每个 JSON 文件包含一组训练样本，每个样本格式如下：

```json
{
    "db_id": "concert_singer",
    "query": "SELECT count(*) FROM singer",
    "query_toks": ["SELECT", "count", "(", "*", ")", "FROM", "singer"],
    "query_toks_no_value": ["select", "count", "(", "*", ")", "from", "singer"],
    "question": "How many singers do we have?",
    "question_toks": ["How", "many", "singers", "do", "we", "have", "?"],
    "sql": {
        "from": {"table_units": [["table_unit", 1]], "conds": []},
        "select": [false, [[3, [0, []]]]],
        "where": [],
        "groupBy": [],
        "orderBy": [],
        "having": [],
        "limit": null,
        "intersect": null,
        "except": null,
        "union": null
    }
}
```

字段说明：

| 字段 | 类型 | 说明 |
|------|------|------|
| `db_id` | string | 数据库唯一标识符 |
| `query` | string | 标准 SQL 查询语句 |
| `query_toks` | list | SQL 语句的分词结果 |
| `query_toks_no_value` | list | SQL 分词（去除数值） |
| `question` | string | 自然语言问题 |
| `question_toks` | list | 问题的分词结果 |
| `sql` | dict | 解析后的 SQL 结构化表示 |

### tables.json 格式

数据库模式定义文件：

```json
{
    "db_id": "concert_singer",
    "table_names": ["singer", "concert", "stadium"],
    "column_names": [
        [-1, "*"],
        [0, "singer_id"],
        [0, "name"],
        [0, "country"],
        [0, "age"],
        [1, "concert_id"],
        [1, "concert_name"],
        ...
    ],
    "column_types": ["number", "text", "text", "number", ...],
    "primary_keys": [[0, "singer_id"], [1, "concert_id"]],
    "foreign_keys": [
        [1, "stadium_id", "stadium", "stadium_id"]
    ]
}
```

字段说明：

| 字段 | 说明 |
|------|------|
| `db_id` | 数据库标识符 |
| `table_names` | 所有表名列表 |
| `column_names` | 列名列表，每项为 [table_id, column_name] |
| `column_types` | 列的数据类型 |
| `primary_keys` | 主键定义 |
| `foreign_keys` | 外键定义 |

### Gold SQL 文件格式

每行一条记录，格式为：`SQL语句\t数据库ID`

```
SELECT count(*) FROM singer	concert_singer
SELECT name, country, age FROM singer ORDER BY age DESC	concert_singer
...
```

## 数据库目录结构

每个数据库目录下包含：

```
database/{db_name}/
├── {db_name}.sqlite    # SQLite 数据库文件（可执行）
└── schema.sql          # 数据库建表 SQL 语句
```

示例（concert_singer 数据库）：

- **singer 表**: singer_id, name, country, age, song_name, song_release_year, net_worth
- **concert 表**: concert_id, concert_name, theme, stadium_id, year
- **stadium 表**: stadium_id, name, location, capacity, average, highest, lowest

## Parquet 文件

由 `convert_dataset.py` 脚本从 JSON 转换而来，包含精简的列：
- `db_id`
- `question`
- `query`

用于模型训练时的数据加载优化。

## 数据来源

### train_spider.json
- 140 个不同领域的数据库
- 7,000 条训练样本
- 覆盖多种复杂 SQL 查询（JOIN、嵌套查询、聚合等）

### train_others.json
来自以下数据集（由 Finegan-Dollak et al., 2018 准备）：
- **Restaurants**: 餐厅数据库
- **GeoQuery**: 地理查询数据库
- **Scholar**: 学术数据库
- **Academic**: 学术数据库
- **IMDB**: 电影数据库
- **Yelp**: 商业评价数据库

### 数据库列表（共 166 个）

| 类别 | 数据库示例 |
|------|-----------|
| 音乐 | concert_singer, singer, music_1, orchestra |
| 餐饮 | restaurant_1, restaurants, coffee_shop, pizza_1 |
| 体育 | baseball_1, soccer_1, sports_competition, university_basketball |
| 航空 | flight_1, flight_2, airline_1, train_station |
| 学术 | scholar, academic, school_finance, student_assessment |
| 电影 | movie_1, imdb, film_rank, tvshow |
| 商业 | yelp, customer_complaints, department_store, product_catalog |
| 政府 | local_govt_in_alabama, county_public_safety, e_government |
| 其他 | hospital_1, hotel_1, insurance_fnol, manufacturer |

## SQL 复杂度分类

Spider 数据集按复杂度分为四个级别：

| 难度 | 特征 | 占比 |
|------|------|------|
| **Easy** | 简单查询，单表 | ~25% |
| **Medium** | GROUP BY, ORDER BY, WHERE | ~40% |
| **Hard** | JOIN, 子查询, OR | ~25% |
| **Extra Hard** | UNION, EXCEPT, INTERSECT | ~10% |

## 使用示例

```python
import json

# 加载训练数据
with open('data/train_spider.json', 'r') as f:
    train_data = json.load(f)

# 查看第一条样本
sample = train_data[0]
print(f"Database: {sample['db_id']}")
print(f"Question: {sample['question']}")
print(f"SQL: {sample['query']}")

# 加载数据库模式
with open('data/tables.json', 'r') as f:
    schemas = json.load(f)

# 获取特定数据库模式
schema = next(s for s in schemas if s['db_id'] == 'concert_singer')
print(f"Tables: {schema['table_names']}")
```

## 评估指标

使用 `spider_eval/` 目录下的评估脚本，主要指标：

- **Exact Match Accuracy**: SQL 语句完全匹配
- **Execution Accuracy**: SQL 执行结果匹配

## 相关论文

如果使用此数据集，请引用：

```bibtex
@article{Yu&al.18c,
  title = {Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task},
  author = {Tao Yu and Rui Zhang and Kai Yang and Michihiro Yasunaga and Dongxu Wang and Zifan Li and James Ma and Irene Li and Qingning Yao and Shanelle Roman and Zilin Zhang and Dragomir Radev},
  booktitle = {EMNLP},
  year = {2018}
}
```

## 参考链接

- [Spider 数据集官网](https://yale-lily.github.io/spider)
- [GitHub 仓库](https://github.com/taoyds/spider)
- [评估代码](https://github.com/taoyds/test-suite-sql-eval)
