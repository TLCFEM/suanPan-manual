# Spring02

Spring Using Strain

## Syntax

```
element Spring02 (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag
```

# Remarks

The `Spring02` uses strain as the input quantity and compute stress.

Note only infinitesimal strain/deformation formulation is supported.
If finite deformation, such a rigid body dynamics, is involved, analysts shall use `T2D2` and `T2D2S` elements.