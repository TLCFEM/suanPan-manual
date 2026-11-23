# CustomElastic1D

General Uniaxial Elastic Material Model Using Custom Expression

The `CustomElastic1D` model evaluates a user-defined scalar expression as the constitutive law.
It is the most general member of the elastic family, since the stress and its tangent are taken directly from an [`expression`](../../../../Collection/Define/expression.md) object.

## Background

The model requires a univariate expression $$f$$ that returns a single scalar.
The stress and tangent stiffness are computed as

$$
\sigma=f(\varepsilon),\qquad E_T=\left.\frac{\mathrm{d}f}{\mathrm{d}\varepsilon}\right|_{\varepsilon},
$$

where the derivative is supplied by the `gradient` method of the expression.
The initial stiffness is set to the gradient evaluated at zero strain.
Because the expression is evaluated only from the current strain, the response is path independent provided the expression itself is a pure function.

!!! warning "implementation limitation"
    The tangent stiffness is taken from the `gradient` method of the expression and no finite-difference fallback is provided.
    An expression whose gradient is undefined at zero strain gives an invalid initial stiffness, and a discontinuous gradient prevents quadratic convergence.
    The material stores no history, so an expression with hidden state would violate the assumed path independence.
A user-defined expression can therefore implement any of the built-in backbones, such as those of [`PolyElastic1D`](PolyElastic1D.md) or [`Tanh1D`](Tanh1D.md), as well as custom laws.

## Syntax

```text title="CustomElastic1D"
material CustomElastic1D (1) (2) [3]
# (1) int, unique material tag
# (2) int, associated expression tag
# [3] double, density, default: 0
```

## Example

See [expression](../../../../Collection/Define/expression.md).

## Remarks

The expression tag `(2)` must refer to an already defined expression with one input and one output.
The initial stiffness is taken from the gradient at zero strain, so a non-differentiable expression at the origin produces an undefined initial tangent.
A discontinuous gradient can cause convergence problems in a Newton--Raphson analysis even when the stress is continuous.
The density `(3)` defaults to zero and follows the same convention as [`Elastic1D`](Elastic1D.md).
This wrapper defines a stress--strain law only; to degrade an existing material use [`CustomStrainDegradation`](../Degradation/CustomStrainDegradation.md) or [`CustomStressDegradation`](../Degradation/CustomStressDegradation.md).
