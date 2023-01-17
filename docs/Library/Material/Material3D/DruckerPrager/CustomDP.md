# CustomDP

Drucker-Prager model With Custom Hardening

## Syntax

```
material CustomDP (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, \eta_y
# (5) double, \eta_f
# (6) double, \xi
# (7) unsigned, cohesion expression tag
# [8] double, density, default: 0.0
```

***The expressions shall be able to compute derivatives.***
