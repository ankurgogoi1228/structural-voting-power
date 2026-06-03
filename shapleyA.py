from fractions import Fraction
from math import factorial

# ---------- 1. Agents and structure ----------
n = 6
agents = list(range(6))                     # 0..5
names = ['C1', 'L1a', 'L1b', 'C2', 'L2a', 'L2b']

# Component centres and their leaves
centers = [0, 3]
leaves_of = {0: [1, 2], 3: [4, 5]}

q = 4   # majority quota: floor(6/2) + 1

# ---------- 2. Vote‑loss yes‑weight ----------
def yes_weight(S_set):
    w = 0
    for c in centers:
        if c in S_set:               # centre itself votes yes
            w += 1
            for leaf in leaves_of[c]:
                if leaf in S_set:    # leaf delegation stays inside S
                    w += 1
    # leaves whose centre is absent contribute 0
    return w

# ---------- 3. Build simple game v(S) ----------
v = {}
for mask in range(1 << n):
    S = {i for i in agents if mask & (1 << i)}
    v[mask] = 1 if yes_weight(S) >= q else 0

# ---------- 4. Shapley value ----------
phi = {i: Fraction(0, 1) for i in agents}
fact = [factorial(k) for k in range(n + 1)]

for i in agents:
    bit_i = 1 << i
    for mask in range(1 << n):
        if mask & bit_i:
            continue               # i must be absent
        k = mask.bit_count()       # size of S
        if v[mask | bit_i] == 1 and v[mask] == 0:
            weight = Fraction(fact[k] * fact[n - k - 1], fact[n])
            phi[i] += weight

# ---------- 5. Output ----------
print("Shapley values for the two‑component star (n = 6, q = 4):")
print("-" * 55)
for i in agents:
    print(f"  {names[i]:>4}: {str(phi[i]):>8}  = {float(phi[i]):.6f}")

total = sum(phi.values())
print(f"\nSum = {total}  (float: {float(total):.6f})")

# Symmetry checks
print("\nSymmetry:")
print(f"  C1 == C2? {phi[0] == phi[3]}")
print(f"  all leaves equal? {phi[1] == phi[2] == phi[4] == phi[5]}")

# Verification against paper's claim
paper_center = Fraction(9, 30)   # 3/10
paper_leaf   = Fraction(3, 30)   # 1/10
print("\nVerification against paper's original (erroneous) values:")
print(f"  C1:  paper {paper_center}, computed {phi[0]}, match: {phi[0] == paper_center}")
print(f"  leaf: paper {paper_leaf}, computed {phi[1]}, match: {phi[1] == paper_leaf}")

# Corrected values
print("\nCorrect values: centres 2/5, leaves 1/20")