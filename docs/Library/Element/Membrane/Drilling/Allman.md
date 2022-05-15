# Allman

Allman's Triangle With Drilling DoFs

* Number of Nodes: 3
* Number of DoFs: 3 (Translation, Translation, Rotation)

## Syntax

```
element Allman (1) (2...4) (5) [6]
# (1) int, unique element tag
# (2...4) int, node i, j, k
# (5) int, material tag
# [6] double, element thickness, default: 1.0
```

## Remarks

* Three middle points on edges are used as integration points.
