# Thermodynamic AGI / 热力学解析智能

> **Core Thesis**: ASI will emerge from **free-energy minimization** + **Landauer computational dissipation**.
> **核心假设**: ASI 将诞生于**自由能最小化原理**与**Landauer计算耗散**的交汇处。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub repo](https://img.shields.io/badge/GitHub-simulai%2FASI-3da639?style=flat)](https://github.com/simulai/ASI)

---

## 🗺️ Interactive Research Map

**[Open research_map.html](docs/research_map.html)** — drag nodes, hover for details, scroll to zoom.

---

## 📂 Repository Structure

```
ASI/
├── docs/
│   ├── research_map.html      ← Interactive D3.js force graph
│   ├── zh/ | en/             ← Full documentation (bilingual)
├── 01_brainstorm/            ← Raw ideas, unpolished
│   ├── zh/ | en/
├── 02_theory/                ← Formalized theory
│   ├── lean4_src/           ← FECG_LEAN Lean4 proofs
│   ├── references.md         ← Bibliography
│   └── zh/ | en/
├── 03_experiments/           ← FARS toy experiments
├── 04_papers/               ← Paper drafts
└── 05_submissions/          ← Submission tracker
```

---

## 📚 Documentation

| Document | EN | ZH |
|----------|----|----|
| README | this file | [docs/zh/README_zh.md](docs/zh/README_zh.md) |
| Core Narrative | [docs/en/narrative_en.md](docs/en/narrative_en.md) | [docs/zh/narrative_zh.md](docs/zh/narrative_zh.md) |
| Research Map (static) | [docs/en/map_en.md](docs/en/map_en.md) | [docs/zh/map_zh.md](docs/zh/map_zh.md) |
| Interactive Map | **[docs/research_map.html](docs/research_map.html)** | — |
| H1–H5 Hypotheses | [02_theory/en/h1_h5_en.md](02_theory/en/h1_h5_en.md) | [02_theory/zh/h1_h5_zh.md](02_theory/zh/h1_h5_zh.md) |
| Landauer Principle | [02_theory/en/landauer_en.md](02_theory/en/landauer_en.md) | [02_theory/zh/landauer_zh.md](02_theory/zh/landauer_zh.md) |
| **Lean4 Proofs** | **[github.com/simulai/FECG_LEAN](https://github.com/simulai/FECG_LEAN)** | [02_theory/lean4_src/](02_theory/lean4_src/) |
| Bibliography | [02_theory/references.md](02_theory/references.md) | — |

---

## 🔬 Lean4 Formalization: FECG_LEAN

**Public repo**: [github.com/simulai/FECG_LEAN](https://github.com/simulai/FECG_LEAN)

Lean 4 + Mathlib machine-verified proofs of attractor dynamics:

| File | Key Theorems |
|------|-------------|
| `FECG_LEAN.lean` | `energy_antitone`, `energy_convergent`, `fixed_point_of_limit` |
| `Composite.lean` | `composite_energy_converges`, `async_energy_converges`, `robust_async_energy_converges` |
| `MultiModal.lean` | `joint_energy_converges`, `attractor_exists_on_compact`, `lasalle_stability` |

These are **theorems**, not hypotheses. If premises hold, conclusions *must* follow.

---

## 📄 Three-Paper Roadmap

| # | Paper | Status | Core |
|---|-------|--------|------|
| 1 | Complementary Pairing | ✅ Done | Helix = DNA hard bias, CTR AUC 0.716 |
| 2 | Thermodynamic Foundations | 🔄 In progress | F = Helmholtz, Landauer, NCA, **Lean4 proofs** |
| 3 | Component Library | 💡 Concept | Landauer gate + Hopfield + MetaGate + routing |

---

## 📖 Core Narrative

### The Problem

GPT-4, Claude, Gemini — all outcomes of "more is better":
> More parameters + More data + More GPUs = Better language model.

**Language models learned language. They didn't learn computation.**

MIT March 2026 proved: **164M cellular automata tokens > 1.6B English tokens.**
What was learned: **computational structure** — not language, not semantics.

### The Four Components

| Component | Physical Meaning | Evidence |
|-----------|----------------|---------|
| **Attention** | Continuous approximation of Helmholtz free-energy minimization | Statistical mechanics |
| **Helix** | DNA complementary pairing = forced low-energy attractor entry | CTR AUC 0.716, 54% fewer params |
| **MetaGate** | Curvature-triggered metacognitive interruption: when `d²F/dt²` is large, pause and introspect | Toy experiments (H3) |
| **Landauer Gate** | Physical dissipation = computational cost signal; replaces gradient as the "effort" signal | Conceptual (Paper 3) |

### Why These Four?

- **Attention**: The transformer is doing physics — it's running gradient descent on a free-energy landscape
- **Helix**: Forces the system into low-energy attractors without soft probability shortcuts — more thermodynamically efficient
- **MetaGate**: Biological analogy: the brain's Default Mode Network activates during "rest" to integrate information. MetaGate does the same: high curvature = near a phase transition = stop and think
- **Landauer Gate**: Every computation erases bits = dissipates heat. This gives AI a physical "effort" signal — it knows when it's "working hard" thermodynamically

### ASI = Most Intelligent Under Thermodynamic Constraints

**Strongest ASI ≠ largest model. Strongest ASI = most intelligent within finite resources & time.**

Landauer (1961): each bit erased = kT·ln2 dissipated.
This is not an analogy. It is a **physical law**.

If computation has cost, then intelligence under constraints is an **optimization problem in a thermodynamic landscape** — and the best AI is the one that finds the lowest-energy attractor fastest with least dissipation.

---

## 📚 Key References

- [FECG_LEAN](https://github.com/simulai/FECG_LEAN) — Lean4 proofs
- [arXiv:2603.10055](https://arxiv.org/abs/2603.10055) — MIT NCA pre-pre-training (2026)
- [Landauer 1961](https://doi.org/10.1147/rd.53.0163) — Irreversibility and Heat Generation
- [Friston 2010](https://doi.org/10.1038/nrn2787) — Free Energy Principle: A Unified Brain Theory
- Full bibliography: [02_theory/references.md](02_theory/references.md)

---

## ⚖️ License

MIT — free to use, build on, argue with.
