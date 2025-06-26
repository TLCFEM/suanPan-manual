# GSSE

General Explicit Integration Algorithm (GSSE)

References:

1. [10.1002/nme.6574](https://doi.org/10.1002/nme.6574)

## Syntax

```text
integrator GSSE (1) [2]
# (1) int, unique integrator tag
# [2] double, spectral radius, \rho_b, default: 0.5
```

## Remarks

If the model is linear elastic, it is possible to indicate using

```text
set linear_system true
```

to speed up the computation.

!!! Warning
    When $$\rho_b<0.5$$, the algorithm extrapolates.

## Accuracy Analysis

![gsse-0.0](gsse-0.0.svg)
![gsse-0.5](gsse-0.5.svg)
![gsse-1.0](gsse-1.0.svg)
