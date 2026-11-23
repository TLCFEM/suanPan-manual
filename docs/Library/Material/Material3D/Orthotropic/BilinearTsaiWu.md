# BilinearTsaiWu

Bilinear Hardening Tsai-Wu Model

## Background

This model uses the orthotropic elastic stiffness of [`OrthotropicElastic3D`](../Elastic/OrthotropicElastic3D.md) and associative plasticity with the Tsai-Wu yield criterion.
The full yield function, the nine strength parameters and the return mapping are derived in [`ExpTsaiWu`](ExpTsaiWu.md).
The only difference is the isotropic hardening law, which is piecewise linear in the equivalent plastic strain.

## Theory

The hardening function is $K(\bar\varepsilon_p)=1+H\bar\varepsilon_p$, where $H$ is the hardening ratio supplied as `(20)`.
For $H>0$ the yield surface grows linearly, $H=0$ gives perfect plasticity and $H<0$ gives linear softening.

!!! warning "implementation limitation"
    For negative `H` the code clamps the hardening function to zero once $\bar\varepsilon_p$ exceeds $-1/H$.
    The surface cannot shrink below zero size, so the softening branch ends abruptly.

## References

1. [Tsai-Wu failure criterion](https://en.wikipedia.org/wiki/Tsai%E2%80%93Wu_failure_criterion)
2. [10.1016/S0045-7825(02)00605-9](https://doi.org/10.1016/S0045-7825(02)00605-9)

## Syntax

```text title="BilinearTsaiWu"
material BilinearTsaiWu (1) (2...7) (8...10) (11...19) [20] [21]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, G_{xy}, G_{yz}, G_{zx}
# (8...10) double, three Poisson's ratios: v_{xy}, v_{yz}, v_{xz}
# (11...19) double, nine yield stresses
# [20] double, hardening ratio, default: 0.0
# [21] double, density, default: 0.0
```

## Remarks

The nine yield stresses are ordered as $\sigma_{11}^t,\sigma_{11}^c,\sigma_{22}^t,\sigma_{22}^c,\sigma_{33}^t,\sigma_{33}^c,\sigma_{12}^0,\sigma_{23}^0,\sigma_{13}^0$.
The six moduli are ordered as $E_1,E_2,E_3,G_{12},G_{23},G_{13}$ and the three Poisson's ratios as $\nu_{12},\nu_{23},\nu_{13}$.
No input is converted to absolute value, so positive elastic and strength parameters must be supplied.
Use [`Rotation3D`](../../Wrapper/Rotation3D.md) to align the material axes with a rotated layup.
