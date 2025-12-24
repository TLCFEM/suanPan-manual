# Balloon1D

Uniaxial Balloon Model

## Syntax

```text
material Balloon1D ${1:(1)} ${2:(2)} ${3:(3)} ${4:(4)} ${5:(5 6 7 8)} ${6:(9 10 11 12)} ${7:(13 14 15 16)} ${8:(17 18 19 20)} ${9:(21 22 23 24)} ${10:(25)} ${11:[(26) (27) (28)...]}
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, k_r
# (4) double, load reversal memory size
# (5 6 7 8) double, u bound, initial, linear, saturation, rate
# (9 10 11 12) double, fm bound, initial, linear, saturation, rate
# (13 14 15 16) double, fc bound, initial, linear, saturation, rate
# (17 18 19 20) double, back stress bound, initial, linear, saturation, rate
# (21 22 23 24) double, similarity bound, initial, linear, saturation, rate
# (25) double, density
# (26) string, token, one of '-fc', '-ac', '-na', '-nd'
# (27 28) double, saturation, rate
```
