# PatchCube

Patch of Hexahedron Elements

* Number of DoFs: 3
* Number of Nodes: varies
* Support Mass
* Support Body Force

## Syntax

A key-value style is used.

```
element PatchCube (1) -node (2...) -knotx (3...) -knoty (4...) -knotz (5...) -material (6) [-thickness (7)]
# (1) int, unique element (patch) tag
# (2...) int, node tags of control node polygon
# (3...) double, knot vector along x axis
# (4...) double, knot vector along y axis
# (5...) double, knot vector along z axis
# (6) int, material tag
# (7) double, thickness
```
