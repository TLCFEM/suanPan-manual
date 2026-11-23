# NLE3D01

Nonlinear Elastic 3D Model

## Syntax

```text title="NLE3D01"
material NLE3D01 (1) (2) (3) (4) (5) [6]
# (1) int, unique material tag
# (2) double, bulk modulus
# (3) double, reference strain
# (4) double, reference stress
# (5) double, m
# [6] double, density, default: 0.0
```

## Theory

The strain energy potential is expressed as

$$
W=\dfrac{9}{2}K\varepsilon_v^2+\dfrac{\varepsilon_0\sigma_0}{1-m}\left(\dfrac{\varepsilon_p}{\varepsilon_0}\right)^{(
1-m)},
$$

where $$K$$ is the bulk modulus, $$\varepsilon_0$$ is the reference strain, $$\sigma_0$$ is the reference stress and $$m\in[0,1]$$ is an exponent that controls nonlinearity.
The volumetric strain $$\varepsilon_v$$ and equivalent strain $$\varepsilon_p$$ are expressed as

$$
\varepsilon_v=\text{trace}\left(\varepsilon\right),\qquad\varepsilon_p=\sqrt{\dfrac{2}{3}\varepsilon_d:
\varepsilon_d}.
$$

The potential is supplied to the abstract framework [`IsotropicNonlinearElastic3D`](IsotropicNonlinearElastic3D.md) through the derivatives with respect to $$\varepsilon_v$$ and $$\varepsilon_s=\varepsilon_p^2$$.
The volumetric derivative implemented in the code is $$\partial W/\partial\varepsilon_v=9K\varepsilon_v$$, because the constructor stores the internal value `bulk = 9K`.

!!! info "deviation from theory"
    The volumetric energy is $$\tfrac92K\varepsilon_v^2$$ instead of the conventional $$\tfrac12K\varepsilon_v^2$$.
    The command-line argument `K` is therefore not the usual small-strain bulk modulus.

The deviatoric derivative returned by the code is

$$
\dfrac{\partial W}{\partial\varepsilon_s}=\dfrac{\sigma_0\varepsilon_0^{-m}}{2}\left(\varepsilon_p^2\right)^{(m-1)/2}.
$$

By the chain rule $$\partial W/\partial\varepsilon_p=2\varepsilon_p\,\partial W/\partial\varepsilon_s$$, so the equivalent stress is $$\sigma_p=\sigma_0(\varepsilon_p/\varepsilon_0)^m$$ and the energy corresponding to this derivative is $$W_\mathrm{dev}=\sigma_0\varepsilon_0(1+m)^{-1}(\varepsilon_p/\varepsilon_0)^{1+m}$$.
The implemented deviatoric exponent is therefore $$1+m$$ rather than the $$1-m$$ printed in the expression above, and the code should be consulted when calibrating $$m$$.

!!! warning "implementation limitation"
    The displayed strain energy uses the exponent $$1-m$$, but the implemented derivative integrates to the power $$1+m$$.
    Calibrate `m` against the implemented derivative rather than against the displayed expression.

## Remarks

The order is `(2)` bulk modulus $$K$$, `(3)` reference strain $$\varepsilon_0$$, `(4)` reference stress $$\sigma_0$$, and `(5)` exponent $$m$$, followed by the optional density.
The parameters $$\varepsilon_0$$ and $$\sigma_0$$ are converted to absolute values and $$m$$ is clamped to $$[0,1]$$.

!!! warning "implementation limitation"
    The reference strain and stress are converted to their absolute values and `m` is clamped to $$[0,1]$$, so negative values are silently replaced rather than rejected.

The internal bulk modulus is nine times the input $$K$$, so the input is not the conventional bulk modulus of linear elasticity and must be calibrated against the given energy definition.
At $$\varepsilon_p=\varepsilon_0$$ the equivalent stress equals $$\sigma_0$$, which gives a direct way to determine the reference stress from a uniaxial curve.
The squared equivalent strain is floored at machine epsilon, so $$m<1$$ produces a very large initial deviatoric tangent rather than a true singularity.

!!! warning "implementation limitation"
    The floor on $$\varepsilon_s$$ controls the initial tangent when $$m<1$$.
    The tangent at the origin is finite but depends on the floor value.

For $$m=0$$ the deviatoric response is linear in $$\varepsilon_p$$ with constant equivalent stress $$\sigma_0$$.
This is a small-strain model based on the infinitesimal strain tensor, so nonlinear geometry is not required.

## References

1. [ISBN 978-0-486-69648-5](https://search.worldcat.org/search?q=bn:9780486696485)
