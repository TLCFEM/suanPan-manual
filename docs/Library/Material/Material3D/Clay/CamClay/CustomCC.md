# CustomCC

Modified Cam-Clay Model With Custom Hardening

The `CustomCC` token subclasses [`NonlinearCamClay`](NonlinearCamClay.md) and supplies the hardening function $$a(\alpha)$$ and its derivative from a user-defined scalar [Expression](../../../../../Collection/Define/expression.md).
It is useful when the hardening law of a built-in variant such as [`BilinearCC`](BilinearCC.md) is too restrictive.

## Theory

The yield surface and associative flow rule are those of [`NonlinearCamClay`](NonlinearCamClay.md),

$$
F(\sigma,a)=\dfrac{(p-p_t+a)^2}{b^2}+\dfrac{q^2}{M^2}-a^2 .
$$

Here the hardening function $$a$$ and its derivative $$\mathrm{d}a/\mathrm{d}\alpha$$ are evaluated by the assigned expression at the volumetric plastic strain $$\alpha$$.
Any smooth hardening or softening law can therefore be used, as long as it can be differentiated.
Because the hardening function is supplied to [`NonlinearCamClay`](NonlinearCamClay.md), the constant elastic predictor, the tension-positive mean stress, the associative flow rule and the two-equation return mapping are all inherited unchanged.

!!! info "deviation from theory"
    The hardening derivative is obtained numerically rather than analytically, so very steep hardening laws or sharp transitions can give an inaccurate consistent tangent.

!!! note "developer note"
    The derivative passed to the return mapping comes from `Expression::gradient`, which uses a fixed finite step of $$10^{-4}$$ instead of analytic differentiation.

## Syntax

```text title="CustomCC"
material CustomCC (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, beta, controls compression-side shape
# (5) double, m, slope of CSL
# (6) double, p_t, tensile yield hydrostatic stress
# (7) int, expression tag for a(\alpha)
# [8] double, density, default: 0.0
```

## Remarks

The assigned expression must be univariate: exactly one input and one output.
It must also be able to compute derivatives, since the consistent stiffness uses $$\mathrm{d}a/\mathrm{d}\alpha$$.
The input is the volumetric plastic strain $$\alpha$$, which is negative in compression.
The expression must return a non-negative value of $$a$$ for every strain reached in the analysis, since a negative value would invert the yield surface.
No check is performed on the sign of the returned hardening function, so an unsuitable expression can silently produce a non-physical response.
The initial value is not prescribed independently; it is simply the expression evaluated at $$\alpha=0$$ at the start of the analysis.

!!! warning "implementation limitation"
    Classical Cam-Clay derives hardening from the compression and recompression indices and the void ratio.
    This variant replaces that relation entirely by the user expression and does not enforce monotonic growth in compression.

## Example

```text
expression SimpleScalar 1 x 100+2e5*x

material CustomCC 1 1E6 .4 .8 .8 20. 1
```

This defines the linear hardening law $$a(\alpha)=100+2\times10^5\alpha$$.

## References

1. On the Generalised Stress-Strain Behaviour of 'Wet' Clay
2. [ISBN 978-0-641-94048-4](https://search.worldcat.org/search?q=bn:9780641940484)
