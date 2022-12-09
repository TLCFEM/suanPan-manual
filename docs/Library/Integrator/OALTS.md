# OALTS

Optimal A-stable Linear Two-Step Method

References:

1. [10.1002/nme.6188](https://doi.org/10.1002/nme.6188)
2. [10.1002/nme.6623](https://doi.org/10.1002/nme.6623)

## Syntax

```text
integrator OALTS (1) [2]
# (1) int, unique integrator tag
# [2] double, spectral radius, default: 0.5
```

## Remarks

This method is closely related to the [Generalised-Alpha](GeneralizedAlpha.md) method (on first order ODEs).
See the second reference for more details, also see [10.1016/j.compstruc.2017.08.013](https://doi.org/10.1016/j.compstruc.2017.08.013).

This method requires a fixed time step.
The initial time step is used for time marching.
For example,

```text
set ini_step_size 1E-2
```

The `fixed_step_size` command such as

```
set fixed_step_size true
```

is not required and this flag is always `true`.