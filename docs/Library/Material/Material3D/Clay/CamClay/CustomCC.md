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

## Example

```text
expression SimpleScalar 1 x 100+2e5*x

material CustomCC 1 1E6 .4 .8 .8 20. 1
```

This defines the linear hardening law $$a(\alpha)=100+2\times10^5\alpha$$.
