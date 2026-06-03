# Structural Voting Power in Liquid Democracy

This repository contains the exact computational verification scripts for evaluating game-theoretic power distributions in liquid democracy networks under the **vote-loss boundary-severing rule**.

## Repository Structures
* `all.py`: Master combinatorial evaluation script covering multiple baseline topologies (Star, Alternating Paths, and Middleman Networks).
* `shapleyA.py`: Dedicated exact coalitional enumeration script verifying the **Two-Component Star** network model topology ($n=6, q=4$).
* `shapleyB.py`: Dedicated matrix simulation and exact evaluation code verifying structural voting power allocations within the **Balanced Binary Tree** network model ($n=7, q=4$).

## Setup & Execution
The scripts use standard library components and the `fractions.Fraction` module to guarantee arbitrary-precision evaluation without rounding distortions. 

To run any verification test, execute the following from your terminal:
```bash
python shapleyA.py
python shapleyB.py
