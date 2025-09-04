# BilinearMises1D

Bilinear J2 Plasticity Model

## Theory

This model is an implementation of the [`Mises1D`](Mises1D.md) abstract model.

Compared to[`Bilinear1D`](Bilinear1D.md), only isotropic hardening is defined.
The kinematic hardening is set to zero.
There is no other significant difference.

## Syntax

```
material BilinearMises1D (1) (2) (3) [4] [5]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, initial yield stress
# [4] double, hardening ratio, default: 0.0
# [5] double, density, default: 0.0
```

## Usage

Please refer to the [`Bilinear1D`](Bilinear1D.md) model.
