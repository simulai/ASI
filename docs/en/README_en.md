# Thermodynamic AGI

> **Core Hypothesis**: ASI (Artificial Superintelligence) will emerge from the intersection of
> **free-energy minimization** and **Landauer computational dissipation**.
> Not a bigger Transformer. Not more GPUs.
> The right physical inductive bias — the thermodynamic one.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## One-Line Pitch

**ASI = most intelligent within finite resources & time = optimal attractor under thermodynamic constraints.**

---

## Repository Structure

```
ASI/
├── docs/                     # Bilingual documentation
│   ├── zh/                   # 中文文档（中文优先）
│   └── en/                   # English documentation
├── 01_brainstorm/            # Raw ideas, unpolished
│   ├── zh/                   # Initial intuitions, unverified
│   └── en/
├── 02_theory/                # Brainstorms → formalization (1st crystallization)
│   ├── zh/
│   └── en/
├── 03_experiments/           # Toy experiments, reproducible
├── 04_papers/                # Paper drafts — one folder per paper
│   ├── paper1_complementary_pairing/
│   ├── paper2_thermodynamic_foundation/
│   └── paper3_component_library/
└── 05_submissions/           # Submission tracker + reviews
```

---

## The Core Narrative

### The Problem with Current AI

GPT-4, Claude, Gemini — all products of "more is better": more parameters, more data, more GPUs.
Scaling Laws are not wrong, but they tell us only this: **scale improves language, not computation.**

MIT's March 2026 work inadvertently proved this:

> Training on Game-of-Life-like cellular automata data — 164M tokens — outperformed 1.6B English tokens.

No semantics were encoded. What was learned was **computational structure**.
We call it: **the free-energy landscape**.

### Our Contribution

**Thermodynamic Analytical Intelligence** (Thermodynamic AGI):

| Component | Physical Interpretation | Evidence |
|-----------|------------------------|----------|
| Free Energy F | Uncertainty cost of system state | Theoretical |
| Attractor | Local minimum of F | CA/NCA dynamics |
| Attention | Continuous approximation of Helmholtz free-energy minimization | Statistical mechanics |
| Helix | DNA complementary-pairing = hard inductive bias (force binding) | CTR AUC 0.716 vs 0.632 |
| MetaGate | Curvature-triggered metacognitive interruption | Toy experiment |
| Landauer Gate | Physical dissipation as computational cost signal | Conceptual |

### MIT 2026 as External Validation

arXiv:2603.10055 (MIT CSAIL, Pulkit Agrawal lab):
- NCA pre-training → 6% perplexity reduction, 1.6× convergence speed
- Attention layers transfer best (reinit = largest loss)
- Token efficiency: 164M NCA > 1.6B English

**We provide the physical explanation**: NCA trajectories = thermodynamically pure attractor dynamics,
no semantic redundancy, each token forces pure attractor inference.

---

## Three-Paper Roadmap

| Paper | Status | Core |
|-------|--------|------|
| Paper 1: Complementary Pairing | ✅ Done, ready to submit | Helix = feature interaction bias, CTR AUC 0.716 |
| Paper 2: Thermodynamic Foundations | 🔄 In progress | F = Helmholtz free energy, Landauer dissipation, NCA external validation |
| Paper 3: Component Library | 💡 Conceptual | Landauer gate + Hopfield + Complementary gate + Routing |

---

## Competitive Moat

Few people simultaneously understand:
1. Free-energy variational inference (theoretical physics)
2. Landauer dissipation (information theory + thermodynamics)
3. Transformer training (engineering)
4. Cellular automata attractor dynamics (complexity science)

**Our moat is combinatorial scarcity of cross-domain expertise.**

Paper 1 results (Helix on KDD Cup TAAC: AUC 0.716) are reproducible.
The thermodynamic framework is the intellectual壁垒.

---

## Getting Started

```bash
# Clone
git clone https://github.com/simulai/ASI.git
cd ASI

# For Chinese documentation
cat docs/zh/README_zh.md
cat docs/zh/narrative_zh.md
cat docs/zh/map_zh.md
```

---

## Contributors

Thermodynamic AGI Research Team — powered by [FARS](https://github.com/simulai/ASI) automatic research system.

*Last updated: 2026-03-23*
