# EB31OS

Elastic 3D Beam With Open Section

* Number of Nodes: 2
* Number of DoFs: 7 (Translation, Translation, Translation, Rotation, Rotation, Rotation, WARPING)

## Syntax

```
element EB31OS (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) [12]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) double, elastic modulus, E
# (5) double, shear modulus, G
# (6) double, area, A
# (7) double, major/strong axis moment of inertia, I_z
# (8) double, minor/weak axis moment of inertia, I_y
# (9) double, torsional constant, J
# (10) double, warping constant, I_w
# (11) int, orientation tag
# [12] bool, nonlinear geometry switch, default: false
```

## Remarks

1. Please check [`orientation`](Orientation.md) for its definition, for example, `B3DOSL` and `B3DOSC`.
2. To use the corotational formulation for nonlinearity, please attach a corotational formulation enabled `orientation`.
