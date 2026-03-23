# FECG_LEAN — Lean4 形式化证明

> 原始仓库：https://github.com/simulai/FECG_LEAN

## 核心文件

| 文件 | 内容 |
|------|------|
| `FECG_LEAN.lean` | 单模态吸引子动力学形式化 |
| `Composite.lean` | 复合架构稳定性证明（异步更新） |
| `MultiModal.lean` | 多模态概念对齐形式化 |
| `report.md` | 完整理论与实验报告 |
| `lakefile.lean` | Lean4 + Mathlib 依赖配置 |

## 定理速查

### FECG_LEAN.lean
- `energy_antitone` — 能量序列单调不增
- `energy_convergent` — 能量序列收敛到下确界
- `fixed_point_of_limit` — 轨道收敛→极限为不动点

### Composite.lean
- `composite_energy_converges` — 总能量收敛
- `composite_limit_is_fixed_point` — 极限为动力学不动点
- `async_energy_converges` — 异步更新下总能量收敛
- `robust_async_energy_converges` — 有界扰动下依然收敛
- `async_limit_is_fixed` — 异步极限点满足局部不动点条件

### MultiModal.lean
- `joint_energy_converges` — 联合能量序列收敛
- `attractor_exists_on_compact` — 紧致不变集上吸引子存在
- `lasalle_stability` — Lasalle 不变性原理变体

## 与热力学框架的对应

| Lean4 定理 | 热力学含义 |
|-----------|-----------|
| `energy_convergent` | 自由能单调不增，必收敛 |
| `fixed_point_of_limit` | 吸引子 = 动力学不动点 |
| `composite_energy_converges` | 多CLFA并行系统总能量收敛 |
| `robust_async_energy_converges` | 有噪声/延迟下多智能体依然收敛 |

## CI 验证

`.github/workflows/lean.yml` — 每次 push 自动运行 `lake build` 验证所有证明。
