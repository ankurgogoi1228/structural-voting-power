from fractions import Fraction
from math import factorial
from itertools import combinations

# ============================================================
# General Shapley computation for a vote‑loss game
# ============================================================
def shapley_values(agents, succ, q, yes_weight_func):
    """
    agents: list of agent labels
    succ: dict mapping agent -> next agent (None if sink)
    q: quota
    yes_weight_func: function taking a coalition set and returning yes-weight
    """
    n = len(agents)
    v = {}
    # build game
    for mask in range(1 << n):
        S = {agents[i] for i in range(n) if mask & (1 << i)}
        v[mask] = 1 if yes_weight_func(S) >= q else 0

    fact = [factorial(k) for k in range(n + 1)]
    phi = {i: Fraction(0, 1) for i in agents}
    for idx, i in enumerate(agents):
        bit_i = 1 << idx
        for mask in range(1 << n):
            if mask & bit_i:
                continue
            k = mask.bit_count()
            if v[mask | bit_i] == 1 and v[mask] == 0:
                weight = Fraction(fact[k] * fact[n - k - 1], fact[n])
                phi[i] += weight
    return phi

# ============================================================
# 1. Star topology (n=6 as in Example)
# ============================================================
print("=== Star (n=6) ===")
n = 6
agents = list(range(n))  # 0 center, 1..5 leaves
succ = {0: None}
for i in range(1, n):
    succ[i] = 0
q = n // 2 + 1   # 4

def yes_weight_star(S):
    if 0 not in S:
        return 0
    return 1 + len(S & set(range(1, n)))

phi_star = shapley_values(agents, succ, q, yes_weight_star)
for i in agents:
    print(f"  {i}: {phi_star[i]} = {float(phi_star[i]):.6f}")
# Expected: center 1/2, leaves 1/(2*(2r-1)) for r=3 => 1/10
center_expected = Fraction(1, 2)
leaf_expected = Fraction(1, 10)
print(f"  Center matches? {phi_star[0] == center_expected}")
print(f"  Leaves match? {all(phi_star[i] == leaf_expected for i in range(1, n))}")

# ============================================================
# 2. Alternating path (m=3): 1->2->3, Y,N,Y
# ============================================================
print("\n=== Alternating path (3 agents) ===")
n = 3
agents = [1, 2, 3]
succ = {1: 2, 2: 3, 3: None}
q = n // 2 + 1   # 2

def yes_weight_path(S):
    w = 0
    for i in S:
        cur = i
        while True:
            if cur not in S:
                break
            if succ[cur] is None:
                w += 1
                break
            cur = succ[cur]
    return w

phi_path3 = shapley_values(agents, succ, q, yes_weight_path)
for i in agents:
    print(f"  {i}: {phi_path3[i]} = {float(phi_path3[i]):.6f}")
expected_path3 = {1: 0, 2: Fraction(1,2), 3: Fraction(1,2)}
print(f"  Matches paper? {all(phi_path3[i] == expected_path3[i] for i in agents)}")

# ============================================================
# 3. Alternating path (m=4): 1->2->3->4, Y,N,Y,N
# ============================================================
print("\n=== Alternating path (4 agents) ===")
n = 4
agents = [1, 2, 3, 4]
succ = {1: 2, 2: 3, 3: 4, 4: None}
q = n // 2 + 1   # 3
phi_path4 = shapley_values(agents, succ, q, yes_weight_path)
for i in agents:
    print(f"  {i}: {phi_path4[i]} = {float(phi_path4[i]):.6f}")
expected_path4 = {1: 0, 2: Fraction(1,3), 3: Fraction(1,3), 4: Fraction(1,3)}
print(f"  Matches paper? {all(phi_path4[i] == expected_path4[i] for i in agents)}")

# ============================================================
# 4. Non-alternating path (4 agents): 1->2->3->4, Y,Y,N,Y
#    Pruned graph: 2->3->4, 1 isolated sink
# ============================================================
print("\n=== Non-alternating path (Y,Y,N,Y) ===")
n = 4
agents = [1, 2, 3, 4]
# original edges: 1->2, 2->3, 3->4. After pruning: remove 1->2 (same type)
succ_pruned = {1: None, 2: 3, 3: 4, 4: None}
q = n // 2 + 1   # 3

def yes_weight_non_alt(S):
    # same logic using succ_pruned
    w = 0
    for i in S:
        cur = i
        while True:
            if cur not in S:
                break
            if succ_pruned[cur] is None:
                w += 1
                break
            cur = succ_pruned[cur]
    return w

phi_non_alt = shapley_values(agents, succ_pruned, q, yes_weight_non_alt)
for i in agents:
    print(f"  {i}: {phi_non_alt[i]} = {float(phi_non_alt[i]):.6f}")
expected_non_alt = {1: Fraction(1,12), 2: Fraction(1,12),
                    3: Fraction(5,12), 4: Fraction(5,12)}
print(f"  Matches paper? {all(phi_non_alt[i] == expected_non_alt[i] for i in agents)}")

# ============================================================
# 5. Middleman network: L1->M, L2->M, M->R, types Y,Y,N,Y
#    L1=1, L2=2, M=3, R=4
# ============================================================
print("\n=== Middleman network ===")
n = 4
agents = ['L1','L2','M','R']
succ_m = {'L1':'M', 'L2':'M', 'M':'R', 'R':None}
q = n // 2 + 1   # 3

def yes_weight_middleman(S):
    w = 0
    for i in S:
        cur = i
        while True:
            if cur not in S:
                break
            if succ_m[cur] is None:
                w += 1
                break
            cur = succ_m[cur]
    return w

phi_mid = shapley_values(agents, succ_m, q, yes_weight_middleman)
for i in agents:
    print(f"  {i}: {phi_mid[i]} = {float(phi_mid[i]):.6f}")
expected_mid = {'L1': Fraction(1,12), 'L2': Fraction(1,12),
                'M': Fraction(5,12), 'R': Fraction(5,12)}
print(f"  Matches paper? {all(phi_mid[i] == expected_mid[i] for i in agents)}")