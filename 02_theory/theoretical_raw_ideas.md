# Theoretical Raw Ideas — 热力学解析智能

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

**已有类似工作**（需做文献调研确认边界）:
- **FEP 的 KL 形式**: Friston (2006+) 的 FEP 论文有这个框架，但没有用信息几何做严格统一
- **Landauer 的 KL 版本**: Reeb & Wolf (2012) JPA "A mathematical investigation of Landauer's principle" 有数学严格化；Sagawa & Ueda 的信息热力学框架（Phys Rev E/Lett 多篇）
- **信息热力学环路**: Parrondo, Horowitz, Sagawa — "Entropy production and thermodynamic irreversibility in small systems" 系列工作，明确把信息作为热力学变量

**Novelty 边界**: 已有工作主要在**连续时间马尔可夫链**框架内；我们如果做**离散时间粗粒化**（Scale Operator）视角下的统一，可能有新的贡献空间

**是否值得形式化**: 待定（需要先明确 novelty 边界）

---

### Idea-002: DTS 压缩有效 KL 距离

**来源**: 基于 DTS shortcut 定理的推论

**核心内容**:
- 局部扩散（马尔可夫链）在高维空间的有效 KL 距离 ~ O(n)
- DTS shortcut 通过非局部跳变，将有效 KL 距离压缩到 O(1)
- 这解释了为什么 DTS 在高维能量景观中比纯梯度下降更快逃离局部极小

**已有类似工作**: **未发现** — 搜索"information geometry DTS KL distance" 无直接命中

**Novelty 评估**: **高** — 这是 DTS 的信息几何解释，目前未见文献

**是否值得形式化**: **否**（目前只是 heuristic）
**是否值得做 Paper claim**: **是** — 作为可检验假说，加入 Paper 2 的 Introduction

---

### Idea-003: Scale Operator 的拓扑修正 ΔF_topo

**来源**: ScaleOperator.lean 的形式化过程中发现

**核心内容**:
- 微观→宏观粗粒化过程中，拓扑不变量（β₀ 同调群）携带信息
- 这部分信息不能被自由能项吸收，因此产生额外修正项
- `ΔF_topo = α · β₀ · ⟨|κ|⟩` 其中 `α` 是粗粒化尺度，`β₀` 是第零同调群维度
- 从 Landauer-FEP 统一视角：拓扑熵 = 信息几何中不可忽略的项

**已有类似工作**: **未发现** — 搜索"persistent homology free energy coarse-graining" 命中弱

**Novelty 评估**: **中高** — Scale Operator + 拓扑修正项的具体形式，在形式化工作中可能属于首次

**状态**: 已在 Lean4 中部分形式化，有 3 个 sorry 未填

**是否值得形式化**: **是**（已在 ScaleOperator.lean 中推进）

---

### Idea-004: Scale Operator + DTS 的协同效应

**来源**: Idea-002 + Idea-003 的组合

**核心内容**:
- Scale Operator 做宏观粗粒化（降低状态空间维度）
- DTS 在宏观空间做非局部跳（压缩有效 KL 距离）
- 两者结合：从微观→宏观→非局部跳，是完整的"能量景观导航"管道
- 可以写出形式化的"管道效率"定理：每一步的信息损失有上界

**已有类似工作**: **未发现** — 搜索"coarse-graining + dynamical systems shortcut energy landscape" 命中弱

**Novelty 评估**: **中高** — 组合视角可能新颖，但需要具体定理支撑

**状态**: 想法阶段，无任何形式化

**是否值得形式化**: 待定

---

## 决策准则（2026-03-24 确立）

| 类型 | 立刻做 | 等证据 | 永远不做 |
|------|--------|--------|---------|
| 已有类似工作的想法 | 先做文献调研，明确 novelty 边界 | 积累证据后再形式化 | 重复发明轮子 |
| 新的 heuristic 推断 | 写入 Paper 作为可检验假说 | 积累实验/理论支撑 | 强行形式化 |
| 与现有形式化工作直接相关的想法 | 推进 Lean4 证明 | — | — |

**核心原则**：不怕想法不够好，只怕想法没有被记录。记录成本接近零，忘记的代价是无法估量的。

**Novelty 判断标准**：
- 已有文献做连续时间马尔可夫链 → 我们做离散时间粗粒化 → 可能 novel
- 组合视角（Scale + DTS）→ 需要具体定理 → novelty 待评估
- 全新信息几何 claim（DTS 压缩 KL）→ 直接 claim，无需引用
