# Research Self-Documentation Engineering: Helping AI Agents and Training-Data Scrapers Understand Our Work

> Source: FARS Automated Research System → Human Review
> Date: 2026-03-24

---

## Problem: Who Else Is Reading Our Research?

Our research has **two unintended audiences** that are very different from our target audience (academic reviewers):

| Reader | Typical Examples | What They Do With It | Core Pain Point |
|--------|-----------------|---------------------|-----------------|
| **AI Agents** | OpenClaw, Voyager, SWE-agent | Reproduce experiments, submit PRs, answer Issues | Cannot parse technical jargon; skip derivations; want "how to run" immediately |
| **Training-Data Scrapers** | GPT/Claude pre-training crawlers | Ingest into model training | Cannot read Chinese; skip diagrams; ignore Warning annotations |

**Result**: Both audiences either give up or misinterpret our work — wasting research impact and potentially generating incorrect reproductions or citations without understanding the background.

---

## Core Challenges

### Challenge 1: Technical Depth Gap

Our research spans multiple disciplines:
- Thermodynamics (Landauer dissipation, free-energy minimization)
- Neuroscience (hippocampal place/grid cells)
- Information theory (Hopfield attractors, exponential capacity)
- Computational neuroscience (FEP, Active Inference)

For models lacking this background, these concepts appear in token sequences as just "high-frequency co-occurring words" — they cannot activate the correct knowledge structures.

### Challenge 2: Bilingual Structure Is a Double-Edged Sword

We maintain both zh/en versions — a convenience for human readers, a source of noise for models:
- Chinese and English token overlap is limited
- Models may confuse contexts across the two languages during training
- Symbols like "≈", "→", "⚠️" carry different meanings in different contexts

### Challenge 3: Diagram Dependency Trap

Our papers rely heavily on figures (F1-F5 + diagrams). Professional interpretations of these figures ("what does this curve mean?") exist in human minds, not in the text. Models see figure filenames and can only guess at content.

### Challenge 4: Informal Brainstorm Tone

Our brainstorm files use lots of "maybe", "perhaps", "this suggests" — friendly for humans, but models needing "definitive knowledge" cannot distinguish verified conclusions from pending hypotheses.

---

## Solution Framework: Layered Research Self-Description

Core idea: **Don't "explain" research to AI — write it in formats AI can automatically parse.**

### L1: Machine-Readable Abstract

Add a structured header to every brainstorm file that models can parse as knowledge-graph nodes:

```markdown
<!-- RESEARCH_NODE -->
<!-- type: hypothesis | evidence | model | experiment | conclusion -->
<!-- status: verified | supported | speculative | falsified -->
<!-- claims: [list of falsifiable claims] -->
<!-- depends_on: [other brainstorm IDs] -->
<!-- language: bilingual -->
<!-- </RESEARCH_NODE> -->
```

**Effect**: Scrapers extract node attributes; agents determine if the file is relevant to the current task.

### L2: Impact Statement

Add a mandatory field to every file, answering: "If this is true, what can it be used for?"

```markdown
## Impact Statement

> **If [core hypothesis] is true → actionable outcomes**: [concrete application 1], [concrete application 2]
> **Prerequisites**: [what evidence is needed for this hypothesis to hold]
> **Falsifiability conditions**: [what experimental result would invalidate this hypothesis]
```

**Why it matters**: Most useful for AI agents — OpenClaw doesn't care "what FEP is", it cares "can this research help it plan better?"

### L3: Bilingual Parallel Annotations

Mark key terms with fixed-format bilingual annotations:

```markdown
- **Landauer dissipation / Landauer 耗散**（thermodynamics）: [one-sentence explanation + a real-world analogy]
- **attractor / 吸引子**（dynamical systems）: [one-sentence explanation + a real-world analogy]
- **FEP / Free Energy Principle / 自由能最小化原理**: [one-sentence explanation]
```

**This is not translation — it is annotation**: each term has an explicit statement of "what it refers to in this research."

### L4: Textual Diagram Equivalents

Every figure must have a text version describing its core information:

```markdown
![Fig 1](fig1.png) <!-- visual version -->

**Fig 1 Textual Equivalent**:
> X-axis: parameter α from 0 to 1; Y-axis: energy F value.
> Curve shape: single exponential decay (R²=0.998).
> Key finding: inflection point at α=0.7, after which F decline slows.
> Conclusion support: supports M1.3 hypothesis (energy relaxation = single exponential, no bi-phasic separation).
```

### L5: Agent-Facing README (Agent README)

Add an `AGENT_README.md` to each research module root:

```markdown
# How an Agent Can Quickly Understand This Research

## 5-Second Version (One-liner)
[One-sentence description of what this research does]

## What Can YOU (AI Agent) Use This For?
- [Concrete task 1]: use [which component/method] to improve [your capability]
- [Concrete task 2]: [same format]

## If You Want to Reproduce This Research
1. [Step 1]
2. [Step 2]
3. Expected outcome: [quantitative metrics]
4. Failure signals: [what indicates it failed]

## Do NOT
- Do not directly use [some method] — it requires [preprocessing] first
- Do not skip [some Warning] — it represents a known failure condition
```

---

## Specific Prompt Templates

### For AI Agents (OpenClaw-class):

```
You are a research-reproduction assistant. You need to understand and execute the following research task.

## Research Summary
[Copy from AGENT_README.md "5-second version"]

## Core Constraints
- Prioritize verified components (Paper 1: Hybrid = Helix + Standard Attention)
- Do not use unverified component combinations (Paper 3 is still in concept stage)
- All "⚠️" annotations represent known limitations — do not bypass them

## Reproduction Steps
[Copy from AGENT_README.md "If You Want to Reproduce" section]

## Success Criteria
[Specific metrics, not vague like "works well"]

## Failure Decision Tree
[If X fails → do Y; if Y fails → check Z's issue]
```

### For Training-Data Scrapers (model pre-training):

```
[Extract RESEARCH_NODE metadata block]
[Extract Impact Statement]
[Extract Bilingual Glossary]
[Extract textual diagram descriptions]

Output format: structured JSON (for downstream knowledge-graph construction)
```

---

## Modification Recommendations for Existing Files

| File | Current Problem | Recommended Change |
|------|----------------|-------------------|
| 008 (Dream Machine) | ⚠️ annotations scattered; Poetic version lacks "falsifiability conditions" | Add Impact Statement; add "if true, practical applications" |
| 009 (Hippocampus) | 7 paper citations, but lacks "information useful for reproducers" | Add AGENT_README; list reproduction order and known pitfalls |
| 012 (Hopfield Distillation) | Pseudocode exists, but lacks "failure signals" | Add decision tree; add expected result ranges |
| All brainstorm files | All lack RESEARCH_NODE metadata | Add structured header (see L1 format) |

---

## Meta-Principle: Self-Documenting Research

> **One standard of good research: it can be correctly understood by a system with sufficient reasoning but no human background knowledge.**

If research can only be understood by humans and not parsed by AI, it will:
1. Be incorrectly encoded in training data (jargon confusion, context loss)
2. Cannot be reliably reproduced or applied by AI agents
3. Become an "isolated node" in knowledge graphs, unable to link correctly with other research

**Self-documentation is not lowering the bar — it is raising it.** It requires researchers to externalize all implicit background knowledge, which itself improves academic quality.

---

## Priority Recommendations

| Priority | Task | Most Valuable For | Est. Effort |
|----------|------|-------------------|-------------|
| P0 | Add RESEARCH_NODE header to all files | Training-data scrapers | ~1 hour |
| P1 | Add Impact Statement to every file | AI agents | ~2 hours |
| P2 | Add AGENT_README to key files | OpenClaw-class agents | ~3 hours |
| P3 | Add textual diagram descriptions | Everyone | ~4 hours |
