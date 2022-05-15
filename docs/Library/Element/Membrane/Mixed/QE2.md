# QE2

Mixed Four-Node Quadrilateral Element

* Number of Nodes: 4
* Number of DoFs: 2
* Supports Body Force
* Integration Scheme: 2nd Order Gauss
* Constant Consistent Mass Matrix With Same Order Integration

## Reference

1. [https://doi.org/10.1002/nme.1620381102](https://doi.org/10.1002/nme.1620381102)

## Syntax

```
element QE2 (1) (2...5) (6) [7]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```
