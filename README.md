# Claude's Cycles

**Hamiltonian Decomposition of Cayley Digraphs on Z<sub>m</sub><sup>3</sup>**

> Inspired by Don Knuth's note *"Claude's Cycles"* (Stanford Computer Science Department, 28 February 2026; revised 04 March 2026), celebrating Claude Opus 4.6's solution to a long-standing open problem in combinatorics.

---

## The Problem

Consider the Cayley digraph $\text{Cay}(\mathbb{Z}_m^3, \{e_0, e_1, e_2\})$ with $m^3$ vertices $(i, j, k)$ for $0 \le i, j, k < m$, and three arcs from each vertex:

- $(i, j, k) \to ((i+1) \bmod m,\; j,\; k)$
- $(i, j, k) \to (i,\; (j+1) \bmod m,\; k)$
- $(i, j, k) \to (i,\; j,\; (k+1) \bmod m)$

**Goal**: Decompose all $3m^3$ arcs into exactly **three directed Hamiltonian cycles**, each of length $m^3$.

## Solution

This repository contains verified, constructive solutions for **all** $m \ge 3$ (except $m = 2$, which is provably impossible):

| Case | Method | File | Complexity |
|------|--------|------|------------|
| **Odd** $m \ge 3$ | Closed-form fiber construction (Claude Opus 4.6) | [`claude_cycles.py`](claude_cycles.py) | $O(m^3)$ |
| **Even** $m \ge 4$ | Complex fiber + threshold search (Knuth/Stapper) | [`even_solution.py`](even_solution.py) | $O(m^2)$ |

### How It Works

The key insight is a **fiber decomposition**. The quotient map $s = (i + j + k) \bmod m$ partitions $m^3$ vertices into $m$ fibers (each an $m \times m$ grid). Every arc increments $s$ by 1, so any Hamiltonian cycle must traverse fibers in strict order $0, 1, \dots, m{-}1, 0, \dots$

This reduces the 3D Hamiltonian problem to: *compose $m$ permutations on $\mathbb{Z}_m^2$ such that the result is a single $m^2$-cycle.*

- **Odd $m$**: Pure structured fibers with diagonal-threshold permutations suffice.
- **Even $m$**: A parity obstruction forces the composite to have even cycle count. A carefully designed *complex fiber* at position $m/2$ breaks this symmetry.

## Interactive 3D Visualization

Open [`visualize.html`](visualize.html) in a browser (serve via HTTP):

```bash
python3 -m http.server 8765
# Open http://localhost:8765/visualize.html
```

Features:
- 3D perspective with drag-to-rotate, scroll-to-zoom
- Toggle individual cycles (A / B / C) on/off
- Step-by-step animation with adjustable speed
- **Node labels**: each vertex shows its index within each cycle (e.g. `a0`, `b3`, `c17`)
- Directional arrows showing traversal order
- Supports $m = 3, 5, 7, 9$

## Quick Start

### Odd $m$ (generate & verify)

```bash
python3 claude_cycles.py
# Generates results/cycles_m{3,5,7,9}.json and verifies each
```

### Even $m$ (construct & verify)

```bash
python3 even_solution.py
# Constructs and verifies for m = 4, 8, 16, 24, 48
```

### Test the threshold heuristic for larger even $m$

```bash
python3 test_conjecture.py
# Tests the step-heuristic for m = 52..100
```

## Project Structure

```
claude-cycles/
├── claude_cycles.py       # Odd-m solver (Claude's construction)
├── even_solution.py       # Even-m solver (Knuth's fiber construction)
├── test_conjecture.py     # Large-scale heuristic verification
├── visualize.html         # Interactive 3D visualization
└── results/
    ├── cycles_m3.json     # Pre-computed cycles for m=3
    ├── cycles_m5.json     # Pre-computed cycles for m=5
    ├── cycles_m7.json     # Pre-computed cycles for m=7
    └── cycles_m9.json     # Pre-computed cycles for m=9
```

## Open Conjecture

For even $m$, the algorithm searches for a threshold $t_c$ within a specific arithmetic progression determined by $(m/2) \bmod 3$. This heuristic has been verified computationally for all even $m$ from 4 to 200, but a general proof that a valid $t_c$ always exists remains an **open mathematical problem**.

## References

- **Knuth, D. E.** (2026). *Claude's Cycles.* Stanford Computer Science Department.
  [https://cs.stanford.edu/~knuth/claude.cycles.pdf](https://cs.stanford.edu/~knuth/claude.cycles.pdf)

- **Knuth, D. E.** — Even-case solution script:
  [https://cs.stanford.edu/~knuth/even_solution.py](https://cs.stanford.edu/~knuth/even_solution.py)

- **Stapper, L.** — Original even-$m$ construction using OR-Tools CP-SAT, referenced in Knuth's note.

## License

MIT
