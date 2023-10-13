# ArcLength

## Syntax

```
step ArcLength (1) (2) (3) (4)
# (1) int, unique step tag
# (2) int, reference node tag
# (3) int, reference dof tag
# (4) double, reference magnitude of applied load
```

The step size in an arc-length analysis is now the arc length.
One can use the following to control stepping strategy.

```
set ini_step_size (1)
set min_step_size (1)
set max_step_size (1)
# (1) double, step size (arc length)

set fixed_step_size (1)
# (1) bool, flag to indicate if to fix the arc length
```

## Remarks

1. A [`Ramm`](../Solver/Ramm.md) solver with default parameters is automatically enabled if no valid `Ramm` solver is
   defined. Not all storage schemes are supported, please check `Ramm` documentation.
