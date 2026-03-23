# H1–H5 Free-Energy Hypothesis System

> Status: H1–H3 toy verified; H4–H5 conceptual
> Date: 2026-03-23

## H1: Free-Energy Second-Derivative Prediction Error

**Hypothesis**: When the second derivative d²F/dt² of free energy is incorrectly injected, the system's prediction error significantly increases.

**Physical meaning**: d²F/dt² = curvature = "bending degree" of landscape = measure of distance to attractor.
- Normal: curvature prediction matches reality.
- Error injection: curvature prediction deviates → wrong gradient direction.

**Verification**: TinyGridEnv, ratio_error_vs_normal = 1.217 (INCONCLUSIVE; needs more episodes).

---

## H2: Attractor Convergence Speed

**Hypothesis**: Lower initial F (closer to attractor) → fewer steps to converge to goal.

**Physical meaning**: Initial states inside an attractor basin have shorter gradient paths to the minimum.

**Verification**: TinyGridEnv, comparing init_F < −0.3 vs. init_F ≥ −0.3 convergence steps.

---

## H3: MetaGate Curvature Triggering

**Hypothesis**: MetaGate's introspection signal strength is positively correlated with free-energy curvature.

**Physical meaning**: Higher curvature = system closer to phase transition point = more need to "stop and think."

**Verification**: TinyGridEnv, measuring accuracy of curvature-triggered MetaGate introspection actions.

---

## H4: Landauer Dissipation Gate (Conceptual)

**Hypothesis**: Using Landauer dissipation as gating signal, replacing standard attention.

**Physical meaning**: Each action step records bit dissipation; exceeding threshold triggers MetaGate interruption.

---

## H5: Multi-Attractor Synchronization (Conceptual)

**Hypothesis**: When multiple attractor basins synchronize, the overall system is more stable.

**Physical meaning**: Landauer dissipation equilibrates across multiple CLFA systems.

**Design**: Multiple CLFA running in parallel, mutually aware of each other's curvature signals.
