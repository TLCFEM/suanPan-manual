# ArcLength

## Syntax

```
step ArcLength (1) (2) (3) (4)
# (1) int, unique step tag
# (2) int, reference node tag
# (3) int, reference dof tag
# (4) double, reference magnitude of applied load
```

## Remarks

1. A [`Ramm`](../Solver/Ramm.md) solver with default parameters is automatically enabled if no valid `Ramm` solver is
   defined. Not all storage schemes are supported, please check `Ramm` documentation.
