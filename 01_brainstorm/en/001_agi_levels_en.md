# AGI Levels — Comprehensive Insights

> Source: AGI Levels Systematic Survey
> Compiled by: FARS Automatic Research System
> Date: 2026-03-23

---

## L1: Emergent Intelligence

**Representatives**: GPT-2/3/4, Claude, Gemini
**Benchmark**: ImageNet, SST-2 (mature)

### Core Technologies
- Attention / Transformer
- Pre-training + Scaling
- In-context learning

### Core Capability
In-distribution generalization: performs well on seen patterns.

### Core Bottlenecks
- Long-tail / out-of-distribution failure
- Compositional generalization:记住了见过 → 无法合成未见
- Hallucination (World Model inconsistency)

---

## L2: Intuitive Intelligence

**Representatives**: GPT-4 + RAG + Tool use
**Benchmark**: VLMEval / GAIA (but measures task completion rate, **NOT** World Model quality)

### Core Technologies
- World Model (世界模型)
- Planning
- RAG / Tool use

### Core Capability
Out-of-distribution generalization: has goals, can decompose into subtasks.

### Core Bottlenecks
- Hallucination detection (World Model inconsistent with reality)
- **No reliable standard** for validating and evaluating World Model quality
- Relies on prompt engineering, lacks physical grounding

### Key Insight
**Benchmark Mismatch**: VLMEval/GAIA measure task completion, but the L2→L3 gap is fundamentally about World Model quality, not completion rate.
World Model quality should be measured by:
- Prediction error on unseen dynamics
- Zero-shot generalization to new tasks
- Abstraction level of representations

---

## L3: Intentional Intelligence

**Representatives**: AutoGPT, Voyager, SWE-agent, Devin
**Benchmark**: SWE-bench / HumanEval (measures task completion, not World Model quality)

### Core Technologies
- Meta-Learning
- Self-Evolution
- Autonomous planning and exploration

### Core Capability
Learning to learn; autonomous exploration on complex tasks not covered in training.

### Devin Key Data (2024)
- SWE-bench: Devin 13.86% vs GPT-4 3.97%
- HumanEval: Devin 25.22% vs GPT-4 3.97%
- Gains come from **agentic architecture**, not base model quality improvement

### Core Bottleneck
**Inf Loop (infinite loop) is the fundamental problem of L3+ agents**
- No resource awareness: doesn't know how much compute has been consumed
- No self-correction: cannot autonomously discover errors
- No World Model evaluation standard

### Key Insight
Devin's gains = agentic architecture, not larger models
→ L3's bottleneck is **architectural design**, not Scale

---

## L4: Reflexive Intelligence

**Representatives**: Researcher-agent, Scientist-agent
**Benchmark**: Non-existent

### Core Technologies
- Meta-Learning
- Self-Correction (metacognitive self-correction)

### Core Capability
Self-improvement; learning to adjust one's own learning strategies.

### Core Bottlenecks
- **Poor resource awareness in multi-agent** (ChatDev/SWE-agent infinite loops)
- Value Alignment
- No thermodynamic "cost signal"

### Key Insight
L4 multi-agent bottleneck = **no computational cost signal**:
- Doesn't know how much resource each action consumed
- No mechanism to proactively interrupt when cost is too high
- Landauer dissipation = natural "resource awareness signal"

---

## L5: Organizational Intelligence

**Representatives**: Does not yet exist (2026)
**Benchmark**: Non-existent

### Core Technologies
- Multi-Agent
- Value Alignment

### Core Bottlenecks
- Goal alignment
- Resource allocation
- No proven multi-agent collaboration yet

---

## Cross-Level Technology Comparison

| Level | Core Technology | Missing |
|-------|----------------|---------|
| L1 | Attention, Transformer, Scaling | No compositional generalization |
| L2 | World Model, Planning | World Model quality unmeasurable |
| L3 | Meta-Learning, Self-Evolution | Inf loops, no resource awareness |
| L4 | Multi-Agent, Alignment | No resource cost signal |

---

## Key Insight: System 1 vs System 2

- **System 1** (L1): Fast, automatic, unconscious = Attention / pattern matching
- **System 2** (L3): Slow, conscious, logical = World Model + Planning + Meta-Learning

L2→L3 = jump from "intuitive matching" to "intentional planning"
Obstacle: **no physical foundation**, all prompt engineering

---

## Key Insight: Training Scaling vs Inference Scaling

| | Training Scaling | Inference Scaling |
|---|---|---|
| Representative | GPT-3 (Chinchilla) | OpenAI o1 |
| Core | compute-optimal | more inference = better reasoning |
| Law | LLM scaling law | Inference scaling law (different!) |

---

## Key Insight: Energy Comparison

| System | Energy |
|--------|--------|
| Human brain | ~20W |
| Claude conversation | ~3Wh/turn |
| Google AI total | 10× human brain (~200W) |
| One LLM training run | hundreds of kilowatts |

**Key insight**: Inf Loop = infinite energy drain.
Lack of resource awareness → L3+ agents may waste massive compute in ineffective loops.

---

## Key Insight: Embodied Cognition

**Embodied hypothesis**: Physical interaction produces more stable World Model.

- Embodied AI: more reliable World Model, but **extremely high energy cost**
- Digital AI: lower energy, but World Model depends on language priors

**Core question** (directly related to our research):
> Under energy constraints, is there a **Pareto optimal** between embodiment frequency and World Model quality?

Thermodynamic modeling:
- Embodiment interaction = reduces free-energy gradient
- Each interaction = Landauer dissipation cost
- Pareto frontier = balance between free-energy minimization + dissipation minimization

---

## Key Insight: Modularity as AGI Foundation

**Why modularity is indispensable**:
1. **Knowledge organization**: modularity systematizes complex knowledge
2. **Parallel development**: independent modules can iterate separately
3. **Specialized optimization**: each module can be targeted for improvement
4. **Interpretability**: module boundaries = causal boundaries

→ This is exactly the core thesis of Paper 3 (Component Library):
Landauer gate + Hopfield + Complementary gate + Routing = thermodynamic implementation of modularity.

---

## Mapping to Our Thermodynamic Framework

| AGI Level | Thermodynamic Interpretation |
|-----------|------------------------------|
| L1 | Attractor basin in free-energy landscape |
| L2 | Basin edges between attractors (compositional generalization failure point) |
| L3 | Saddle-point transitions between attractors (requires World Model navigation) |
| L4 | Curvature-triggered MetaGate introspection |
| L5 | Synchronization and competition in multi-attractor systems |

| Problem We Solve | Position in AGI Framework |
|-----------------|--------------------------|
| World Model quality evaluation | Core of L2→L3 gap |
| Attention = physical approximation | Physical grounding for L1 |
| MetaGate curvature introspection | Resource awareness for L4 |
| Landauer dissipation | Computational cost signal at all levels |
| NCA computational structure transfer | Physical explanation for L2→L3 |
