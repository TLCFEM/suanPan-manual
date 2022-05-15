# materialtestbyload

This command category can be used to test most material models **depend on load/stress input only** without establishing
a FE model. Some wrappers and material models that rely on other material models cannot be tested in this way.

## Syntax

```
materialTestByLoad1D (1) (2) (3) [4...]
# (1) int, unique tag of the material model to use
# (2) double, size of per stress increment
# (3) int, number of steps along increment direction
# [4...] int, optional numbers of steps for stress history

materialTestByLoad2D (1) (2...4) (5) [6...]
# (1) int, unique tag of the material model to use
# (2...4) double, size of per stress increment
# (5) int, number of steps along increment direction
# [6...] int, optional numbers of steps for stress history

materialTestByLoad3D (1) (2...7) (8) [9...]
# (1) int, unique tag of the material model to use
# (2...7) double, size of per stress increment
# (8) int, number of steps along increment direction
# [9...] int, optional numbers of steps for stress history
```

## Remarks

1. The Newton-Raphson method is implemented to solve the corresponding strain increments. Thus softening models should
   not be tested in this way.
