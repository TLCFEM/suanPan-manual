# NLE1D01

Nonlinear Elastic 1D Type 01

The `NLE1D01` material is a smoothed uniaxial bilinear elastic material model which uses the MP formula to approximate the bilinear backbone.
The name `MP` refers to the Menegotto--Pinto transition function.
Internally `NLE1D01` instantiates [`BilinearElastic1D`](BilinearElastic1D.md) with a nonzero transition radius.

!!! info "deviation from theory"
    Only the monotonic first-loading branch of the Menegotto--Pinto equation is used.
    The curvature parameter $R$ is the constant supplied as `(5)`, with no reversal detection, no evolution of $R$, no Bauschinger effect and no isotropic hardening.
    The model is therefore an elastic backbone, not the cyclic hysteretic model from which the transition formula originates.

## Theory

Let $$E$$ be the elastic modulus, $$\sigma_y$$ the yield stress, $$\varepsilon_y=\sigma_y/E$$ the yield strain and $$b=H/E$$ the hardening ratio.
With the normalized strain $$n=\max(\epsilon_0,|\varepsilon|/\varepsilon_y)$$, where $$\epsilon_0$$ is a small positive floor, and transition radius $$R>0$$, the implementation defines

$$
a=1+n^R,\qquad c=(1-b)\,a^{-1/R},
$$

$$
\sigma=\operatorname{sign}(\varepsilon)\,|\varepsilon|\left[bE+(1-b)E\left(1+\left(\frac{|\varepsilon|}{\varepsilon_y}\right)^R\right)^{-1/R}\right],
$$

and the consistent tangent stiffness

$$
E_T=bE+\frac{Ec}{a}=H+(E-H)\left(1+\left(\frac{|\varepsilon|}{\varepsilon_y}\right)^R\right)^{-1/R-1}.
$$

As $$|\varepsilon|\to 0$$ the tangent tends to $$E$$, and as $$|\varepsilon|\to\infty$$ the backbone tends to the bilinear asymptote $$\operatorname{sign}(\varepsilon)\big[\sigma_y+H\big(|\varepsilon|-\varepsilon_y\big)\big]$$.
Larger values of $$R$$ give a sharper transition and recover the sharp-corner [`BilinearElastic1D`](BilinearElastic1D.md) backbone in the limit.
The response remains path independent and symmetric in tension and compression, so no hysteresis is introduced.

## Syntax

```text title="NLE1D01"
material NLE1D01 (1) (2) (3) (4) (5) [6]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, turning stress
# (4) double, hardening ratio
# (5) double, radius of transition
# [6] double, density, default: 0
```

## Example

```
material NLE1D01 1 2E5 400 .01 10
```

## Remarks

The argument `(3)` is the yield stress magnitude and `(4)` is the hardening ratio, consistent with [`BilinearElastic1D`](BilinearElastic1D.md).
The radius `(5)` is the Menegotto--Pinto shape exponent and is dimensionless; it must be positive, with larger values giving a sharper knee.
Typical values in steel cyclic models lie between 3 and 20, but this monotonic model has no hysteresis and no cyclic degradation of the radius.
The constructor uses absolute values for the elastic modulus and yield stress, so their signs do not matter.
The density `(6)` defaults to zero.
Use the sharp-corner [`BilinearElastic1D`](BilinearElastic1D.md) when a distinct yield point is required, and [`MultilinearElastic1D`](MultilinearElastic1D.md) for an arbitrary number of segments.

## References

1. Method of analysis for cyclically loaded reinforced concrete plane frames including changes in geometry and non-elastic behaviour of elements under combined normal force and bending
