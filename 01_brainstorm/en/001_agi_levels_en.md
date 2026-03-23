# AGI Levels Framework

> Source: AGI Levels Systematic Survey
> Date: 2026-03-23
> Organized by: FARS Automatic Research System

## AGI Level 0: No Intelligence
No intelligent behavior whatsoever.

## AGI Level 1: Emergent
Passive response, no goal maintenance.
Examples: linear regression, traditional ML, basic search engines.

## AGI Level 2: Intuitive
Pattern matching + memory, emergent behavior.
**Benchmarks mature**: ImageNet, SST-2, etc.
Representatives: GPT-2/3/4, Claude, Gemini.

**Core capability**: In-distribution generalization.
**Core bottleneck**: Cannot reliably synthesize novel rules.

## AGI Level 3: Intentional
Goal decomposition, long-term planning, active exploration.
**Benchmark gap**: VLMEval/GAIA measure task completion, not world-model quality.
Representatives: AutoGPT, Voyager, SWE-agent.

**Core capability**: Out-of-distribution generalization.
**Core bottleneck**: No physical grounding; relies on prompt engineering.

## AGI Level 4: Reflexive
Learning to learn, metacognition.
**Benchmark**: Non-existent.
Representatives: Researcher-agent, Scientist-agent.

**Core capability**: Self-improvement.
**Core bottleneck**: Poor resource awareness (infinite loops).

## AGI Level 5: Organizational
Multi-agent collaboration, emergent organization.
**Core bottleneck**: Goal alignment, resource allocation.

---

## Core Technologies by Level

| Level | Core Mechanism | Missing |
|-------|---------------|---------|
| L1 | Memory, emergence | No planning |
| L2 | Attention, Transformer | No goal maintenance |
| L3 | World Model, Planning | No physical foundation |
| L4 | Meta-learning, metacognition | No resource awareness |
| L5 | Multi-agent, alignment | No theoretical framework |

---

## Key Findings

1. **L2→L3 is the biggest gap**: From "remember" to "synthesize" — requires compositional generalization.
2. **L3 world model evaluation is a blank**: No benchmark measures world-model quality itself.
3. **L4 multi-agent resource bottleneck**: ChatDev/SWE-agent loops infinitely; no thermodynamic "cost signal."
4. **Embodied AI vs. digital AI**: Physical interaction produces more stable world models, but higher energy cost.

---

## Mapping to Our Thermodynamic Framework

- L2 = attractor **basin** in free-energy landscape
- L3 = **saddle-point transitions** between attractors
- L4 = **curvature-aware** metacognition trigger
- L5 = **synchronization and competition** in multi-attractor systems

Landauer dissipation = **computational cost signal** at every level.
