# MIT NCA Pre-pre-training: Thermodynamic Interpretation

> Source: MIT Improbable AI Lab, Pulkit Agrawal team
> Paper: arXiv:2603.10055 (March 2026)
> Date: 2026-03-23

## Experimental Results

- NCA data (164M tokens) outperforms 1.6B English tokens
- Language model perplexity reduced by up to 6%
- Convergence speed improved by up to 1.6×
- Attention layers transfer best (reinitialization = largest performance loss)
- Complexity matching: OpenWebText/OpenWebMath prefer high-complexity NCA; code prefers medium complexity

## MIT's Interpretation

> "What language models may actually need to learn is not language itself, but the computational structure behind language."

## Our Thermodynamic Interpretation

**NCA trajectories = thermodynamically pure attractor dynamics.**

- CA pixels are not "semantic tokens" — they are "attractor states."
- Each NCA sequence from a random rule = each attractor basin is different.
- Predicting the next pixel = infer current attractor dynamics = gradient descent on free-energy landscape.
- Natural language's "semantic shortcuts" and "co-occurrence priors" = local minima in free-energy landscape to rely on = no pure inference required.

**Landauer perspective**: Each CA update step = erase 1 bit of information = must dissipate kT·ln2.
Natural language tokens have statistical redundancy = information not fully erased = low training efficiency.
NCA data forces full erasure at every token = high training efficiency.

## Key Implications

1. **Attention layers transfer best** = Attention ≈ free-energy minimization = domain-agnostic = universal.
2. **MLP layers transfer poorly** = MLP = stores domain-specific patterns = depends on source-target domain match.
3. **Complexity matching determines transfer** = The "shape" (curvature) of free-energy landscape determines which attractors are most valuable for a target domain.

## Significance for Our Work

Paper 2 (Thermodynamic Foundations) gains **independent external validation**:
- MIT discovered the same phenomenon from "computational structure transfer" angle.
- We explain the same phenomenon from "thermodynamic / free-energy" angle.
- Two languages, mutually reinforcing.
