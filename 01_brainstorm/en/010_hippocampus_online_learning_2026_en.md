# Hippocampus-Equivalent Algorithms in 2026: Online Learning Alternatives

> Source: 2025–2026 arXiv latest papers survey
> Compiled by: FARS Automatic Research System
> Date: 2026-03-23

---

## Core Problem

Current approaches:

| Approach | Learn during inference? | Cost |
|----------|------------------------|------|
| Standard Transformer | ❌ Frozen weights | No online learning |
| Hopfield Network | ❌ Train once, read only | No incremental learning |
| KV-Cache | ⚠️ Cache only, no new patterns | Cannot generalize |
| **Hippocampus itself** | ✅ Fully online | — |

What we need: **inference-time online learning + new memory storage + anti-forgetting + thermodynamic efficiency**

---

## 2026 State-of-the-Art

### Option 1: HiPPO Zoo ⭐ Most Relevant (Feb 2026)

**Paper**: Goffinet, Hanks & Carlson (2026) — *HiPPO Zoo: Explicit Memory Mechanisms for Interpretable State Space Models*
**arXiv**: `2602.21340`

**This is the most directly relevant paper found.**

Core idea: The HiPPO framework (Gu & Dao et al.) compresses sequential history via orthogonal polynomial bases, but memory mechanisms have always been implicit. HiPPO Zoo makes them explicit:

- **Adaptive memory allocation**: doesn't pre-set capacity, dynamically allocates
- **Associative memory**: given partial input, retrieves complete memory pattern
- **Online training**: efficient streaming setting training, real-time weight updates
- **Interpretable**: memory structure is explicit, not a black box

**Correspondence to hippocampus**:
- HiPPO polynomial bases ≈ hippocampus's **orthogonalized representations**
- Adaptive allocation ≈ hippocampus's **scene-specificity** (new cell groups activate for new scenes)
- Associative memory ≈ hippocampus's **pattern completion**

**Why it matters**:
> First paper to make SSM memory mechanisms **explicit and interpretable**, with online learning support. Equivalent to upgrading Mamba into "Mamba with hippocampal memory."

---

### Option 2: Memento — Case Memory Online RL (Aug 2025)

**Paper**: Zhou et al. (2025) — *Memento: Fine-tuning LLM Agents without Fine-tuning LLMs*
**arXiv**: `2508.16153`

Core design: **Memory-augmented Markov Decision Process (M-MDP)**

- **Episodic memory**: stores past experiences, differentiable or non-parametric
- **Neural case-selection policy**: learns to select the most relevant cases from memory
- **Policy improvement through memory retrieval**: no gradient updates needed, enables continuous real-time learning
- **Out-of-distribution tasks: +4.7–9.6%**

**Performance**:
- GAIA top-1: 87.88% Pass@3
- DeepResearcher: 66.6% F1, 80.4% PM
- **Outperforms training-based methods** without fine-tuning the base LLM

**Why it matters**:
> Truly implements "inference-time learning" for LLM agents — doesn't change model weights, only uses case memory for continuous adaptation. Exactly corresponds to hippocampus's **episodic memory + experience-driven adaptation**.

---

### Option 3: PhiNets — CA3/CA1 Dual Predictor Architecture (2024-2025)

**Paper**: Ishikawa et al. (2024-2025) — *PhiNets: Brain-inspired Non-contrastive Learning Based on Temporal Prediction Hypothesis*
**arXiv**: `2405.14650`

Core design: simulating hippocampus **CA3 → CA1** dual pathway:

- **CA3 predictor** (compressed representation like autoencoder) ≈ hippocampus CA3 (associative memory)
- **CA1 predictor** (preserves temporal details) ≈ hippocampus CA1 (output to cortex)
- **X-PhiNet**: with momentum encoder, adapts faster to new patterns
- **Continual + online learning**: adapts to new patterns faster than standard SimSiam

**Direct correspondence to hippocampus**:
- CA3 compression ≈ Hopfield attractor low-energy states
- CA1 temporal fidelity ≈ memory's temporal ordering
- Dual predictor structure ≈ hippocampus's two parallel pathways (direct perforant path + trisynaptic circuit)

---

### Option 4: Online-LoRA / TreeLoRA — Parameter-Efficient Continual Learning (2025)

**Papers**:
- Online-LoRA (`arXiv:2411.05663`) — task-free online continual learning
- TreeLoRA (`arXiv:2506.10355`) — hierarchical gradient-similarity guided LoRA

Core idea: **Don't modify original weights, only update lightweight adapters**

- Catastrophic forgetting's root problem: full-parameter fine-tuning overwrites old knowledge
- LoRA's solution: freeze original weights, only train low-rank adapters
- Online-LoRA further: no need to know task boundaries in advance, detects and adapts online
- TreeLoRA: uses hierarchical gradient tree to guide which LoRA to update and which to preserve

**Implications for hippocampus**:
- LoRA ≈ hippocampus's **synaptic plasticity** (reinforces specific connections only, doesn't change overall structure)
- Online LoRA ≈ hippocampus's **fast synaptic reinforcement** (CA3 one-shot learning)
- Tree structure ≈ hippocampus's **organizational hierarchy** (Dentate Gyrus → CA3 → CA1)

---

### Option 5: DMA — Online RAG Alignment (Nov 2025)

**Paper**: Bai et al. (2025) — *DMA: Online RAG Alignment with Human Feedback*
**arXiv**: `2511.04880`

Core design: **online RAG + human feedback closed loop**

- Doesn't train offline — **receives human feedback in real-time** to update retrieval strategy
- Retrieval quality = user feedback signal
- Online optimization of retrieval + generation alignment

**Why it matters**:
> Implements "hippocampal navigation feedback signal" in RAG — hippocampus continuously calibrates spatial representations via place cell feedback, DMA continuously calibrates retrieval strategy via human feedback.

---

### Option 6: KVCOMM — Multi-Agent Online KV-cache Communication (NeurIPS 2025)

**Paper**: Ye et al. (2025) — *KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems*
**arXiv**: `2510.12872` (NeurIPS 2025)

Core design: **Inference-time online KV-cache sharing across agents**

- Multiple agents don't replicate weights — **share attention states instead**
- Online negotiation on which KV-cache to pass, which to discard
- 10x reduction in communication overhead

**Correspondence to hippocampus**:
- KV-cache sharing ≈ hippocampus's **memory sharing** (multiple individuals in a group sharing experiences)
- Online negotiation ≈ hippocampus's **replay mechanism** (replays memories to other brain regions during sleep/rest)

---

## Comprehensive Comparison

| Approach | Online Learning | Associative Memory | Anti-Forgetting | Interpretable | Difficulty |
|----------|----------------|-------------------|----------------|--------------|------------|
| **HiPPO Zoo** | ✅ Streaming | ✅ Explicit | ✅ Adaptive | ✅ All | Medium |
| **Memento** | ✅ Zero-gradient | ✅ Case retrieval | ✅ Case buffer | Partial | Low |
| **PhiNets** | ✅ Online | ✅ CA3 compression | ✅ Contrastive reg | Partial | Medium |
| **Online-LoRA** | ✅ Online | ❌ None | ✅ Low-rank isolation | ✅ Visualizable | Low |
| **DMA** | ✅ Online | ⚠️ RAG | ⚠️ Data-dependent | Partial | Low |
| **KVCOMM** | ✅ Online | ⚠️ Shared cache | ⚠️ None | Partial | Medium |

---

## Priority: HiPPO Zoo + Memento Combination

**Why this combination is optimal**:

```
HiPPO Zoo (bottom-layer SSM)
    ↓ Associative memory + adaptive allocation
    ↓ Stores new scenes in low-energy states
    ↓
Memento (upper-layer case memory)
    ↓ Policy improvement via case retrieval
    ↓ No gradient updates needed
    ↓
Landauer Gate (cost sensing)
    ↓ Perceives dissipation of each memory retrieval
    ↓ Decides whether storing new cases is worth it
```

**Why this combination is equivalent to the hippocampus**:

| Hippocampus Function | HiPPO Zoo + Memento Implementation |
|---------------------|----------------------------------|
| Place cells (spatial encoding) | HiPPO orthogonal polynomial bases |
| Grid cells (periodic metric) | SSM recurrent state updates |
| Pattern separation (DG) | HiPPO adaptive allocation |
| Associative memory (CA3) | Memento case memory retrieval |
| Pattern completion | HiPPO associative memory |
| Output to cortex (CA1) | Mamba SSM output layer |

---

## Papers to Download

| Paper | arXiv ID | Local Path |
|-------|---------|-----------|
| HiPPO Zoo | `2602.21340` | Pending |
| Memento | `2508.16153` | Pending |
| PhiNets | `2405.14650` | Pending |
| Online-LoRA | `2411.05663` | Pending |
| TreeLoRA | `2506.10355` | Pending |
| DMA | `2511.04880` | Pending |
| KVCOMM | `2510.12872` | Pending |
