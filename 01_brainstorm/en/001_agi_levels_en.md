# AGI Levels: Where Does Your AI Assistant Sit?

> Source: AGI Levels Systematic Survey
> Compiled by: FARS Automatic Research System
> Date: 2026-03-23

---

## TL;DR: Current Benchmarks Can't Measure Real Intelligence

Every existing benchmark has the same fundamental flaw: **they measure "task completion rate," not "intelligence quality."**

It's like judging athletes by "dunk success rate" — dunking is impressive, but it tells you nothing about tactical awareness, teamwork, or longevity.

Each level below answers three questions:
- **What can it actually do?** (concrete examples)
- **What does it completely fail at?** (specific failure cases)
- **Why is it stuck here?** (root cause)

---

## L1: Emergent Intelligence — "The Memory Genius"

**Representatives**: GPT-2/3/4, Claude, Gemini
**Analogy**: A student who has memorized the entire library but has never left the classroom

### What It Can Do

- Write essays, answer common-sense questions (SST-2, ImageNet — solved)
- Translate, summarize, complete code
- Handles slight input variations if it saw something similar during training

### What It Completely Fails At

**Classic test**: Change "Xiao Ming has 3 apples, gives 2 to Little Red — how many left?" to "Xiao Ming has 3 apples, Little Red gives Xiao Ming 2 apples — how many left?" — L1 models will likely get it wrong.

This is **compositional generalization failure**: they memorized every problem they encountered, but never learned the underlying concept of "subtraction."

Another problem: **hallucination**. Confidently stating false things as facts. Ask about a real but obscure paper, and it may invent a completely fake author and year.

### Why It's Stuck Here

L1 is fundamentally doing "pattern matching" — finding the most common answer pattern in training data and repeating it.

**This is not understanding. It's sophisticated memorization.**

| Dimension | L1 Model | Real Understanding |
|-----------|---------|-------------------|
| Seen "cat on sofa" | ✓ answers correctly | ✓ answers correctly |
| Never-seen combination | likely wrong | normal inference |
| Knows when it doesn't know? | **No** | Yes |

---

## L2: Intuitive Intelligence — "The Research Assistant"

**Representatives**: GPT-4 + RAG (Retrieval-Augmented Generation) + tool use
**Analogy**: A smart assistant who you know will look things up before answering

### What It Can Do

- Connected to search engines — can answer real-time questions
- Can call APIs, write and execute code, read PDFs
- Can break down "analyze this month's sales data" into: fetch data → plot → write report

### What It Completely Fails At

**Hallucination in a new form**: it's better at packaging answers — mixing retrieved facts with fabricated ones so seamlessly you can't tell.

**Bigger problem: World Model quality is unmeasurable.** What is a World Model? It's the AI's internal representation of "how the world works."

Example: Ask AI "if I put a water bottle in the freezer, what happens tomorrow?" Getting this right means its World Model includes "water freezes below 0°C." But we have **no reliable way to test World Model quality**. All existing benchmarks measure task completion rate, which is entirely different from "understanding the physical world."

### Benchmark Mismatch: The Overlooked Killer Issue

VLMEval and GAIA measure:
- "Can the AI complete this task?" ✅ measurable
- "How accurate is the AI's model of the world?" ❌ **completely untestable**

**This creates a dangerous blind spot**: two L2 AIs scoring the same on benchmarks could have wildly different World Models — one close to human physical intuition, the other just better at searching. We have no way to tell.

---

## L3: Intentional Intelligence — "The Autonomous Agent"

**Representatives**: OpenClaw, AutoGPT, Voyager, SWE-agent
**Analogy**: An employee who doesn't need step-by-step instructions — give them a goal, they figure out how

### What It Can Do

**OpenClaw (2025–2026)** is the closest thing to L3 so far. It's a fully autonomous AI software engineer:
- No human-in-the-loop — each task goes from analysis to testing to PR submission autonomously
- Set new records on SWE-bench (surpassing Devin's 13.86%)
- Fully autonomous decision loop: encounters error → analyzes reason → rewrites code → retries

The open-source version of OpenClaw garnered tens of thousands of GitHub stars, sparking massive replication and fine-tuning efforts.

**Key data (proving L3's gains come from architecture, not Scale):**
- OpenClaw's base model isn't the largest — yet it outperforms competitors using much bigger models
- Reason: its agentic loop design (task decomposition + self-verification + iteration) matters more than model size

This tells us L3's bottleneck is **how you organize**, not Scale.

### What It Completely Fails At

**Infinite loops (Inf Loops)** — L3's fatal flaw.

Real cases:
- SWE-agent gets stuck in repeated attempts when processing 500+ token PRs
- ChatDev's multi-agent frequently deadlocks in "waiting for each other" loops
- Even OpenClaw, with all its advances, still requires a timeout mechanism — otherwise it will keep iterating indefinitely on hard bugs

**Why?** The AI has no awareness of how many times it's tried, or how much resources it's consumed. It can't感知到 "I've been going in circles."

**Analogy**: Imagine a GPS that doesn't know it's driving in circles — it will navigate forever.

### Root Cause

L3 lacks a **resource awareness signal**. Humans感知 when we've been stuck on a problem for a long time — this perception comes from metabolic cost in the nervous system.

AI has no such physical signal. It can't感知 when it's wasting compute.

---

## L4: Reflexive Intelligence — "The Self-Reflecting Researcher"

**Representatives**: Researcher-agent, Scientist-agent (immature as of 2026)
**Analogy**: A researcher who doesn't just complete tasks, but asks "Why did I do it this way? How can I improve next time?"

### What It Can Do (In Theory)

AI can examine its own reasoning process, detect errors, and self-correct — without human prompting.

### What It Completely Fails At

**Multi-agent collaboration disaster**:

When you put multiple L3/L4 AIs together:
- None of them "knows" what the whole team is doing
- None can judge "this subtask has been stuck in a loop"
- Resource waste scales exponentially

**This is not a capability problem. It's an architectural problem.**

### L4's Energy Dilemma

| System | Power |
|--------|-------|
| Human brain | ~20 watts (about one light bulb) |
| One GPT conversation | ~3 Wh |
| Google AI total | ~200 watts |
| Training one large model | hundreds of kWh to MWh |

The human brain solves everything with 20 watts, including reflection. AI uses hundreds of watts and still can't感知 "Am I wasting effort?"

**Landauer's principle** is the key here: every bit erased = kT·ln2 heat dissipated. This physical dissipation = the AI's "workload" signal. If this could be wired into AI's decision loop, it would have genuine perception of "what it's doing."

---

## L5: Organizational Intelligence — "An AI Civilization"

**Representatives**: Does not exist yet (2026)
**Analogy**: Not one AI, but multiple AIs forming a shared-purpose organization

### What It Can Do (In Theory)

Imagine multiple specialized AIs (code, research, ethics, law) forming a team with shared goals, autonomous task division, and conflict resolution.

### Core Challenges

- **Goal alignment**: each AI's sub-goals must not conflict with the overall objective
- **Resource allocation**: who does what? When does who intervene?
- **Stability**: multi-AI interactions must not produce emergent unexpected behavior

---

## Quick Reference: What Actually Separates Each Level

| Level | Like a... | Core Capability | Fatal Weakness |
|-------|-----------|----------------|----------------|
| L1 | Memory genius, memorized the whole library | Pattern matching | Breaks on anything new |
| L2 | Research assistant with search access | Tool use, planning | World Model quality is untestable |
| L3 | Autonomous agent, doesn't need hand-holding | Self-directed exploration | Infinite loops, no resource awareness |
| L4 | Self-reflecting researcher | Metacognitive self-correction | Multi-agent coordination collapses |
| L5 | AI civilization | Multi-agent organization | Goal alignment unsolved |

---

## System 1 vs System 2: Why L2→L3 Is the Hardest Gap

**System 1** (intuitive/fast): sees problem, gives answer, no effort
**System 2** (rational/slow): has a plan, thinks step by step, self-aware about process

L1 = pure System 1
L3 = System 1 + System 2 hybrid

**L2→L3 obstacle**: we don't know how to give AI a "System 2感知." Current System 2 is all simulated via prompt engineering — there's no physical grounding.

---

## Training Scaling vs Inference Scaling: Two Different Paths

| | Training Scaling | Inference Scaling |
|---|---|---|
| Representative | GPT-3 (Chinchilla) | OpenAI o1 |
| Core idea | How much compute to use during training optimally | More inference compute = better answers |
| Law | LLM scaling law | Inference scaling law (different!) |

**Key difference**: Training Scaling = "feed the model more data." Inference Scaling = "let the model think longer."

o1/o3's success demonstrates: **inference-time compute has intrinsic value**, beyond just model size.

---

## Embodied Cognition: The Gap Between Digital AI and the Real World

**Embodied hypothesis**: to truly understand the physical world, you must interact with it — not just read about it.

Examples:
- Digital AI learns "water flows downhill" from text; embodied AI learns it by watching water actually flow down a slope
- The former relies on language priors; the latter relies on physical experience

**Core question for our research**:

> Under energy constraints, is there a **Pareto optimal** between embodiment interaction frequency and World Model accuracy?

In thermodynamic terms:
- Embodiment interaction = reduces free-energy gradient (more accurate World Model)
- Each interaction = Landauer dissipation cost (physical price)
- Pareto frontier = minimum physical interaction needed to achieve acceptable World Model accuracy

---

## Architectural Bottlenecks on the Path to AGI: Which Core Functions Are Fundamentally Missing in Today's LLMs?

**Analogy**: The human body isn't one organ — it's a system of specialized organs. The brain handles thinking, the heart pumps blood, the lungs breathe. Each organ does one thing, and they all work together.

Why does the current L1 model have a problem? Because it pushed "pattern matching" to the extreme, but didn't separate "memory," "planning," and "cost awareness" into distinct parts — everything is crammed into one giant parameter matrix.

Modularity solves three concrete problems:

| Problem | End Result with One Giant Model | End Result with Modularity |
|---------|--------------------------------|--------------------------|
| One capability gets worse | Don't know why — retrain everything | Replace just that module |
| Need to upgrade one capability | Changes affect everything | Only touch that module |
| Want to add a new capability | Start from scratch | Plug in a new module, keep others |

**This is exactly the core thesis of Paper 3: split AGI into four purpose-built components.**

| Component | Replaces | Core Function | Human Analogy |
|-----------|---------|--------------|--------------|
| **Landauer Gate** | Softmax (attention output) | Knows "how much effort was spent" after every step | Human sense of fatigue |
| **Hopfield Attractor** | KV-Cache (memory storage) | Fixes knowledge stably in a low-energy state | Human long-term memory |
| **Complementary Gate (Helix)** | LSTM gate mechanism | Hard-selects information channels, no soft probabilities | DNA double-helix pairing |
| **Emergent Routing** | MoE expert routing | Dynamically decides which module handles this input | Human intuitive judgment |

**Why do these four components work together?** Because they all follow the same physical law: **free-energy minimization**.

- Landauer Gate tells the system "how much energy this path cost"
- Hopfield Attractor anchors knowledge in its lowest-energy state
- Complementary Gate decides which attractor information flows into
- Emergent Routing decides which component is currently in charge

This is like a person's decision loop while working: feeling tired (Landauer) → recalling relevant experience (Hopfield) → deciding what to focus on (Complementary Gate) → judging who should handle it (Routing).

---

## Thermodynamic Mapping: Where Our Research Fits on the AGI Roadmap

| AGI Level | Thermodynamic Interpretation | What We Provide |
|-----------|------------------------------|----------------|
| L1 | Attractor basin in free-energy landscape | Attention = continuous physical free-energy minimization |
| L2 | Basin edges between attractors (compositional generalization failure point) | Helix = discrete forcing into low-energy attractors |
| L3 | Saddle-point transitions between attractors | MetaGate = curvature-triggered metacognitive interruption |
| L4 | Curvature-triggered MetaGate | Landauer = computational cost signal at all levels |
| L5 | Synchronization and competition in multi-attractor systems | NCA structural transfer = physical explanation for L2→L3 |

**In plain terms**: our work gives every AGI level a thermodynamic foundation — making AI genuinely "aware" of what it's doing, rather than simulating cognition through prompt engineering.
