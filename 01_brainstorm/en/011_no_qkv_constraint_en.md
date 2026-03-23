# The No-QKV Constraint: Forcing Systems Toward Physically Grounded Memory

> Source: In-depth discussion on why "no QKV projection" is the correct research direction
> Date: 2026-03-23

---

## Core Proposition

> **"No QKV projection" is not a restriction — it's a liberation.**
>
> It forces the system away from "soft probability catch-all" toward "physical energy + attractors + hard selection" — a path more biologically and thermodynamically grounded.

---

## 1. The Fundamental Flaws of QKV Projection

Current Transformer attention = **three linear projections (Q, K, V) + softmax** → soft routing + weighted sum.

This mechanism is extremely strong for **static knowledge extraction** (pre-training), but inherently lacks:

| Missing Capability | Physical/Biological Correspondence |
|-----------------|-------------------------------|
| Hard, energy-guided selection (no "fatigue/cost" threshold) | Lacks Landauer dissipation sensing |
| Content-addressable stable attractors (KV-cache is just linear cache, not dynamic self-organized low-energy states) | Lacks Hopfield attractors |
| Incrementally writing new memories without destroying old attractors (fine-tuning causes catastrophic forgetting) | Lacks hippocampus dual-system |

**Banning QKV forces the system to stop relying on linear projection + soft probability to "simulate" everything — it must use other mechanisms for association, retrieval, and routing.**

This pushes the problem directly to Hopfield attractors' door — because Hopfield is naturally **projection-free, energy-landscape-driven content-addressable memory**.

---

## 2. Modern Hopfield Networks = The Paradigmatic No-QKV Implementation

Research from 2020–2025 has repeatedly confirmed: modern Hopfield can **partially or fully replace** Transformer attention layers:

| Attribute | Transformer QKV | Modern Hopfield |
|---------|----------------|---------------|
| Routing | Soft probability (softmax weighted) | Energy minimization (gradient descent to attractor) |
| Memory storage | KV-cache linear cache (read/write separate, no self-organization) | Hebbian outer product update, dynamic self-organization |
| Incremental writing | Requires fine-tuning, overwrites old knowledge | Online incremental writing, capacity O(N log N) |
| Forgetting problem | Catastrophic forgetting | Ameliorated via sparse/partial forgetting |
| Cost awareness | None | Energy function inherently has "cost" term |

**Key research support**:
- Ramsauer et al. (2020): Modern Hopfield networks as attention layer — theoretical foundation
- Krotov & Hopfield (2020): Dense associative memory, higher-order interactions
- Linear Attention as Iterated Hopfield: Linear attention is essentially continuous Hopfield iteration
- Outlier-Efficient Modern Hopfield: Plug directly into large Transformers, solves outlier problem

---

## 3. Perfect Alignment with the Four Components

With QKV banned, all four components have a clearer implementation path:

### Hopfield Attractor → KV-Cache Upgrade

- KV-cache: passive linear storage, read/write separate, no self-organization
- Hopfield: active energy basin — new experiences online iterative update (Hebbian), automatically converge to stable low-energy state

### Emergent Routing → Winner-Take-All Energy Competition

- Original design: dynamically decide which module handles this input
- QKV-free upgrade: **whichever expert/module's attractor converges first, wins** (winner-take-all via energy)
- No softmax soft allocation — hard selection within the energy landscape

### Complementary Gate → Hard Lateral Inhibition

- Original design: complementary pairing, selective information on/off
- QKV-free upgrade: **hard lateral inhibition**, not soft softmax
- Analogy: DNA double helix hard pairing (A-T, C-G), not probabilistic soft binding

### Landauer Gate → Explicit Term in Energy Function

- Original design: perceive computation cost, trigger MetaGate introspection
- QKV-free upgrade: **Landauer-like cost explicitly in Hopfield energy function**
- Each state update = each dissipation, cost directly encoded in dynamics

**Result**: the entire system becomes a **fully energy-landscape-driven closed loop**, not a probability cloud.

---

## 4. Implementation Paths and Risks

### Recommended Experimental Path

**Step 1: Small-scale validation**
Replace self-attention in a small Transformer with a **modern Hopfield layer**:
- Reference Ramsauer 2020 or Krotov-Hopfield series
- Compare on simple tasks (memory retrieval, pattern completion, incremental learning)

**Step 2: Continual learning test**
Sequentially feed different tasks, compare forgetting rates:
- vs RAG (external memory)
- vs LoRA (parameter-efficient fine-tuning)
- vs HiPPO Zoo/Memento (online learning SSM)

**Step 3: Add thermodynamic cost**
Include Landauer-like cost in Hopfield energy function:
- Penalize large norm updates
- Each state update explicitly counts dissipation
- Test whether "cost sensing" improves system stability

**Step 4: Radical version (all-Hopfield)**
Reference STanHop-Net-style work, completely discard QKV, use pure Hopfield dynamics.

### Risks to Watch

| Risk | Mitigation |
|------|----------|
| **Capacity vs. stability**: too-correlated patterns produce spurious attractors | Sparse Hopfield, partial forgetting |
| **Computational overhead**: iterative convergence may be slower than softmax | Use dense associative memory, or use Hopfield only at critical layers |
| **Training difficulty**: end-to-end gradients may struggle | Hybrid: Transformer backbone + Hopfield memory plugin |

---

## 5. Core Conclusion

> **Banning QKV = transforming Transformer from "universal soft probability simulator" to "energy-landscape-driven physical machine."**

This is not regression — it's **returning to physical reality**. Real neurons don't execute matrix multiplication plus softmax. They execute threshold dynamics driven by ionic concentration gradients.

Our four components (Landauer + Hopfield + Complementary Gate + Emergent Routing) are precisely the minimal toolset for realizing this transformation.

**The critical next experiment**: build a **no-QKV prototype** proving that energy-driven attractors genuinely outperform QKV soft probability on incremental learning tasks.
