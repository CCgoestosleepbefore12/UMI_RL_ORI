# UMI-RL 需求规格(spec)

> 状态:**骨架**。正文待 /grill 盘问后填写 —— 不要凭空起草。
> 下面是待澄清的结构提纲(每条都是 /grill 要逼问的点)。

## 1. 目标与动机
- [ ] 一句话目标:对 UMI 预训练 flow-matching 策略做 RL 后训练,达到什么效果?
- [ ] 成功判据:相对预训练策略,在什么任务/指标上提升多少算成功?

## 2. 底座与约束
- [ ] 预训练策略:架构 = flow-matching;具体网络、动作维度、action chunk 长度?
- [ ] 训练信号来源:真机 / offline-to-online / 世界模型想象 / 仿真 —— **未定**
- [ ] 奖励:稀疏成功 / 稠密 / HIL / 学习式 reward —— **未定**
- [ ] 真机预算、UMI 数据规模、算力?

## 3. 方法选型
- [ ] 在三个家族中选定:(A) Flow-SDE(pi_RL) / (B) QAM / (C) advantage-conditioned(RECAP)
- [ ] 选定依据(由 §2 约束反推)

## 4. 模块划分
- [ ] policy / algo / critic / rollout / reward 各自接口与数据流
- [ ] 与 UMI 的边界:哪些 import、哪些必须改 UMI 内部

## 5. 实验与评估
- [ ] 基线、消融、评估协议

## 6. 里程碑
- [ ] 分阶段交付
