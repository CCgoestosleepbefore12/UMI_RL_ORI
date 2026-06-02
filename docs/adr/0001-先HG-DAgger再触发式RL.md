# ADR 0001 — 先 HG-DAgger,RL 触发式引入

状态:已采纳(2026-06-02)
关联:`docs/方法选型分析.md`、`docs/CONTEXT.md`

## 背景

- 底座:UMI 预训练 **flow-matching** 策略。任务:从人手接书 → 上架。
- 失败模式拆两半:**(a) 广泛泛化**(没见过就崩,靠数据,不碰)+ **(b) 协变量漂移/无法恢复**(熟场景漂出 demo 成功轨迹回不来)。近期范围:**先锁窄场景做稳 (b)**。
- 硬件:有机械臂 + 遥操**实时接管**。定位:工程优先,论文最后。
- 曾计划:Phase 1 直接用 advantage-conditioned RL,并先在 Phase 0 训 reward model。

## 决定

**Phase 0 第一步用 HG-DAgger(纯 BC),不上 RL,也不先训 reward model。**
RL(advantage-conditioned → QAM)降为**触发式升级**;reward/value 模型推迟到触发时再训。

## 理由

1. **绕开 flow-RL 的复杂度税**:flow 策略做 RL 的全部机制(QAM/Flow-SDE/critic 穿去噪)都是为"likelihood 不可解"付的。HG-DAgger 的更新就是 BC——聚合"demo + 人接管纠正",用现成 flow-matching loss 微调,**不碰 likelihood、零新机制**,UMI 现成训练代码即可。
2. **对口**:(b) 协变量漂移正是 DAgger 被发明出来解决的;有遥操实时接管即就绪。
3. **最短路径**:先做最简单、可能直接解决问题的东西,只在它证明不够时才加复杂度。

## 备选方案(为何不选为第一步)

- **直接 advantage-conditioned RL**:能用失败数据、能脱离人自改进,但多一层 reward model + advantage 估计;在 HG-DAgger 够用前不必付。**推迟,非否决。**
- **Q-chunking + QAM / 世界模型 / 纯在线 PPO·SAC / token-GRPO / sim-based**:见 `方法选型分析.md` §4/§6。

## 触发条件(何时从 HG-DAgger 升级到 RL)

- ① 想**脱离人**、让策略在自采 rollout 上自改进(→ 需 reward model);或
- ② HG-DAgger 的 **BC-on-纠正触顶**(继续接管也不再提升);或
- ③ teleop 本身做不好该纠正、需要超过人的动作(书的接递/上架大概率不触发)。

## 后果

- 前期工作量显著减少(免训 reward model)。
- HG-DAgger 与 advantage-conditioned 同谱系,攒下的 HIL 数据可直接复用于触发后的 RL,平滑升级。
- 风险:若 (b) 的某些状态 teleop 也救不回,或 BC 很快触顶,需提前进 Phase 1。
