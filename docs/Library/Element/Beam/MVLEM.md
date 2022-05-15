# MVLEM

Multiple Vertical Line Element Model

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Rotation)

The `MVLEM` element is often used in modelling walls. It is in fact a simplified beam element with shear response.

Personally I do not recommend the usage of this element in any cases.

## Syntax

```
element MVLEM (1) (2) (3) (4) (5) ((6) (7) (8) (9) (10)...)
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag of shear spring
# (5) double, height of shear spring, ranges from 0 to 1
# (6) double, fibre width
# (7) double, fibre thickness
# (8) double, reinforcement ratio of target fibre
# (9) int, concrete material (host) tag
# (10) int, steel material tag
```

## Remarks

1. Parameters `(6)` to `(10)` form a group of parameters that define a single fibre, if there are multiple fibres, which
   is often the case, repeat five parameter group for each fibre.
