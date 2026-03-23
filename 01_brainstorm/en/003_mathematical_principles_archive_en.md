# Mathematical Principles of Intelligence — Archived

> **Predecessor repo**: https://github.com/simulai/Mathematical-Principles-of-Intelligence
> **Archived**: 2026-03-23
> **Status**: Archived; content integrated into ASI Thermodynamic AGI framework

---

## Core Contributions

| Proposition | Core Content | Connection to ASI |
|------------|-------------|------------------|
| **e-base Scaling Law** | Optimal branching factor for info transmission efficiency = e ≈ 2.718 | Thermodynamic version of scaling law; ASI interprets this as optimal computation structure under Landauer constraint |
| **Cognitive Holonomy ℋ** | Conserved topological charge in cognitive state space, constrains entropy production | Topological invariant of free-energy landscape; isomorphic to attractor basin topology |
| **"Vice is Virtue" Principle** | Memristor hardware defects (noise, drift) are computational assets | Landauer dissipation perspective: noise = byproduct of information erasure ≠ pure cost |
| **Zero-Dissipation Limit** | Δℋ = 0 → ΔE → 0 | ASI L3 MetaGate goal: high curvature triggers introspection = reduces invalid state transitions = tends toward zero dissipation |
| **Generalized Cognitive Thermodynamics** | TΔS + ΔE + μΔℋ ≥ 0 | ASI core inequality: 2nd law + free energy + topological conservation |

## Empirical Validation

- **Kaggle Disaster Tweets**: F1 = 0.82868 (single DistilBERT)
- **DeepSeek mHC Alignment**: Theoretical predictions consistent with DeepSeek-AI mHC
- **Ricci Flow Learning**: "Eureka" moments visualized during phase transitions

## Lean4 Formalization

- `EBase.lean`: e-base scaling law proof
- Archived: `lean_playground/LeanPlayground/EBase.lean`

## Why Integrate Into ASI

ASI is the **mature version** of Mathematical Principles:

```
Mathematical Principles (2025-12)          ASI (2026-03)
├── e-base scaling (exploratory)    ──────→  scaling law → Landauer constraint
├── Cognitive Holonomy ℋ (prototype) ──────→  attractor topology → Free Energy Principle
├── "Vice is Virtue" (intuition)    ──────→  Landauer dissipation = information erasure cost
├── Kaggle F1=0.828 (early empirics) ──────→  KDD Cup AUC=0.716 (stronger evidence)
└── Scattered documentation         ──────→  3-paper system + FARS automated research
```

## Links

- Predecessor: https://github.com/simulai/Mathematical-Principles-of-Intelligence
- ASI: https://github.com/simulai/ASI
- FECG_LEAN: https://github.com/simulai/FECG_LEAN
