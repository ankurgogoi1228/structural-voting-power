from fractions import Fraction
from math import factorial

# ---------- 1. Network definition ----------
n = 7
agents = list(range(1, n+1))          # 1, 2, ..., 7

# Type of each agent (Y = yes, N = no)
theta = {1: 'Y', 2: 'Y', 3: 'Y', 4: 'Y',
         5: 'N', 6: 'N', 7: 'Y'}

# Successor in the delegation graph (None = sink)
succ = {1: 5, 2: 5, 3: 6, 4: 6,
        5: 7, 6: 7, 7: None}

# Quota: floor(n/2) + 1 = 4
q = n // 2 + 1

# ---------- 2. Vote‑loss yes‑weight ----------
def yes_weight(S_set):
    """Total effective yes‑votes for coalition S_set."""
    w = 0
    for i in S_set:
        cur = i
        while True:
            if cur not in S_set:      # chain left coalition
                break
            nxt = succ[cur]
            if nxt is None:           # sink reached inside coalition
                w += 1
                break
            cur = nxt
    return w

# ---------- 3. Build the simple game v(S) ----------
# Use bit masks (0..127) for compactness
v = {}
for mask in range(1 << n):
    S = {i for i in agents if mask & (1 << (i-1))}
    v[mask] = 1 if yes_weight(S) >= q else 0

# ---------- 4. Compute Shapley values ----------
phi = {i: Fraction(0, 1) for i in agents}
fact = [factorial(k) for k in range(n+1)]   # cache factorials

for i in agents:
    bit_i = 1 << (i-1)
    for mask in range(1 << n):
        if mask & bit_i:
            continue                     # i must be absent
        if v[mask | bit_i] == 1 and v[mask] == 0:
            k = mask.bit_count()          # |S|
            weight = Fraction(fact[k] * fact[n - k - 1], fact[n])
            phi[i] += weight

# ---------- 5. Display results ----------
print("Shapley values for the balanced binary tree (n=7, q=4):")
print("-" * 50)
for i in agents:
    f = float(phi[i])
    print(f"φ_{i} = {phi[i]}   (≈ {f:.6f})")

print(f"\nSum = {sum(phi.values())}   (float: {float(sum(phi.values()))})")
print("Expected from correct enumeration: sum = 1.")

# Optional check against the paper's erroneously reported values
print("\nComparison with paper's (incorrect) appendix values:")
paper = {1: Fraction(8,105), 2: Fraction(8,105), 3: Fraction(8,105),
         4: Fraction(8,105), 5: Fraction(13,105), 6: Fraction(13,105),
         7: Fraction(34,105)}
for i in agents:
    print(f"  Agent {i}:  true {phi[i]:>8}  paper {paper[i]:>8}  diff = {phi[i] - paper[i]}")