# BilinearJ2

Bilinear J2 Plasticity

## Theory

The `BilinearJ2` model is a J2 plasticity model with a bilinear stress-strain curve and a hardening response that can be split between isotropic and kinematic parts.
It is the three-dimensional counterpart of [`Bilinear1D`](../../Material1D/vonMises/Bilinear1D.md) and a special case of the framework described in [`CustomJ2`](CustomJ2.md).

The yield function is

$$
F=\sqrt{\dfrac{3}{2}(\mathbf s-\mathbf\beta):(\mathbf s-\mathbf\beta)}-\left(\sigma_y+H_\text{iso}p\right),
$$

in which $$\mathbf s=\mathrm{dev}\,\mathbf\sigma$$, $$\mathbf\beta$$ is the back stress, and $$p$$ is the accumulated plastic strain.
The input hardening ratio $$h$$ is converted to a plastic modulus $$E_p=Eh/(1-h)$$, which is then split as

$$
H_\text{iso}=\beta E_p,\qquad H_\text{kin}=(1-\beta)E_p.
$$

Thus $$\beta=1$$ gives pure isotropic hardening and $$\beta=0$$ gives pure linear kinematic hardening.

!!! warning "implementation limitation"
    The yield radius is clamped to zero when the linear isotropic branch would become negative.
    A negative hardening ratio therefore gives a truncated softening response rather than a negative yield radius.

A radial return is used.
With the trial shifted stress $$\mathbf\xi=\mathrm{dev}\,\mathbf\sigma^{tr}-\mathbf\beta_n$$ and $$G=E/[2(1+\nu)]$$, the multiplier is obtained in closed form from

$$
\Delta\gamma=\dfrac{\lVert\mathbf\xi\rVert-\sqrt{2/3}\,(\sigma_y+H_\text{iso}p_n)}{2G+\dfrac{2}{3}\left(H_\text{iso}+H_\text{kin}\right)}.
$$

The updates are $$\mathbf\sigma=\mathbf\sigma^{tr}-2G\Delta\gamma\,\mathbf n$$, $$\mathbf\beta=\mathbf\beta_n+\dfrac{2}{3}H_\text{kin}\Delta\gamma\,\mathbf n$$ and $$p=p_n+\sqrt{2/3}\Delta\gamma$$, with $$\mathbf n=\mathbf\xi/\lVert\mathbf\xi\rVert$$.

!!! info "deviation from theory"
    The multiplier is normalised so that the plastic strain increment equals $$\Delta\gamma$$ times the unit normal.
    The accumulated plastic strain therefore increases by $$\sqrt{2/3}\Delta\gamma$$ rather than by $$\Delta\gamma$$.

The consistent tangent is assembled from the same denominator $$2G+\dfrac{2}{3}(H_\text{iso}+H_\text{kin})$$.
The stored history is the accumulated plastic strain followed by the six back-stress components.

## Syntax

```text title="BilinearJ2"
material BilinearJ2 (1) (2) (3) (4) [5] [6] [7]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, yield stress
# [5] double, hardening ratio, default: 0.0
# [6] double, beta, default: 1.0
# [7] double, density, default: 0.0
```

## Variants

The `NonlocalBilinearJ2` token keeps this bilinear J2 backbone and adds a nonlocal failure variable stored in a seventh material degree of freedom.
The variable grows once the equivalent plastic strain exceeds a threshold and degrades the stress by a scalar factor, giving strain-softening with a regularised length scale.
It requires seven compulsory parameters: the elastic modulus, Poisson's ratio and yield stress as above, then `(5)` plastic strain threshold, `(6)` evolution rate, `(7)` reference length and `(8)` diffusion rate, followed by the optional hardening ratio, beta and density.
The reference length sets the gradient length scale and the diffusion rate controls spatial coupling of the nonlocal field.
It must be used with a nonlocal element such as `NonlocalC3D8`.
A minimal invocation is `material NonlocalBilinearJ2 1 1E4 .2 200 .1 5. 1. 100. .02`.

## Remarks

The elastic modulus and the yield stress are converted to absolute values in the constructor.
The hardening ratio must be smaller than unity because the plastic modulus contains the factor $$1/(1-h)$$.
A negative hardening ratio gives linear softening, and the yield radius is clamped to zero once it becomes negative.
The parameter `beta` is not a Lode-angle parameter here, it only splits the plastic modulus between isotropic and kinematic hardening.
The default `beta=1` reproduces the isotropic-only law of [`BilinearMises1D`](../../Material1D/vonMises/BilinearMises1D.md).
For a general nonlinear hardening curve derive a model from [`NonlinearJ2`](NonlinearJ2.md) or use [`CustomJ2`](CustomJ2.md) instead.
The default hardening ratio of zero gives perfect plasticity, which can localise into a single element layer under softening conditions.
Use a three-dimensional solid element such as `C3D8` with this material.

## References

1. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
