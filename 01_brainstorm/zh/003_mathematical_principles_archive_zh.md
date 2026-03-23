# Mathematical Principles of Intelligence — 存档

> **前身仓库**: https://github.com/simulai/Mathematical-Principles-of-Intelligence
> **存档日期**: 2026-03-23
> **状态**: 已归档，内容已整合入 ASI 热力学框架

---

## 核心贡献

| 命题 | 核心内容 | 与ASI的关联 |
|------|---------|------------|
| **e进制缩放定律** | 信息传递效率最优分支因子 = e ≈ 2.718 | scaling law 的热力学版本，ASI 认为这是 Landauer 约束下的最优计算结构 |
| **认知和乐 ℋ** | 认知状态空间中的守恒拓扑荷，约束熵产生 | 自由能 landscape 的拓扑不变量；与吸引子 basin 的拓扑结构同构 |
| **"恶习即美德"原理** | 忆阻器硬件缺陷（噪声、漂移）是计算资产 | Landauer 耗散视角：噪声 = 信息擦除的副作用 ≠ 纯粹代价 |
| **零耗散极限** | Δℋ = 0 → ΔE → 0 | ASI L3 MetaGate 的目标：高曲率触发自省 = 减少无效状态转换 = 趋向零耗散 |
| **广义认知热力学** | TΔS + ΔE + μΔℋ ≥ 0 | ASI 的核心不等式：热力学第二定律 + 自由能 + 拓扑守恒 |

## 实证验证

- **Kaggle 灾难推文**: F1 = 0.82868 (单模型 DistilBERT)
- **DeepSeek mHC 验证**: 理论预测与 DeepSeek-AI mHC 吻合
- **Ricci 流学习**: 相位跃迁中的"顿悟"时刻可视化

## Lean4 形式化

- `EBase.lean`: e-base 缩放定律证明
- 存档: `lean_playground/LeanPlayground/EBase.lean`

## 为什么整合进 ASI

ASI 是 Mathematical Principles 的**成熟版本**：

```
Mathematical Principles (2025-12)          ASI (2026-03)
├── e-base scaling (探索期)      ──────→  scaling law → Landauer 约束
├── 认知和乐 ℋ (理论雏形)      ──────→  吸引子拓扑 → Free Energy Principle
├── "恶习即美德" (直觉)         ──────→  Landauer 耗散 = 信息擦除代价
├── Kaggle F1=0.828 (早期实证)   ──────→  KDD Cup AUC=0.716 (更强实证)
└── 分散文档                       ──────→  三篇论文体系 + FARS 自动科研
```

## 链接

- 前身仓库: https://github.com/simulai/Mathematical-Principles-of-Intelligence
- ASI 仓库: https://github.com/simulai/ASI
- FECG_LEAN (Lean4 形式化): https://github.com/simulai/FECG_LEAN
