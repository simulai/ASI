# Thermodynamic AGI — Research Map

> Last updated: 2026-03-23
> Core thesis: **Strongest ASI = smartest within finite resources & time** = optimal attractor under thermodynamic constraints

---

## Position Map

```
Computational Abstraction (concrete ← → universal)
                │
  High          │  Helix (DNA)
  Thermodynamic  │  Landauer Gate
  Constraint    │  Hopfield Attractor
                │
  Low           │  Standard Attention  NCA Pre-train (MIT 2026)
  Thermodynamic │  LLM Scaling
  Constraint    │
                └─────────────────────────────────────
                          Thermodynamic Constraint (weak ← → strong)

[Current frontier]
                     ·
  Hard Inductive     ·   NCA (MIT 2026) — computational structure transfer
  Bias               ·
                     · Landauer dissipation
  Soft Probabilistic ·
                     · Standard Transformer
[Legacy NLP]
```

---

## Key Nodes

### Core Layer (Ours)

| Paper | Status | Core Contribution |
|-------|--------|-------------------|
| Paper 1: Complementary Pairing | ✅ Done | Helix = DNA hard inductive bias, CTR AUC 0.716 |
| Paper 2: Thermodynamic Foundations | 🔄 In progress | F = Helmholtz free energy, Landauer + NCA external validation |
| Paper 3: Component Library | 💡 | Landauer gate + Hopfield + Complementary gate + Routing |

### Supporting Layer (Referenced)

| Work | Relationship |
|------|-------------|
| MIT NCA Pre-train (arXiv:2603.10055, 2026) | External validation: computational structure transfer |
| Hopfield Networks (1982) | Energy function foundation; we approximate with Attention |
| Helmholtz Machine | Free-energy variational inference, theoretical root |
| Landauer (1961) | Computational dissipation principle, core of L3 |
| Platonic Representation Hypothesis (Isola 2024) | Cross-modal representation convergence → supports cross-domain transfer |
| Complementary Learning Systems (McClelland et al.) | Dual memory systems → neuroscience basis for Helix |

### Competitive Layer (Same direction, different path)

| Work | Difference |
|------|-----------|
| DeepMind DreamerV3 | World model, no thermodynamic framing |
| Voyager/AutoGPT | L3 planning, no physical grounding |
| MoE Scaling (Jelassi 2025) | MLP expansion → memory; we use Landauer → reasoning |
| Knowledge Distillation / Pruning | Compress model; we use thermodynamics to find optimal sub-structure |

---

## Research Gaps We Fill

### Gap 1: No Evaluation Standard for L3 World Models
**Status quo**: VLMEval/GAIA measure task completion, not world-model quality.
**Our contribution**: Energy landscape curvature as world-model quality signal.

### Gap 2: No Physical Interpretation of Attention
**Status quo**: Attention = softmax(QK^T), empirically effective, physically vague.
**Our contribution**: Attention = continuous approximation of Helmholtz free-energy minimization.

### Gap 3: No Unified Mechanism for Compositional Generalization
**Status quo**: L2→L3 jump via prompt engineering, no theory.
**Our contribution**: Helix complementary pairing = forced low-energy state = bypasses compositional explosion.

### Gap 4: No Resource Awareness in Multi-Agent Systems
**Status quo**: ChatDev/SWE-agent loop infinitely.
**Our contribution**: Landauer dissipation as "computational cost signal" → triggers MetaGate interruption.

---

## Architecture Diagram

```
              ┌──────────────────────────────────────────────┐
              │          Thermodynamic AGI                    │
              │  (Free-Energy Minimization + Landauer Cost)   │
              └──────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
    Free Energy F          Landauer ε              Attractor 𝔸
  (Helmholtz var.)        (bit cost)            (state conv.)
        │                       │                       │
   ┌────┼────┐            ┌───┼────┐            ┌────┼────┐
   │    │    │            │    │    │            │    │    │
Attention Helix     MetaGate  LandauerGate  EnergyLandscape CurvatureMeta
(cont. approx.)  (hard pair)  (introspection) (new component)  (F theory) (MetaGate)
```

---

## Competitive Moat

Rare combination of expertise:
1. Free-energy variational inference (theoretical physics)
2. Landauer dissipation (information theory + thermodynamics)
3. Transformer training (engineering)
4. Cellular automata dynamics (complexity science)

**Helix on KDD Cup TAAC verified (AUC 0.716)** — reproducible evidence.
The *thermodynamic framing* is the壁垒 (barrier): hard to replicate without all four domains.

---

## Next Opportunities

1. **NCA + Helix connection**: Feed NCA trajectories into Helix; test if better than standard Attention
2. **MetaGate + Multi-Agent**: Test Landauer-dissipation-triggered metacognition on ChatDev/SWE-agent
3. **Paper 2 submission**: Integrate MIT NCA work → strengthen external validation narrative
4. **Landauer Gate chip**: FPGA physical implementation; verify real energy vs. theoretical prediction

---

*This map is a living document — updated with each new insight.*
*Maintained by FARS automatic research system.*
