# PolyJ2

Polynomial Hardening J2 Model

The `PolyJ2` defines a J2 material with isotropic hardening.
The isotropic hardening is controlled by a polynomial.
The kinematic hardening is disabled.

## Theory

The `PolyJ2` model is a concrete implementation of the [`NonlinearJ2`](NonlinearJ2.md) framework with a polynomial isotropic hardening law.
The yield radius is

$$
k(p)=\sum_{i=0}^{n}a_i p^i,
$$

in which $$p$$ is the accumulated equivalent plastic strain and $$a_0$$ is the initial yield stress.
The kinematic contribution is $$h(p)=0$$, so the back stress remains zero.
The derivative passed to the local Newton corrector is

$$
k'(p)=\sum_{i=1}^{n}i\,a_i p^{i-1}.
$$

The return mapping solves the discrete consistency condition of [`CustomJ2`](CustomJ2.md), which reduces here to a denominator of $$2G+\dfrac{2}{3}k'(p)$$.
A negative polynomial value is clamped to zero, which makes the radius non-negative.

!!! warning "implementation limitation"
    The derivative is set to zero together with the clamped radius.
    A polynomial that dips below zero therefore changes the local tangent abruptly instead of retaining its analytic slope.

## Syntax

```text title="PolyJ2"
material PolyJ2 (1) (2) (3) (4) [(5)...]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, density
# [(5)...] double, parameters in polynomial
```

## Example

The isotropic hardening function is defined to be a polynomial function of equivalent plastic strain.

$$
\sigma_y(\bar\varepsilon_p)=a_0+a_1\bar\varepsilon_p+a_2\bar\varepsilon_p^2+\cdots+a_n\bar\varepsilon_p^n.
$$

Clearly, $$a_0$$ is the initial yielding stress.

To define, for example, the following hardening

$$
\sigma_y(\bar\varepsilon_p)=100+4000\bar\varepsilon_p+80000\bar\varepsilon_p^3
$$

with $$E=200000$$ and $$\nu=0.3$$, the following command can be used.

```
material PolyJ2 1 2E5 .3 .0 1E2 4E3 0. 8E4
```

## Remarks

The density is read as the fourth argument, before the polynomial coefficients.
The parser rejects fewer than three coefficients after the density.
The coefficients correspond to increasing powers of the accumulated plastic strain, so a zero coefficient must be written explicitly when a power is absent.
High-order polynomials can overflow or oscillate at large plastic strain, so keep the tabulated range in mind.
The local iteration requires $$E+k'(p)\geqslant0$$ over the whole loading history.
For a piecewise-linear curve use [`MultilinearJ2`](MultilinearJ2.md), and for an expression-defined curve use [`CustomJ2`](CustomJ2.md).
The same polynomial can be defined in one dimension with [`CustomMises1D`](../../Material1D/vonMises/CustomMises1D.md).
Use a three-dimensional solid element such as `C3D8` with this material.

## References

1. J. C. Simo and T. J. R. Hughes, *Computational Inelasticity*, Springer, New York, 1998, [doi:10.1007/b98904](https://doi.org/10.1007/b98904).
