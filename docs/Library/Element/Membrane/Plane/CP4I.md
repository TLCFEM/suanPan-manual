# CP4I

Bilinear Incompatible Quadrilateral

* Number of Nodes: 4
* Number of DoFs: 2 (Translation, Translation)
* Integration Scheme: 2nd Order Gauss
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Syntax

```
element CP4I (1) (2...5) (6) [7]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```
