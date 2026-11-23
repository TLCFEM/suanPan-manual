# Tanh1D

Uniaxial Elastic Material Using $$\tanh$$

## Syntax

```text title="Tanh1D"
material Elastic1D (1) (2) [3]
# (1) int, unique material tag
# (2) double, elastic modulus
# [3] double, density, default: 0.0
```

## Theory

The constitutive equation is defined as

$$
\sigma=E\tanh(\epsilon),
$$

where $$E$$ is the elastic modulus and $$\epsilon$$ is the strain.

The tangent stiffness is the derivative of the backbone,

$$
E_T=\frac{\mathrm{d}\sigma}{\mathrm{d}\varepsilon}=E\,\mathrm{sech}^2(\varepsilon)=\frac{E}{\cosh^2(\varepsilon)}.
$$

Since $$\cosh(\varepsilon)\ge 1$$, the tangent stiffness decreases from $$E$$ at zero strain towards zero at large strain.
The backbone is odd and saturates at $$\pm E$$, providing a smooth and bounded alternative to a perfectly plastic plateau.

## Remarks

The keyword in a command is `Tanh1D`; the `material Elastic1D` line in the syntax block is a typographical error.
The elastic modulus `(2)` sets both the initial tangent stiffness and the saturation stress, and it is used as given.
The density `(3)` defaults to zero.
Because a single parameter fixes both the initial slope and the plateau, the transition strain is of order unity and cannot be adjusted independently.

!!! warning "implementation limitation"
    The law has no separate yield or transition strain parameter, unlike a regularised elastoplastic plateau.
    A common tanh-based fit with $$\sigma=\sigma_s\tanh(\varepsilon/\varepsilon_0)$$ cannot be reproduced unless $$\sigma_s=E$$ and $$\varepsilon_0=1$$ are acceptable.
    A negative modulus input gives a negative tangent.

!!! note "developer note"
    The modulus is stored without `fabs`.

Use [`CustomElastic1D`](CustomElastic1D.md) if the saturation stress and the initial slope must be specified separately.
For a stiffening backbone use [`Sinh1D`](Sinh1D.md).
