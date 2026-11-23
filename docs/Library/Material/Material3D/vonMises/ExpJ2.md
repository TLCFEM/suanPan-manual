# ExpJ2

Exponential Isotropic Hardening J2 Model

The kinematic hardening is not defined in this model.

## Theory

The backbone function is defined as

$$
\sigma=\sigma_y\left(\left(1+a\right)e^{-b\varepsilon_p}-ae^{-2b\varepsilon_p}\right),
$$

where $$a$$ and $$b$$ are two constants that control the shape of the backbone.
The initial stiffness $$\sigma'|_{\varepsilon_p=0}=\sigma_y(a-1)b$$.

This model is a concrete implementation of the [`NonlinearJ2`](NonlinearJ2.md) framework.
It supplies the isotropic radius $$k(p)$$ with the backbone above, where $$p$$ is the accumulated equivalent plastic strain, and it sets the back-stress magnitude to $$h(p)=0$$.
The derivative required by the local Newton corrector is

$$
k'(p)=\sigma_y b\left[2a e^{-2bp}-(1+a)e^{-bp}\right].
$$

The backbone has a single stationary point at $$e^{-bp}=(1+a)/(2a)$$, where it attains $$k_\text{max}/\sigma_y=(1+a)^2/(4a)$$.
For $$a>1$$ and $$b>0$$ the response hardens first and softens after that peak, while $$0<a<1$$ gives immediate softening.
The value $$a=1$$ gives zero initial hardening slope and a subsequent decrease of the radius.
The local iteration requires $$E+k'(p)\geqslant0$$, so strongly softening parameter sets can fail to converge.

!!! info "deviation from theory"
    A monotone Voce or exponential saturation law increases towards a limit without softening.
    This backbone instead turns over and decays towards zero after its peak, so it is not a standard exponential hardening law.

!!! warning "implementation limitation"
    A negative isotropic radius is clamped to zero and its derivative is discarded.
    The softening branch is therefore truncated at zero stress rather than followed into negative yield radii.

## Remarks

The yield stress is converted to its absolute value in the constructor, but $$a$$ and $$b$$ are taken as given.
The parameter $$b$$ controls the rate at which the peak is approached and has units of inverse plastic strain.
The parameter $$a$$ controls the peak amplification defined above and should normally exceed unity for a hardening response.
The softening branch of the backbone is not regularised, so a negative tangent can cause mesh-dependent localisation.
Use [`PolyJ2`](PolyJ2.md) or [`MultilinearJ2`](MultilinearJ2.md) for a monotone alternative, [`ArmstrongFrederick`](ArmstrongFrederick.md) for Voce saturation plus kinematic hardening, and [`CustomJ2`](CustomJ2.md) for an arbitrary hardening law.
The uniaxial counterpart is [`ExpMises1D`](../../Material1D/vonMises/ExpMises1D.md).
Use a three-dimensional solid element such as `C3D8` with this material.

## References

1. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
2. [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4)
## Syntax

```text title="ExpJ2"
material ExpJ2 (1) (2) (3) (4) (5) (6) [7]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, yield stress
# (5) double, a
# (6) double, b
# [7] double, density, default: 0.0
```
