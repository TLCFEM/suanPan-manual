# NLE1D01

Nonlinear Elastic 1D Type 01

The `NLE1D01` material is a smoothed uniaxial bilinear elastic material model which uses the MP formula to approximate
the bilinear backbone.

## Syntax

```
material NLE1D01 (1) (2) (3) (4) [5] [6]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, turning stress
# (4) double, hardening ratio
# [5] double, radius of transition, default: 20
# [6] double, density, default: 0
```