# CustomGurson

Gurson Model With Custom Hardening

## Theory

This model is a concrete implementation of the abstract [`NonlinearGurson`](NonlinearGurson.md) porous plasticity family.
It replaces the built-in matrix hardening law by an [Expression](../../../../Collection/Define/expression.md) supplied by the user.
The expression takes the equivalent plastic strain $$\varepsilon_m^p$$ as its only input and returns two values,

$$
\left[\sigma_y\left(\varepsilon_m^p\right),\ \dfrac{\mathrm{d}\sigma_y}{\mathrm{d}\varepsilon_m^p}\right].
$$

Both values enter the coupled return mapping directly, the first in the yield function and the second in the Newton Jacobian.
The yield function, the void growth law, the nucleation law and the consistent tangent are unchanged from [`NonlinearGurson`](NonlinearGurson.md).
This makes the model suitable for fitting an arbitrary matrix curve without modifying the source code.

!!! warning "implementation limitation"
    Initialisation requires exactly one input and exactly two outputs from the expression.
    A single-output expression is rejected even if it could supply the derivative by finite differences.

## Syntax

```text title="CustomGurson"
material CustomGurson (1) (2) (3) (4) [5] [6] [7] [8] [9] [10]
# (1) int, unique material tag
# (2) int, expression tag
# (3) double, elastic modulus
# (4) double, Poisson's ratio
# [5] double, q1, default: 1.0
# [6] double, q2, default: 1.0
# [7] double, fn, default: 0.0
# [8] double, sn, default: 1.0
# [9] double, en, default: 0.0
# [10] double, density, default: 0.0
```

## Remarks

The yield stress evolution can be customized.
The attached expression must return $$\sigma_y(\varepsilon_m^p)$$ and its derivative with respect to $$\varepsilon_m^p$$.
See the [parent](NonlinearGurson.md) page for more details.

Initialisation checks that the expression has one input and two outputs.
The expression must provide analytic derivatives because the Jacobian uses the returned second value rather than a finite-difference approximation.
The expression tag must refer to an expression defined before the material is first used.
There is no initial void fraction parameter, so set `initial_history(1)` with the `initial material history` command when needed.
The uniaxial counterpart is [`CustomGurson1D`](../../Material1D/vonMises/CustomGurson1D.md).
For a tabulated law use [`TableGurson`](TableGurson.md), and for the built-in implicit law use [`ExpGurson`](ExpGurson.md).

## References

1. A. L. Gurson, Continuum theory of ductile rupture by void nucleation and growth, Part I: yield criteria and flow rules for porous ductile media, *Journal of Engineering Materials and Technology* 99 (1977) 2--15, [doi:10.1115/1.3443401](https://doi.org/10.1115/1.3443401).
2. V. Tvergaard and A. Needleman, Analysis of the cup-cone fracture in a round tensile bar, *Acta Metallurgica* 32 (1984) 157--169, [doi:10.1016/0001-6160(84)90213-X](https://doi.org/10.1016/0001-6160(84)90213-X).
