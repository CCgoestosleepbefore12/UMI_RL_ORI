# 项目术语表(CONTEXT)

> 随对话持续补充。每条:术语 — 定义 — 在本项目里的含义。

## 任务

- **目标任务** — 从人手中接过一本书,放到书架上。含天然阶段:接近人手 → 抓书 → 搬运 → 上架放置。
- **硬件** — 有机械臂在跑策略 + 遥操可**实时接管**(HIL-SERL 就绪)。
- **失败模式拆成两半**(关键区分):
  - **(a) 广泛泛化** — 没见过的书/手势/书架/背景/光照就崩。**RL 治不了,靠数据**(UMI 多样 demo + 表征)。**Phase 0 明确不碰。**
  - **(b) 协变量漂移/无法恢复** — 熟场景下策略漂出 demo 成功轨迹就回不来(demo 全成功、没教过救回)。**这是 RL/HIL 的靶子。**
- **近期范围** — **先锁窄场景做稳**(固定房间 + 一小批书 + 固定书架),robust 后再用数据扩范围。

## 方法路线(关键)

- **Phase 0 = HG-DAgger**(不是 RL)——人 gated 实时接管纠正,聚合"demo + 纠正"用**现成 flow-matching loss** 微调。**绕开 flow 策略做 RL 的全部复杂度税**(likelihood 不可解 → QAM/Flow-SDE/critic),(b) 协变量漂移正是 DAgger 的对口问题。详见 `docs/adr/0001-*.md`。
- **RL 是触发式升级**(Phase 1 advantage-conditioned → Phase 2 QAM):仅当①想脱离人自改进(需 reward model)或②BC-on-纠正触顶时才上。
- **reward model 推迟** — Phase 0 不需要;触发 Phase 1 时用 HG-DAgger 攒的 HIL 数据训(人接管=负信号、纠正动作=高 advantage、整条 rollout 人标成败)。
- **HG-DAgger 与 advantage-conditioned 同谱系** — 后者 ≈ 前者 + 用失败数据 + 按 advantage 加权;平滑升级,数据复用。

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
