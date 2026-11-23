# BilinearMises1D

Bilinear J2 Plasticity Model

## Theory

This model is an implementation of the [`Mises1D`](Mises1D.md) abstract model.

Compared to [`Bilinear1D`](Bilinear1D.md), only isotropic hardening is defined.
The kinematic hardening is set to zero.
There is no other significant difference.

The isotropic radius supplied to the [`Mises1D`](Mises1D.md) base class is

$$
k(p)=\sigma_{y0}+H_\text{iso}p,\qquad H_\text{iso}=E\,\dfrac{H}{1-H},
$$

where $$H$$ is the input hardening ratio and $$p$$ is the accumulated plastic strain.

!!! warning "implementation limitation"
    The conversion divides by $1-H$, and the code does not check that $H$ differs from unity.
    With $H=0$ the plastic modulus vanishes and the base class returns a zero tangent during plastic loading.
    The elastic modulus and the yield stress are converted to absolute values in the constructor.

Both derivatives required by the base class are constants, $$\mathrm{d}k/\mathrm{d}p=H_\text{iso}$$ and $$\mathrm{d}h/\mathrm{d}p=0$$.
Consequently the plastic corrector terminates in a single Newton update and the consistent tangent is $$E^{ep}=EH$$.

## Syntax

```text title="BilinearMises1D"
material BilinearMises1D (1) (2) (3) [4] [5]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, initial yield stress
# [4] double, hardening ratio, default: 0.0
# [5] double, density, default: 0.0
```

## Remarks

The elastic modulus and the yield stress are converted to absolute values in the constructor.
The hardening ratio must be smaller than unity because the isotropic modulus contains the factor $$1/(1-H)$$.
A negative hardening ratio gives linear softening and the radius is clamped at zero in the base class.
The stored history matches [`Mises1D`](Mises1D.md), namely the accumulated plastic strain in `initial_history(0)` and a permanently zero back stress in `initial_history(1)`.
A dedicated implementation of the same isotropic-only law is available as [`Bilinear1D`](Bilinear1D.md) with `beta` set to unity.

## Usage

Please refer to the [`Bilinear1D`](Bilinear1D.md) model.

## References

1. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
