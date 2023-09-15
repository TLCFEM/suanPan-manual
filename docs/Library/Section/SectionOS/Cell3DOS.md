# Cell3DOS

Basic Building Block for 3D OS Section

## Reference

1. [Distributed plasticity analysis of steel building structural systems](https://www.proquest.com/dissertations-theses/distributed-plasticity-analysis-steel-building/docview/304696456/se-2)

## Syntax

```
section Cell3DOS (1) (2) (3) (4) (5) [6] [7]
# (1) int, unique section tag
# (2) double, area
# (3) double, sectional coordiante
# (4) double, n
# (5) int, material tag
# [6] double, eccentricity/location along y axis, default: 0.0
# [7] double, eccentricity/location along z axis, default: 0.0
```

## Remarks

The parameters `(3)` and `(4)` are $$\bar\omega$$ and $$n$$ in Eq. 7.37 and Eq. 7.39. They are used in the calculation of torsion related deformation.

The attached material needs to be an OS material.
