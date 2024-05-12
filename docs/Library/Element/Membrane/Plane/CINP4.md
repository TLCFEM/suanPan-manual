# CINP4

Bilinear Infinite Quadrilateral

* Number of Nodes: 4
* Number of DoFs: 2 (Translation, Translation)

## References

1. [https://doi.org/10.1016/0045-7949(84)90019-1](https://doi.org/10.1016/0045-7949(84)90019-1)

## Syntax

```
element CINP4 (1) (2...5) (6) [7]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```

## Remarks

1. The first two nodes are finite nodes while the latter two are infinite nodes.
