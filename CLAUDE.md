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
- [x] **方法选型已定**(详见 `docs/方法选型分析.md`):
  - 约束:flow 策略 · 真机几十条 · sim 不确定 · reward 未定 · 工程优先
  - 关键洞察:**瓶颈是 reward/value 信号,不是 RL 算法**——三家族都依赖它
  - Phase 0(关键路径):定 + 建 reward/value 信号
  - Phase 1(第一线):advantage-conditioned 微调(最省样本、风险最低)
  - Phase 2(升级):Q-chunking critic + QAM
  - 备选:世界模型想象(RISE 近亲)
- [ ] **下一步:/grill Phase 0 的 reward/value 信号**(progress / 学习式 value / 稀疏+LOO / HIL 四选一)→ 填 spec.md → /plan

## 工作流程(沿用全局 CLAUDE.md)

读 spec → /grill → /plan → 确认 → 实现 → 测试 → /simplify → review → /commit。
可独立验证组件(buffer/normalizer/GAE/loss/shape 变换等)走 /tdd。张量操作注释 shape。
