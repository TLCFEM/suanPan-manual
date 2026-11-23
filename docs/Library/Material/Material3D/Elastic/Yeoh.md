# Yeoh

Regularized Yeoh Material For Compressible Rubbers

The following strain energy density is used.

$$
W=\sum_{i=1}^nC_{i0}(J_1-3)^i+\sum_{i=1}^nC_{i1}(J_3-1)^{2i}.
$$

where $$C_{i0}$$ and $$C_{i1}$$ are material constants.
$$J_1$$ and $$J_3$$ are reduced invariants of the right Cauchy-Green deformation tensor.

## Background

With $\mathbf C=\mathbf F^\mathrm T\mathbf F$, $I_1=\mathrm{tr}\,\mathbf C$ and $J=\sqrt{\det\mathbf C}$, the arguments of the energy are $J_1=I_1J^{-2/3}$ and $J_3=J$.
Using the reduced invariant $J_1$ separates the distortional response from the volumetric response of an isotropic material.
The first sum is the reduced-polynomial form introduced by Yeoh and the second sum is a volumetric penalty built from even powers of $J-1$.

!!! info "deviation from theory"
    The original Yeoh model is formulated for incompressible rubber and contains only powers of $I_1-3$.
    This implementation uses the reduced invariant $J_1$ and adds a volumetric series in $J-1$, so it is a regularised compressible variant.

At small strain the initial shear modulus is $\mu_0=2C_{10}$ and the initial bulk modulus is $K_0=2C_{11}$.
A negative $C_{20}$ followed by a positive $C_{30}$ reproduces the softening at small strain and the stiffening at large strain observed in filled rubber.
The second Piola-Kirchhoff stress and the consistent tangent are obtained by differentiating the energy with respect to the Green strain.

## Syntax

```text title="Yeoh"
material Yeoh (1) (2...)
# (1) int, unique material tag
# (2...) double, material constants with possible density
```

## Remarks

1. The above command takes input list of arbitrary length ($$\ge2$$, excluding tag).
2. If the number of double inputs is odd, the last one is interpreted as density.
3. If the number of double inputs is even, the density is assumed to be zero.
4. The first half of double inputs is read as $$C_{i0}$$ and the second half as $$C_{i1}$$.

!!! warning "implementation limitation"
    The parser splits the coefficient list into two equal halves.
    The deviatoric and volumetric series must therefore have the same number of terms.

5. The coefficients are not converted to absolute values, so the sign of $C_{20}$ and $C_{30}$ is meaningful.
6. The model takes the Green-Lagrange strain in Voigt notation and requires nonlinear geometry in the host element.
7. The third invariant is floored at machine epsilon to avoid a singularity when the volume ratio vanishes.

!!! warning "implementation limitation"
    Flooring $I_3$ at machine epsilon modifies the volumetric penalty as $J$ approaches zero.
    The exact strain energy is not recovered near vanishing volume ratio.

8. For a two-parameter deviatoric response with a single volumetric term use [`MooneyRivlin`](MooneyRivlin.md), and for compressible foam use [`BlatzKo`](BlatzKo.md).

## Examples

For $$i=1$$, let $$C_{10}=20$$ and $$C_{11}=4000$$, the strain energy density is

$$
W=20(J_1-3)+4000(J_3-1)^2.
$$

The following command shall be used.

```
material Yeoh 1 20 4000
```

If density is nonzero, say for example $$\rho=10^{-4}$$, then the following command shall be used.

```
material Yeoh 1 20 4000 1E-4
```

For $$i=3$$, let $$C_{10}=20$$, $$C_{20}=30$$, $$C_{30}=40$$, $$C_{11}=2000$$, $$C_{21}=3000$$ and $$C_{31}=4000$$, the strain energy density is

$$
W=20(J_1-3)+30(J_1-3)^2+40(J_1-3)^3+2000(J_3-1)^2+3000(J_3-1)^4+4000(J_3-1)^6.
$$

The following command shall be used.

```
material Yeoh 1 20 30 40 2000 3000 4000
```

## References

1. O. H. Yeoh, *Characterization of Elastic Properties of Carbon-Black-Filled Rubber Vulcanizates*, Rubber Chemistry and Technology, 63(5):792–805, 1990, [10.5254/1.3538289](https://doi.org/10.5254/1.3538289).
2. O. H. Yeoh, *Some Forms of the Strain Energy Function for Rubber*, Rubber Chemistry and Technology, 66(5):754–771, 1993, [10.5254/1.3538343](https://doi.org/10.5254/1.3538343).
