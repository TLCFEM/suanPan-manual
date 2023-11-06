# Spring01

Spring Using Displacement

## Syntax

```
element Spring01 (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag
```

## Remarks

The `Spring01` uses displacement as the input quantity and compute force.
It can be used as a zero-length element to connect two nodes.

Note only infinitesimal strain/deformation formulation is supported.
If finite deformation, such a rigid body dynamics, is involved, analysts shall use `T2D2` and `T2D2S` elements.
