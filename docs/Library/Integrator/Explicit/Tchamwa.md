# Tchamwa

First order explicit time integration method using the Tchamwa scheme.

References:

1. [10.1002/nme.6574](https://doi.org/10.1002/nme.6574)

## Syntax

```text
integrator Tchamwa (1) [2]
# (1) int, unique integrator tag
# [2] double, spectral radius, \rho_\infty, default: 0.5
```

## Theory

The integration relationship is given by the following.

$$
u_{n+1}=u_n+\Delta{}tv_n+\phi\Delta{}t^2a_n,
$$

$$
v_{n+1}=v_n+\Delta{}ta_n,
$$

where

$$
\phi=\dfrac{2}{1+\rho_\infty}.
$$

The Tchamwa scheme has a first order accuracy and controllable numerical dissipation.

## Remarks

If the model is linear elastic, it is possible to indicate using

```text
set linear_system true
```

to speed up the computation.
