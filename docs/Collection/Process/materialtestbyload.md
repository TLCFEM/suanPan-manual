# materialtestbyload

This command category tests most material models **that depend on load/stress input only** without establishing an FE model.
Some wrappers and material models that rely on other material models cannot be tested in this way.

## Syntax

```text title="materialtestbyload"
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

materialTestByLoadWithBase3D (1) (2...7) (8...13) (14) [15...]
# (1) int, unique tag of the material model to use
# (2...7) double, base stress vector applied in a single increment before cycling
# (8...13) double, size of per stress increment during cycling
# (14) int, number of steps along increment direction
# [15...] int, optional numbers of steps for stress history
```

## Remarks

1. The Newton-Raphson method is implemented to solve the corresponding strain increments.
   Softening models should therefore not be tested in this way.
2. The `WithBase` variant first applies the given base stress, then cycles with the specified stress increment.
   It keeps the mean stress constant while the shear stress is cycled, as used in the [cyclic regimes example](../../Example/Geotechnical/cyclic-regimes-of-sand.md).
