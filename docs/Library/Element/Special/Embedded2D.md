# Embedded2D

2D Embedded Element

## Syntax

```
element Embedded2D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, host element tag
# (3) int, slave node tag
# [4] double, penalty factor, default: 1E4
```

## Remarks

1. Currently, the following element types are supported: [`CP4`](../Membrane/Plane/CP4.md)
   , [`CP5`](../Membrane/Plane/CP5.md), [`CP7`](../Membrane/Plane/CP7.md) and [`CP8`](../Membrane/Plane/CP8.md).
