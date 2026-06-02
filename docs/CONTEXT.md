# 项目术语表(CONTEXT)

> 随对话持续补充。每条:术语 — 定义 — 在本项目里的含义。

## 底座

- **UMI**(Universal Manipulation Interface)— 手持夹爪在野外采数据 + 训 Diffusion/Flow Policy 的范式;本项目的预训练底座。
- **flow-matching 策略** — 用速度场把噪声流到动作分布的生成式策略。**边际 action log-likelihood 不可解**(积分算不出),这是本项目 RL 的核心技术难点。

## flow 策略 RL 的核心矛盾

标准 PPO/GRPO 需要 `log π(a|s)` 算 importance ratio,但 flow/diffusion 的 likelihood 不可解。
所以问题不是"PPO 还是 GRPO",而是:**怎么把 RL 信号传进一个 likelihood 不可解的 flow 策略?**
→ 基于自回归 token-likelihood 的 GRPO(SimpleVLA-RL/TGRPO/RIPT-VLA)对本项目**直接失效**。

## 三个可用家族(真正要选的"方法")

| 家族 | 怎么绕过 likelihood | 代表 | 天然搭配信号来源 |
| :-- | :-- | :-- | :-- |
| **(A) 去噪当 MDP/SDE** | 把逐步去噪 reparameterize 成 SDE,在每步做 policy gradient | **pi_RL**(Flow-SDE/Flow-Noise)、RL-100 | 在线 / 仿真 |
| **(B) critic 梯度蒸馏** | 不算 likelihood,把 critic 梯度经 adjoint matching 转成对 flow 每步的逐步监督 | **QAM**、LWD | offline-to-online |
| **(C) advantage-conditioned 监督** | 把 advantage 当条件,退化成监督式 BC,彻底躲开 likelihood | **RECAP/RISE**(已读) | 离线 / 世界模型想象 |

> 方法选型 = 选哪个家族;家族与"信号来源"强耦合 —— 这两个其实是同一个决定。

## 优先深读

- **pi_RL** — 代表 (A),与本项目架构最贴(arXiv 2510.25889)
- **QAM** — 代表 (B),adjoint matching 把 critic 梯度灌进 flow(arXiv 2601.14234)
- RISE — (C) 已读,直接对照

> 关联 Obsidian 笔记:`maps/强化学习后训练 主题地图.md`、`concepts/Advantage-conditioned 微调.md`
