# Sleeve3D

The `Sleeve3D` constraint keeps the distance between two nodes inside a specified interval.
It combines the effects of [`MinimumGap3D`](MinimumGap3D.md) and [`MaximumGap3D`](MaximumGap3D.md) using one Lagrange multiplier.

## Syntax

```text title="Sleeve3D"
Sleeve3D (1) (2) (3) (4) (5)
constraint Sleeve3D (1) (2) (3) (4) (5)
# (1) int, unique constraint tag
# (2) int, node tag
# (3) int, node tag
# (4) double, minimum gap
# (5) double, maximum gap
```

## Theory

The constraint is inactive while the current distance lies strictly between the two limits.
The limits are squared internally and compared with the squared chord length, so the arguments are distances rather than squared distances.
The order of the two limits is irrelevant since the smaller value is always taken as the lower bound.
The participating DoFs are `1`, `2` and `3`.

## Remarks

The constraint is enforced exactly and is released once the distance returns inside the interval; as for [`FixedLength`](FixedLength.md), it shall not be used with global damping models in dynamic analysis.

## Example

```text
node 1 0 0 0
node 2 1 0 0
constraint Sleeve3D 1 1 2 0.5 2.
```
