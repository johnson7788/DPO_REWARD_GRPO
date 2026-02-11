# 安装环境
```
git clone https://github.com/microsoft/agent-lightning.git
cd agent-lightning
bash scripts/setup_stable_gpu.sh
```
## 其它安装方法
```
安装类型	使用场景	主要依赖	命令
标准版	基础 Agent 训练，无需 GPU	Agent Lightning 核心组件	pip install agentlightning
开发版	贡献代码，高级功能	开发工具、Agent 框架	pip install -e .[dev,agent,apo]
GPU 稳定版	生产环境 RL 训练	PyTorch 2.7、vLLM 0.9.2、VERL 0.5.0	bash scripts/setup_stable_gpu.sh
GPU 最新版	最新功能	PyTorch 2.8、vLLM 0.10.2、最新 VERL	bash scripts/setup_latest_gpu.sh
```

# 验证
```
# 检查 CLI 是否可用
agl --help
 
# 测试基础导入
python -c "import agentlightning; print(agentlightning.__version__)"
 
# 运行最小示例
cd examples/minimal
python write_traces.py --help
```