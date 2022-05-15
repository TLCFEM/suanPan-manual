# Embedded3D

3D Embedded Element

## Syntax

```
element Embedded3D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, host element tag
# (3) int, slave node tag
# [4] double, penalty factor, default: 1E4
```

## Remarks

1. Currently, the following element types are supported: [`C3D8`](../Cube/C3D8.md) and [`C3D20`](../Cube/C3D20.md).
