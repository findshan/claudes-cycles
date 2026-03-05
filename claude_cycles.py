#!/usr/bin/env python3
"""
Claude's Cycles — Hamiltonian Decomposition of Cayley Digraphs

Implementation of the algorithm discovered by Claude Opus 4.6 and described
in Don Knuth's note "Claude's Cycles" (28 February 2026).

Given odd m > 1, decomposes the digraph on m³ vertices ijk (0 ≤ i,j,k < m)
with arcs to i⁺jk, ij⁺k, ijk⁺ (where x⁺ = (x+1) mod m) into three
directed Hamiltonian cycles.
"""

import json
import os
from pathlib import Path


def generate_cycle(m: int, c: int) -> list[tuple[int, int, int]]:
    """
    Generate Hamiltonian cycle `c` (0, 1, or 2) for the digraph of order m.

    This is a direct translation of Knuth's C program from the paper.
    The permutation string d encodes which coordinate to bump:
      '0' -> bump i, '1' -> bump j, '2' -> bump k.

    Returns a list of (i, j, k) tuples forming the cycle (length m³),
    where the last vertex connects back to the first.
    """
    assert m > 2 and m % 2 == 1, "m must be odd and > 2"
    assert 0 <= c <= 2, "c must be 0, 1, or 2"

    cycle = []
    i, j, k = 0, 0, 0
    n = m * m * m

    for t in range(n):
        cycle.append((i, j, k))

        s = (i + j + k) % m

        # Determine permutation d based on s, i, j
        if s == 0:
            d = "012" if j == m - 1 else "210"
        elif s == m - 1:
            d = "210" if i == 0 else "120"
        else:
            d = "201" if i == m - 1 else "102"

        # Bump the coordinate specified by d[c]
        direction = d[c]
        if direction == '0':
            i = (i + 1) % m
        elif direction == '1':
            j = (j + 1) % m
        else:
            k = (k + 1) % m

    return cycle


def verify_hamiltonian(m: int, cycle: list[tuple[int, int, int]]) -> bool:
    """Verify that a cycle is a valid Hamiltonian cycle of length m³."""
    n = m * m * m

    # Check length
    if len(cycle) != n:
        print(f"  FAIL: cycle length = {len(cycle)}, expected {n}")
        return False

    # Check all vertices are distinct
    vertex_set = set(cycle)
    if len(vertex_set) != n:
        print(f"  FAIL: only {len(vertex_set)} distinct vertices, expected {n}")
        return False

    # Check all vertices are valid
    for (i, j, k) in cycle:
        if not (0 <= i < m and 0 <= j < m and 0 <= k < m):
            print(f"  FAIL: invalid vertex ({i},{j},{k})")
            return False

    # Check adjacency: each vertex connects to the next via a valid arc
    for t in range(n):
        vi, vj, vk = cycle[t]
        ni, nj, nk = cycle[(t + 1) % n]

        # The arc must be exactly one coordinate bumped by 1 mod m
        di = (ni - vi) % m
        dj = (nj - vj) % m
        dk = (nk - vk) % m

        valid_arcs = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        if (di, dj, dk) not in valid_arcs:
            print(f"  FAIL: invalid arc from ({vi},{vj},{vk}) to ({ni},{nj},{nk})")
            return False

    return True


def verify_decomposition(m: int, cycles: list[list[tuple[int, int, int]]]) -> bool:
    """
    Verify that 3 cycles form a valid arc decomposition:
    - Each cycle is Hamiltonian
    - At each vertex, the 3 arcs go to different coordinates across the 3 cycles
    """
    print(f"\n{'='*60}")
    print(f"Verifying decomposition for m = {m} ({m**3} vertices)")
    print(f"{'='*60}")

    all_ok = True

    # Verify each cycle is Hamiltonian
    for c in range(3):
        ok = verify_hamiltonian(m, cycles[c])
        status = "✓" if ok else "✗"
        print(f"  Cycle {c}: {status} Hamiltonian (length {len(cycles[c])})")
        all_ok = all_ok and ok

    # Verify arc partition: at each vertex, the 3 cycles use different directions
    arc_map = {}  # (i,j,k) -> set of directions used

    for c in range(3):
        n = m * m * m
        for t in range(n):
            vi, vj, vk = cycles[c][t]
            ni, nj, nk = cycles[c][(t + 1) % n]

            di = (ni - vi) % m
            dj = (nj - vj) % m
            dk = (nk - vk) % m

            if (di, dj, dk) == (1, 0, 0):
                direction = 0
            elif (di, dj, dk) == (0, 1, 0):
                direction = 1
            else:
                direction = 2

            key = (vi, vj, vk)
            if key not in arc_map:
                arc_map[key] = set()

            if direction in arc_map[key]:
                print(f"  FAIL: direction {direction} used twice at vertex {key}")
                all_ok = False
            arc_map[key].add(direction)

    # Each vertex should have all 3 directions
    for v, dirs in arc_map.items():
        if dirs != {0, 1, 2}:
            print(f"  FAIL: vertex {v} has directions {dirs}, expected {{0,1,2}}")
            all_ok = False

    if all_ok:
        print(f"  Arc partition: ✓ All 3m³ = {3*m**3} arcs correctly partitioned")

    print(f"  Overall: {'✓ PASS' if all_ok else '✗ FAIL'}")
    return all_ok


def verify_m3_example(cycles: list[list[tuple[int, int, int]]]) -> bool:
    """Cross-check cycle 0 for m=3 against Knuth's example in the paper."""
    # Knuth's cycle 0 for m=3 (starting from 022):
    knuth_c0 = [
        (0,2,2), (0,0,2), (0,0,0), (0,0,1), (0,1,1), (0,1,2),
        (0,1,0), (0,2,0), (0,2,1),
        (1,2,1), (1,0,1), (1,1,1), (1,1,2), (1,2,2), (1,0,2),
        (1,0,0), (1,1,0), (1,2,0),
        (2,2,0), (2,2,1), (2,0,1), (2,0,2), (2,0,0), (2,1,0),
        (2,1,1), (2,1,2), (2,2,2),
    ]

    # Our cycle starts at (0,0,0). Find offset to match Knuth's starting point.
    cycle = cycles[0]
    try:
        offset = cycle.index((0, 2, 2))
    except ValueError:
        print("  FAIL: vertex (0,2,2) not found in cycle 0")
        return False

    rotated = cycle[offset:] + cycle[:offset]

    if rotated == knuth_c0:
        print("  Knuth m=3 example: ✓ Cycle 0 matches paper exactly")
        return True
    else:
        print("  FAIL: Cycle 0 does not match Knuth's m=3 example")
        for idx, (a, b) in enumerate(zip(rotated, knuth_c0)):
            if a != b:
                print(f"    First mismatch at position {idx}: got {a}, expected {b}")
                break
        return False


def save_results(m: int, cycles: list[list[tuple[int, int, int]]], verified: bool):
    """Save cycles to a JSON file."""
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    data = {
        "m": m,
        "num_vertices": m ** 3,
        "num_arcs_per_cycle": m ** 3,
        "total_arcs": 3 * m ** 3,
        "verified": verified,
        "cycles": [
            [list(v) for v in cycle]
            for cycle in cycles
        ],
    }

    out_path = results_dir / f"cycles_m{m}.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved to {out_path}")


def main():
    print("Claude's Cycles — Hamiltonian Decomposition")
    print("=" * 60)
    print("Algorithm from Knuth's paper (28 Feb 2026)")
    print("Discovered by Claude Opus 4.6\n")

    test_values = [3, 5, 7, 9]
    all_passed = True

    for m in test_values:
        # Generate 3 cycles
        cycles = [generate_cycle(m, c) for c in range(3)]

        # Verify
        ok = verify_decomposition(m, cycles)

        # Extra check for m=3
        if m == 3:
            verify_m3_example(cycles)

        # Save to JSON
        save_results(m, cycles, ok)
        all_passed = all_passed and ok

    print(f"\n{'='*60}")
    if all_passed:
        print("All decompositions verified successfully! ✓")
    else:
        print("Some verifications FAILED! ✗")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
