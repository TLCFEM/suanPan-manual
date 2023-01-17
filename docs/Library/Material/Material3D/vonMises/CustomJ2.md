# CustomJ2

J2 Plasticity Model With Custom Hardening

## Theory

This model is an implementation of the [`NonlinearJ2`](NonlinearJ2.md) abstract model.

## Syntax

```
material CustomJ2 (1) (2) (3) (4) (5) [6]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, possions ratio
# (4) int, isotropic hardening expression tag
# (5) int, kinematic hardening expression tag
# [6] double, density, default: 0.0
```

## Remarks

Both hardening functions shall be defined in terms of the equivalent plastic strain.

The isotropic hardening function evaluates to the yield stress for trivial equivalent plastic strain.

The kinematic hardening function evaluates to zero for trivial equivalent plastic strain.

The usage is similar to that of [`CustomMises1D`](../../Material1D/vonMises/CustomMises1D.md).

***The expressions shall be able to compute derivatives.***