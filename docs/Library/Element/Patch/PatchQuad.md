# PatchQuad

Patch of Quadrilateral Elements

* Number of DoFs: 2
* Number of Nodes: varies
* Support Mass
* Support Body Force

## Syntax

A key-value style is used.

```
element PatchQuad (1) -node (2...) -knotx (3...) -knoty (4...) -material (5) [-thickness (6)]
# (1) int, unique element (patch) tag
# (2...) int, node tags of control node polygon
# (3...) double, knot vector along x axis
# (4...) double, knot vector along y axis
# (5) int, material tag
# (6) double, thickness
```
