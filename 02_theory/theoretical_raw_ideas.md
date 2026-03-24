# Theoretical Raw Ideas — Thermodynamic AGI

> 规则：随手记，不判断，不要求完整，不怕矛盾。防止好想法被忘记，也防止同一个想法两个月后再"发现"一遍。

---

## 2026-03-24

### Idea-001: FEP / Landauer / Shannon 的 KL 统一基底

**来源**: GPT 分析 + 与 AI 的多次交流

**核心内容**:
- 三者共享同一个数学对象：`D_KL(q‖p)`
- FEP: `D_KL(q_{t+1} ‖ p_eq)` (nats)
- Landauer: `W_min = k_B·T·D_KL(p‖q)` (joules)
- Shannon: `D_KL(p‖U)` — 相对均匀分布
- `k_B·T` = 信息↔热力学的"汇率"

**已有类似工作**（已复核 URL）：
- Reeb & Wolf (2014): "An improved Landauer principle with finite-size corrections" — NJP 16 103011. URL: https://arxiv.org/abs/1306.4352
- Sagawa & Ueda (2009): "Minimal Energy Cost for Thermodynamic Information Processing" — PRL 102 250602. URL: https://arxiv.org/abs/0906.3448
- Sagawa & Ueda (2012): "Thermodynamics of information" — Nature Physics 8, 264. URL: https://www.nature.com/articles/nphys2254
- Horowitz & Sandberg (2014): "Second-law-like inequalities with information" — URL: https://arxiv.org/abs/1409.5351
- Parrondo, Horowitz & Sagawa (2015): "Thermodynamics of information" — URL: https://arxiv.org/abs/1410.0257
- Friston (2006+): FEP 论文群 — 框架已有，但没有用信息几何做 FEP/Landauer 统一严格化

**Novelty 边界**: 已有工作全部在连续时间/马尔可夫链框架；我们做离散粗粒化 + 拓扑修正，边界清晰

**决策**: 值得形式化 — 需明确 novelty：离散粗粒化视角 + ΔF_topo 拓扑修正

---

### Idea-002: DTS 压缩有效 KL 距离

**来源**: 基于 DTS shortcut 定理的推论

**核心内容**:
- 局部扩散（马尔可夫链）在高维空间的有效 KL 距离 ~ O(n)
- DTS shortcut 通过非局部跳变，将有效 KL 距离压缩到 O(1)
- 这解释了为什么 DTS 在高维能量景观中比纯梯度下降更快逃离局部极小

**已有类似工作**: 未发现

**Novelty**: 高 — DTS 的信息几何解释，目前未见文献

**决策**: 不强行形式化（目前只是 heuristic）；作为可检验假说写入 Paper 2 Introduction

---

### Idea-003: Scale Operator 的拓扑修正 ΔF_topo

**来源**: ScaleOperator.lean 的形式化过程中发现

**核心内容**:
- 微观→宏观粗粒化过程中，拓扑不变量（β₀ 同调群）携带信息
- 这部分信息不能被自由能项吸收，因此产生额外修正项
- `ΔF_topo = α · β₀ · ⟨|κ|⟩` 其中 `α` 是粗粒化尺度，`β₀` 是第零同调群维度

**状态**: 已在 Lean4 中部分形式化，3 个 sorry 未填

**决策**: 继续推进 — 填完 sorry，完成 ΔF_topo 定理

---

### Idea-004: Scale Operator + DTS 的协同效应

**来源**: Idea-002 + Idea-003 的组合

**核心内容**:
- Scale Operator 做宏观粗粒化（降低状态空间维度）
- DTS 在宏观空间做非局部跳（压缩有效 KL 距离）
- 两者结合：从微观→宏观→非局部跳，是完整的"能量景观导航"管道
- 形式化的"管道效率"定理：每一步的信息损失有上界

**已有类似工作**: 未发现

**决策**: 有 novelty，需要具体定理支撑后再推进

---

### Idea-005: 代码叠加态 — "专利翻译"作为 AGI 代码生成目标（2026-03-24）

**来源**: 与 AI 关于 FEP + 代码生成的讨论

**核心洞察**: 把代码生成目标从"生成正确代码"改为"翻译推理路径"

> 大模型走过的路，我们重新走一遍。

- 专利 = (问题陈述) → (推理路径) → (最终公式/代码)
- 翻译 = 把自然语言推理路径转成 Lean4 证明 → 强制模型把完整推理"说出来"
- 优势：过程本身是 ground truth，结果难验证，过程好记录

**热力学解释**：
$$F(\text{推理路径}) = -\log p(\text{结论}|\text{路径}) + D_{\text{KL}}(q_\theta(\text{路径}|\text{问题}) \| p(\text{最优路径}))$$

- 能量景观作用：不是直接生成代码，而是给推理路径打分
- Landauer 耗散 = 推理路径的复杂度 → 越"正确"的推理，耗散越低

**组件可行性**：

| 组件 | 可行性 | 主要障碍 |
|------|--------|---------|
| AST → 语义 latent space | 中高 | 需要大规模 code corpus 对比学习预训练 |
| Energy-guided Neural ODE | 中 | 语义 loss 不平滑，需 jump-diffusion 改造 |
| STE 桥 | 高 | 工程成熟 |
| Abstract Interpretation | 低（general）/高（受限） | 先做类型+作用域，做减法 |

**实现路径**: 先在代码补全任务上验证"语义 latent space + energy flow"是否优于 next-token prediction，再逐步加入 STE 和 abstract feedback

**状态**: 想法（未验证）

**决策**: 长期目标（5-10年），近期可做消融验证 — 建议标记为 ASI 时代工具

---

## 决策准则（2026-03-24 确立）

| 类型 | 立刻做 | 等证据 | 永远不做 |
|------|--------|--------|---------|
| 已有类似工作的想法 | 先做文献调研，明确 novelty 边界 | 积累证据后再形式化 | 重复发明轮子 |
| 新的 heuristic 推断 | 写入 Paper 作为可检验假说 | 积累实验/理论支撑 | 强行形式化 |
| 与现有形式化工作直接相关的想法 | 推进 Lean4 证明 | — | — |

**Novelty 判断标准**：
- 已有文献做连续时间马尔可夫链 → 我们做离散时间粗粒化 → 可能 novel
- 组合视角（Scale + DTS）→ 需要具体定理 → novelty 待评估
- 全新信息几何 claim（DTS 压缩 KL）→ 直接 claim，无需引用

---

## FARS Research Workflow（研究自动化系统）

### 参考系统

**Analemma AI FARS GitLab** — Fully Automated Research System:
- 每步实验都有 Proceed / Refute / Pivot 条件
- Claims-first: 每个 figure/table/section 映射到具体 Claim
- Decision Rules: plan.json 每步实验都有判定条件

**本项目的 FARS Research Skill**:
- 自动跟踪 theoretical_raw_ideas.md 状态
- 定期复核文献 URL 有效性
- 根据决策准则自动路由到不同处理轨道
- 有成果时主动推送 GitHub

### 轨道路由

```
New Idea
  ├─ 有 prior art? → 补充 URL → novelty 评估 → 明确边界
  └─ 无 prior art?
        ├─ 有形式化基础? → 推进 Lean4 证明
        └─ 无形式化基础?
              ├─ 有实验数据? → 写入 Paper claim
              └─ 无实验数据? → 记录，待积累
```

### Cron 触发机制

- 每 6 小时检查 theoretical_raw_ideas.md 中有待处理 idea
- 有 pending sorry → 尝试推进 Lean4 证明
- 有 Idea-002 级别新想法 → 自动写入 Paper proposal
- CI 通过时 → 推送最新状态
