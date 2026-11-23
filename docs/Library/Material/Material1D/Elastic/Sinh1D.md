# Sinh1D

Uniaxial Elastic Material Using $$\sinh$$

## Syntax

```text title="Sinh1D"
material Elastic1D (1) (2) [3]
# (1) int, unique material tag
# (2) double, elastic modulus
# [3] double, density, default: 0.0
```

## Theory

The constitutive equation is defined as

$$
\sigma=E\sinh(\epsilon),
$$

where $$E$$ is the elastic modulus and $$\epsilon$$ is the strain.

The tangent stiffness is the derivative of the backbone,

$$
E_T=\frac{\mathrm{d}\sigma}{\mathrm{d}\varepsilon}=E\cosh(\varepsilon).
$$

Since $$\cosh(\varepsilon)\ge 1$$, the tangent stiffness is always at least $$E$$ and grows without bound as $$|\varepsilon|$$ increases.
The backbone is odd, path independent and has no saturation stress, so it represents progressive stiffening rather than yielding.

## Remarks

The keyword in a command is `Sinh1D`; the `material Elastic1D` line in the syntax block is a typographical error.
The elastic modulus `(2)` is the initial tangent stiffness at zero strain and is used as given.

!!! warning "implementation limitation"
    The constructor stores the modulus without applying `fabs`.
    A negative input gives a negative initial tangent and a backbone that stiffens in the negative direction.

The density `(3)` defaults to zero.
The exponential growth of the backbone can produce very large stresses at moderate strains, which may cause convergence problems or numerical overflow.
For a saturating backbone use [`Tanh1D`](Tanh1D.md), and for a fitted polynomial use [`PolyElastic1D`](PolyElastic1D.md).
