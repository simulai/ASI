# Free Energy Minimization: A Constraint, Not a Blueprint

> Source: In-depth discussion on FEP (Free Energy Principle) and the freedom of modular decomposition
> Compiled by: FARS Automatic Research System
> Date: 2026-03-23

---

## Core Tension: FEP Is So General It Loses Prescriptive Power

The Free Energy Principle (FEP), proposed by Karl Friston, is powerful precisely because it's so universal:

> **FEP is not a "theory of the brain" — it is the necessary behavior of any non-equilibrium system that maintains a boundary.**

All it requires is a **Markov blanket** (internal/external boundary). Internal states then minimize variational free energy (an upper bound on surprise) through perception and action.

**What does this mean?**

FEP can be "applied" to almost any self-organizing system: cells, organs, brains, societies, economic systems. Friston himself emphasizes this repeatedly.

So when we say "all four components obey free-energy minimization," we're actually saying:
- They're not randomly assembled engineering hacks
- They're each implementing the same thermodynamic/information-theoretic objective at **different levels / different timescales**
- **But FEP itself is so "loose" that there are theoretically infinite ways to modularize it**

Any overall closed loop that effectively minimizes free energy is a valid solution.

---

## The Four Components: One Elegant, Bio-Inspired Decomposition — Not the Only Answer

Our four components (Landauer Gate, Hopfield Attractor, Complementary Gate, Emergent Routing) are compelling because:

- They cover the critical loop: **perception → memory → decision → execution**
- Each maps directly to specific physical mechanisms in energy/entropy/information flow
- Natural progression: perceive cost → retrieve low-energy memory → hard-select path → route to best-matching "organ"

**But if you ask "what else could it be?" — there are many other valid decompositions.**

---

## Alternative Modular Decompositions

| Decomposition Source | # of Components | Core Components | Why It Also Obeys FEP | Difference from Our Version |
|---------------------|-----------------|----------------|----------------------|---------------------------|
| **Ours (bio + physics inspired)** | 4 | Landauer Gate, Hopfield Attractor, Complementary Gate, Emergent Routing | Cost sensing → stable anchoring → hard selection → dynamic allocation | Most "hardware-level," most explicitly energetic |
| **Classic Active Inference layers** (Friston mainstream) | Multiple, often simplified to 4 functional loops | Perception (prediction error minimization), Action (policy selection), Learning (structure update), Attention (precision weighting) | Each layer/process does gradient descent on the variational bound | More functional/algorithmic, less physicshardware flavor |
| **Predictive Coding hierarchy** | Usually 4–6 layers | Low-level sensory, mid-level feature, high-level concept, top-level goal/prior | Each layer minimizes prediction error (≈ local form of free energy) | More "neural network-style" hierarchy, not independent organs |
| **Brain network neuroscience** | Usually 4–7 large modules | Vision, Auditory/Language, Executive Control, Default Mode Network (DMN), Salience Network, Limbic/Emotional | High integration within modules, weak connections between, globally minimizes surprise | More macro, more task-oriented |
| **Autonomous / multi-agent Active Inference** | 4 agent roles | World modeler, Planner, Actor, Critic (or Actor-Critic + Meta-learner) | Each agent minimizes its own free energy, collaborating via message passing | More like multi-LLM system division of labor |
| **Minimalist physics-only** (thermodynamic necessity) | 3–4 | Boundary maintainer (Markov blanket), Energy estimator, State attractor, Transition selector | Almost pure physics: maintain boundary → estimate energy → low-energy state → select path | Most abstract — possibly our four's "minimal implementation" |

---

## Key Conclusion: Freedom Is a Feature, Not a Bug

FEP's "freedom" is precisely its strength — like the Second Law of Thermodynamics, it is a **constraint**, not a **blueprint**.

- The Second Law tells you "systems must evolve toward higher entropy," but doesn't specify how to build an engine.
- FEP tells you "systems must minimize free energy," but doesn't prescribe how many blocks to use or how to stack them.

Our four components are one **especially engineerable** answer (because they map directly onto upgrade paths for Transformer/MoE/LSTM/Hopfield), but not the only answer.

**Treat it as a design space, not a unique solution.**

---

## Directions for Further Exploration

### 1. Fewer Components: Can We Compress to Three?

For example, merge Complementary Gate and Emergent Routing into a single "deterministic routing + selection" module.

**Rationale**: Complementary Gate's hard selection is essentially a form of routing — just a different implementation. Merging them is more parsimonious.

### 2. More Components: Add a Dedicated "Uncertainty Estimation" Module

Corresponds to neuroscience **neuromodulation / precision weighting** — the brain doesn't treat all information equally; it dynamically adjusts module weights based on current uncertainty.

**Analogy**: Humans do less and act faster on familiar tasks (high confidence), hesitate on unfamiliar ones (low confidence, needs more resources).

### 3. Different Timescales: One Module Per Timescale

| Timescale | Physical Process | Module |
|-----------|-----------------|--------|
| Milliseconds | Perceptual update | Fast predictive coding layer |
| Seconds–minutes | Planning and action selection | Mid-speed Active Inference |
| Hours–days | Learning / structural update | Slow weight adjustment |

This aligns naturally with multi-agent systems' "different reaction speeds."

### 4. Multi-Agent Flavor: Four Components as Four Small Agents

Each component is an independent agent, communicating via an Active Inference protocol.

**Benefit**: Naturally parallel — each agent can be trained/upgraded/replaced independently.
**Challenge**: Communication overhead, timing synchronization, consistency guarantees.

---

## Thermodynamics vs Engineering: Two Parallel Paths

| | Thermodynamic Route (ours) | Engineering Route |
|--|--------------------------|-------------------|
| Goal | Prove components are physically necessary | Prove components work on benchmarks |
| Validation | Lean4 formal proofs + Landauer's equation | NLP/RL benchmark testing |
| Risk | Elegant but ungrounded in practice | Effective but lacks physical foundation |
| **Optimal strategy** | **Prove effectiveness on benchmarks first, then backfill the physics** | — |

> **Our current bottleneck**: The physics derivation of all four components is done (Paper 2), but we haven't yet proven their effectiveness on benchmarks. This is the next mandatory step.
