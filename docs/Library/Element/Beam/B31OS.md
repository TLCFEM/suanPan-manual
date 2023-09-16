# B31OS

3D Displacement Based Beam With Torsion and Warping

* Number of Nodes: 2
* Number of DoFs: 7 (Translation, Translation, Translation, Rotation, Rotation, Rotation, Warping)

## Reference

1. [Distributed plasticity analysis of steel building structural systems](https://www.proquest.com/dissertations-theses/distributed-plasticity-analysis-steel-building/docview/304696456/se-2)

## Syntax

```
element B31OS (1) (2) (3) (4) (5) [6] [7]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# (5) int, orientation tag
# [6] int, number of integration points, default: 6
# [7] int, nonlinear geometry switch, default: false
```

## Remarks

1. The Lobatto integration is used by default. The number of integration points ranges from 3 to 20.
2. Please check [`orientation`](Orientation.md) for its definition.
3. To use the corotational formulation for nonlinearity, please attach a corotational
   transformation [`B3DOSC`](Orientation.md).
4. The reference also introduced a circumvention of membrane locking.
   It _**is**_ implemented in this element.
   The Hermite shape function is used for the interpolation of $$\phi$$.
5. A 3D OS section is required for this element.

The Alemdar's thesis contains a few typos. The following expressions are confirmed to be correct and used in the
implementation.

1. Eq. 7.12
2. Eq. 7.41
3. Eq. 7.58
