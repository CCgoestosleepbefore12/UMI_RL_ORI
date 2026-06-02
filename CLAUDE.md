# UMI_RL_ORI — 项目说明(进入本目录先读)

## 这是什么

在 **UMI 预训练的 flow-matching 策略**之上做**强化学习后训练**的项目。
本仓库是官方 UMI 的 **fork**(不是 submodule),原因见下。

## 架构决定:为什么用 fork 而不是 submodule

- 本项目**会改动 UMI 内部源码**。submodule 里的文件属于上游历史、不属于本仓库,编辑后改动游离,必须倒进单独 fork 再更新指针 —— 研究阶段摩擦太大。
- 规则:**要改底座 → fork-and-own;只调用底座 → submodule。** 本项目属前者。
- 代价:历史与 UMI 混合,合并上游可能冲突 —— 这是"既改底座又跟上游"的固有成本。

## 仓库结构

```
UMI_RL_ORI/
├── (UMI 原始源码)          ← 可直接改,改动记入本仓库历史
│   diffusion_policy/ umi/ scripts*/ train.py eval_real.py ...
├── umi_rl/                  ← 本项目新增的 RL 代码(尽量把 UMI 当库 import)
│   ├── policy/  algo/  critic/  rollout/  reward/
├── configs/rl/             ← RL 配置
├── docs/spec.md            ← 需求规格(待 /grill 后填)
└── docs/CONTEXT.md         ← 项目术语表(随对话持续补充)
```

## remote

- `origin`   → git@github.com:CCgoestosleepbefore12/UMI_RL_ORI.git(本项目)
- `upstream` → 官方 UMI(只读,push 已禁用);跟官方更新:`git fetch upstream && git merge upstream/main`

## 当前状态 / 下一步

- [x] fork UMI、搭好骨架
- [ ] **方法选型未定**:flow 策略 RL 的三个家族 —— (A) Flow-SDE/把去噪当 MDP(pi_RL)、(B) critic 梯度蒸馏(QAM)、(C) advantage-conditioned 监督(RECAP/RISE,已读)。详见 docs/CONTEXT.md。
- [ ] 下一步:深读 pi_RL + QAM → 定信号来源(真机/offline-to-online/世界模型)与奖励 → /grill 填 spec.md → /plan
- 信号来源、奖励:**均未定**(应读够几篇后反推,不要凭感觉)

## 工作流程(沿用全局 CLAUDE.md)

读 spec → /grill → /plan → 确认 → 实现 → 测试 → /simplify → review → /commit。
可独立验证组件(buffer/normalizer/GAE/loss/shape 变换等)走 /tdd。张量操作注释 shape。
