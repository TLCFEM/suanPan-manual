# Mindlin

Mindlin Plate Element

* Number of Nodes: 4
* Number of DoFs: 3 (Translation, Translation, Rotation)

## Syntax

```
element Mindlin (1) (2...5) (6) (7) [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# (7) double, thickness
# [8] int, number of integration points, default: 5
```
