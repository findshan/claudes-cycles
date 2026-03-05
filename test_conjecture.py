import time
from even_solution import _precompute_bases, _serp_perm_c1, count_cycles, compose_perms, _serp_perm, build_all_fibers, check_all_hc

def test_heuristic(m):
    h = m // 2
    if h % 3 == 0:
        step, offset = 6, 0
    elif h % 3 == 2:
        step, offset = 6, 2
    else:
        step, offset = 2, 0

    for t_b in (0, 2):
        base_c1, base_c2 = _precompute_bases(m, t_b)
        for t_c in range(offset, m, step):
            # Fast c1 and c2 checks using precomputed bases
            Cc1 = _serp_perm_c1(t_c, m)
            if count_cycles(compose_perms(Cc1, base_c1)) != 1:
                continue
            Cc2 = _serp_perm(t_c, m)
            if count_cycles(compose_perms(Cc2, base_c2)) != 1:
                continue
            # c0 doesn't depend on t_c; verify the full solution once
            fibers = build_all_fibers(m, m - 1, t_b, t_c)
            if check_all_hc(fibers, m):
                return (m - 1, t_b, t_c)
    return None

if __name__ == "__main__":
    import multiprocessing
    print("Testing conjecture heuristic from m=52 to 200...")
    
    t0 = time.time()
    # Test sequentially since it's quite fast on PyPy, but we only have CPython
    # We'll just test a few larger values to see if they break
    for m in range(52, 102, 2):
        tm0 = time.time()
        res = test_heuristic(m)
        if res is None:
            print(f"!!! COUNTEREXAMPLE OR HEURISTIC FAILURE AT m = {m} !!!")
        else:
            print(f"m={m:3d} : OK. t_a={res[0]}, t_b={res[1]}, t_c={res[2]} ({time.time()-tm0:.3f}s)")
    
    print(f"Total time: {time.time() - t0:.2f}s")
