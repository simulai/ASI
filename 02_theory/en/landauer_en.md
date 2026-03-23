# Landauer Computational Dissipation Principle

> Source: Rolf Landauer (1961), "Irreversibility and the Generation of Heat"
> Compiled: 2026-03-23

## Core Formula

```
E ≥ kT · ln 2 · per-bit-erased
```

**Every bit of information erased must dissipate at least kT·ln2 energy** (≈ 0.693 kT).

Where:
- k = Boltzmann constant
- T = system temperature (Kelvin)
- ln2 = the constant linking information theory and thermodynamics

## Physical Meaning

This is an **irreversibility proof**:
- Erasing information = irreversible operation = must dissipate energy.
- Reversible operations (not erasing information) theoretically need not dissipate.

## Implications for AI

### 1. Computation Has Physical Cost
Every "computation" step — neural network forward pass or gradient descent — erases information.
This means:
- Larger models = more parameters = more bit-erasing = more energy consumption.
- Energy expended *beyond* the Landauer lower bound = waste = thermodynamic inefficiency.

### 2. Thermodynamic Interpretation of Inductive Bias
Why does "hard inductive bias" (Helix complementary pairing) sometimes beat "soft probability" (standard Attention)?

Helix complementary pairing = **forced entry into low-energy state** = reduces state-space search = fewer bit erasures = more energy-efficient = higher Landauer efficiency.

### 3. Thermodynamic Trigger for Metacognition
MetaGate = curvature-triggered introspection = pause before making a large state transition.
= Avoid large bit erasures = energy saving = self-organized criticality.

### 4. Thermodynamic Limit of LLM Scaling
When model parameter count grows large enough, the total bit-erasure per forward pass reaches a thermodynamic limit.
This is not an algorithmic problem — it is a physical one.

## Connection to Our Research

1. **H4 (Landauer Gate)**: Directly uses dissipation as gating signal.
2. **H5 (Multi-attractor synchronization)**: Multi-system Landauer dissipation equilibration.
3. **Paper 2**: Landauer is a core component of the thermodynamic framework.
4. **MIT NCA paper**: "Computational structure transfer" can be explained by Landauer dissipation.
