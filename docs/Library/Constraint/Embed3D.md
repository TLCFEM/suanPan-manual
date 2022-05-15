# Embed3D

The `Embed3D` constraint implements the embedded constraint in 3D space via multiplier method.

## Syntax

```
constraint Embed3D (1) (2) (3)
# (1) int, unique constraint tag
# (2) int, host element tag
# (3) int, embedded node tag
```

## Remarks

1. The `Embed3D` constraint is only implemented with linear formulation.
2. Currently, the following host element types are supported: [`C3D8`](../Element/Cube/C3D8.md)
   and [`C3D20`](../Element/Cube/C3D20.md).
