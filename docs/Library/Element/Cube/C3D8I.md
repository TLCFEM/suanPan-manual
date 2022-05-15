# C3D8I

Linear Cube/Brick With Incompatible Modes

* Number of Nodes: 8
* Number of DoFs: 3 (All Translation)
* Supports Body Force
* Integration Scheme: Irons Six-Point
* Constant Consistent Mass Matrix With Same Order Integration

## Syntax

```
element C3D8I (1) (2...9) (10)
# (1) int, unique element tag
# (2...9) int, eight corner nodes with conventional order
# (10) int, material tag
```

## Remarks

1. `C3D8I` is `C3D8` with incompatible modes.
2. Nonlinearity is not implemented in `C3D8I`.
