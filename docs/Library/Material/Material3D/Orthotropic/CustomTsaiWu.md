# CustomTsaiWu

Tsai-Wu Model With Custom Isotropic Hardening

## Background

This model uses the orthotropic elastic stiffness of [`OrthotropicElastic3D`](../Elastic/OrthotropicElastic3D.md) and associative plasticity with the Tsai-Wu yield criterion.
The full yield function, the nine strength parameters and the return mapping are derived in [`ExpTsaiWu`](ExpTsaiWu.md).

## Theory

The isotropic hardening function is supplied by the expression with tag `(20)`, $$K(\bar\varepsilon_p)=f(\bar\varepsilon_p)$$.
Its derivative $$\mathrm dK/\mathrm d\bar\varepsilon_p$$ is obtained from the gradient of the same expression and enters the consistent tangent.

!!! warning "implementation limitation"
    The expression must be univariate, must evaluate to unity at zero plastic strain and must supply a gradient.
    Initialization fails with an error if any of these conditions is not met.

## Syntax

```text title="CustomTsaiWu"
material CustomTsaiWu (1) (2...7) (8...10) (11...19) (20) [21]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, G_{xy}, G_{yz}, G_{zx}
# (8...10) double, three Poisson's ratios: v_{xy}, v_{yz}, v_{xz}
# (11...19) double, nine yield stresses
# (20) int, isotropic hardening expression tag
# [21] double, density, default: 0.0
```

***The expressions shall be able to compute derivatives.***

## Remarks

The nine yield stresses are ordered as $$\sigma_{11}^t,\sigma_{11}^c,\sigma_{22}^t,\sigma_{22}^c,\sigma_{33}^t,\sigma_{33}^c,\sigma_{12}^0,\sigma_{23}^0,\sigma_{13}^0$$.
The six moduli are ordered as $$E_1,E_2,E_3,G_{12},G_{23},G_{13}$$ and the three Poisson's ratios as $$\nu_{12},\nu_{23},\nu_{13}$$.
No input is converted to absolute value, so positive elastic and strength parameters must be supplied.
Use [`Rotation3D`](../../Wrapper/Rotation3D.md) to align the material axes with a rotated layup.

## Example

```text
expression SimpleScalar 1 x 1+.1x
material CustomTsaiWu 1 1E5 1E5 1E5 1E5 1E5 1E5 .3 .3 .3 400 300 400 300 250 200 200 200 200 1
```
