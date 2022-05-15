# Embed2D

The `Embed2D` constraint implements the embedded constraint in 2D space via multiplier method.

## Syntax

```
constraint Embed2D (1) (2) (3)
# (1) int, unique constraint tag
# (2) int, host element tag
# (3) int, embedded node tag
```

## Remarks

1. The `Embed2D` constraint is only implemented with linear formulation.
2. Currently, the following host element types are supported: [`CP4`](../Element/Membrane/Plane/CP4.md)
   , [`CP5`](../Element/Membrane/Plane/CP5.md), [`CP7`](../Element/Membrane/Plane/CP7.md)
   and [`CP8`](../Element/Membrane/Plane/CP8.md).
