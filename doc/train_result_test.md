# 训练后的模型测试
## 训练后的模型回答明显更丰富了

====== 开始 RAGAgent 真实环境测试 ======
LLM 资源配置完成: local_agent_model @ DeepSeek API

>>> 正在提问: 药品开胸顺气丸的可以用来治什么？
>>> 等待 DeepSeek 思考与工具调用 (请观察 ToolLoggingHooks 输出)...

2026-02-11 13:10:25,329 - INFO - --- Q: 药品开胸顺气丸的可以用来治什么？ ---
2026-02-11 13:10:25,329 - INFO - --- Q: 药品开胸顺气丸的可以用来治什么？ ---
13:10:25 - LiteLLM:INFO: utils.py:3427 - 
LiteLLM completion() model= local_agent_model; provider = hosted_vllm
2026-02-11 13:10:25,338 - INFO - 
LiteLLM completion() model= local_agent_model; provider = hosted_vllm
13:10:27 - LiteLLM:INFO: utils.py:3427 - 
LiteLLM completion() model= local_agent_model; provider = hosted_vllm
2026-02-11 13:10:27,177 - INFO - 
LiteLLM completion() model= local_agent_model; provider = hosted_vllm
2026-02-11 13:10:28,861 - INFO - [规则奖励]发现执行了SQL: SELECT `indication` FROM drugs_info WHERE `med_name` = '开胸顺气丸';
2026-02-11 13:10:28,861 - INFO - [规则奖励]发现执行了SQL: SELECT `indication` FROM drugs_info WHERE `med_name` = '开胸顺气丸';

====== 测试执行完成 ======
最终奖励得分 (Reward): 5.0375
2026-02-11 13:10:29,008 - INFO - [外部奖励模型] 评分: 4.9375
2026-02-11 13:10:29,008 - INFO - [外部奖励模型] 评分: 4.9375
2026-02-11 13:10:29,008 - INFO - [LLM奖励] 回答质量奖励: 4.938
2026-02-11 13:10:29,008 - INFO - [LLM奖励] 回答质量奖励: 4.938
2026-02-11 13:10:29,008 - INFO - 问题: 药品开胸顺气丸的可以用来治什么？的答案
根据查询结果，“开胸顺气丸”主要用于以下病症：

1. 消积化滞，行气止痛。适用于气郁食滞引起的各种症状，如胸胁胀满、胃脘疼痛、嗳气呕恶、食少纳呆。
2. 理气宽胸，消积导滞。适用于气郁不舒、停食停水引起的胸膈痞满、脘腹胀痛、饮食减少等症状。

这种药物主要针对由气郁和食滞引起的相关症状，帮助缓解因这些原因导致的不适。如果您有具体症状或健康问题，请咨询医生或药师以获得专业建议。对应的轮次奖励: 5.0375
2026-02-11 13:10:29,008 - INFO - 问题: 药品开胸顺气丸的可以用来治什么？的答案
根据查询结果，“开胸顺气丸”主要用于以下病症：

1. 消积化滞，行气止痛。适用于气郁食滞引起的各种症状，如胸胁胀满、胃脘疼痛、嗳气呕恶、食少纳呆。
2. 理气宽胸，消积导滞。适用于气郁不舒、停食停水引起的胸膈痞满、脘腹胀痛、饮食减少等症状。

这种药物主要针对由气郁和食滞引起的相关症状，帮助缓解因这些原因导致的不适。如果您有具体症状或健康问题，请咨询医生或药师以获得专业建议。对应的轮次奖励: 5.0375
2026-02-11 13:10:29,008 - INFO - Stop multi-turn: reward=5.037, 
2026-02-11 13:10:29,008 - INFO - Stop multi-turn: reward=5.037, 
2026-02-11 13:10:34,203 - WARNING - [non-fatal] Tracing: request failed: timed out
2026-02-11 13:10:40,230 - WARNING - [non-fatal] Tracing: request failed: timed out
2026-02-11 13:10:47,274 - WARNING - [non-fatal] Tracing: request failed: timed out
2026-02-11 13:10:47,274 - ERROR - [non-fatal] Tracing: max retries reached, giving up on this batch.