"""UMI-RL:在 UMI 预训练 flow-matching 策略之上做强化学习后训练。

设计原则:UMI 当作底座(尽量当库用),RL 相关的新代码都放在本包内。
需要改动 UMI 内部时直接改(本仓库是 fork,不是 submodule),改动记录进本仓库历史。

子包:
- policy : 对 UMI 策略的 RL 包装(Flow-SDE 采样、advantage-conditioned 包装等)
- algo   : RL 算法实现(pi_RL / QAM / RECAP ...)
- critic : value / Q 网络
- rollout: rollout 采集(真机 / 仿真 / 世界模型想象)
- reward : 奖励定义与 reward/critic 模型
"""
