# BlatzKo

Blatz-Ko Hyperelastic Material

The Blatz-Ko material can be used to simulate foam rubber.

## Background

Finite-strain isotropic hyperelasticity defines a strain energy density $W$ per unit reference volume as a function of the invariants of the right Cauchy-Green tensor $\mathbf C=\mathbf F^\mathrm T\mathbf F$.
Here $I_1=\mathrm{tr}(\mathbf C)$ and $I_3=\det\mathbf C=J^2$, with $J$ the volume ratio.
The second Piola-Kirchhoff stress is $\mathbf S=2\partial W/\partial\mathbf C$.

The implementation uses the compressible potential

$$
W=\dfrac{\mu}{2}\left[I_1-3+\dfrac{1}{\beta}\left(I_3^{-\beta}-1\right)\right],\qquad
\mu=\dfrac{E}{2(1+\nu)},\qquad
\beta=\dfrac{\nu}{1-2\nu}.
$$

Here $E$ and $\nu$ are the small-strain Young's modulus and Poisson's ratio.
The code stores $\mu$ and $\tfrac12(1+\beta)$ and evaluates the stress as

$$
\mathbf S=\mu\left(\mathbf I-I_3^{-(1+\beta)}\operatorname{cof}\mathbf C\right)
=\mu\left(\mathbf I-I_3^{-\beta}\mathbf C^{-1}\right).
$$

The cofactor is assembled directly from the six Green-strain entries supplied by the element, and the consistent tangent is obtained by differentiating this expression.
This potential is the compressible Storakers/Ogden hyperfoam form with exponent $\alpha=2$.
It is related to the classic Blatz-Ko foam potential $\tfrac{\mu}{2}(I_2/I_3+2\sqrt{I_3}-5)$, which is the $\alpha=-2$ member with $\nu=0.25$.
The small-strain bulk modulus inherited from $E$ and $\nu$ is $K=E/[3(1-2\nu)]$.

!!! info "deviation from theory"
    The implementation uses the $\alpha=2$ compressible hyperfoam potential rather than the classic $\alpha=-2$ Blatz-Ko energy $I_2/I_3+2\sqrt{I_3}-5$.
    The two forms give different stress predictions for a general deformation.

## References

1. [10.1016/0045-7949(86)90199-9](https://doi.org/10.1016/0045-7949(86)90199-9)
2. [10.1122/1.548937](https://doi.org/10.1122/1.548937)
3. R. W. Ogden, *Non-linear Elastic Deformations*, Dover, 1997, Chapter 7.

## Syntax

```text title="BlatzKo"
material BlatzKo (1) (2) (3) [4]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# [4] double, density, default: 0.0
```

## Remarks

Both `(2)` and `(3)` are replaced by their absolute values, so only positive $E$ and $\nu$ can be entered.
The model targets compressible foam rubber with moderate Poisson's ratio, and values approaching $0.5$ make $\beta$ large and stiffen the volumetric response sharply.

!!! warning "implementation limitation"
    The constructor applies `fabs` to both inputs, so negative Poisson's ratios cannot be modelled.
    A value of `nu` equal to `0.5` is not rejected and makes the exponent singular.

The material takes the Green-Lagrange strain as input, so the nonlinear geometry switch must be enabled in the host element.
The third invariant is floored at machine epsilon to prevent a singularity at $J=0$.

!!! warning "implementation limitation"
    Flooring $I_3$ at machine epsilon modifies the potential near vanishing volume ratio.
    The exact hyperelastic response is therefore not recovered as $J$ approaches zero.

The tangent stiffness is re-evaluated at every step from the current deformation, unlike the constant stiffness of [`IsotropicElastic3D`](IsotropicElastic3D.md).
For nearly incompressible rubber prefer [`MooneyRivlin`](MooneyRivlin.md) or [`Yeoh`](Yeoh.md).
