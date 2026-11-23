# ElasticOS

Isotropic Elastic Material For Open Sections

The `ElasticOS` model provides linear elastic resultants for open-section beam elements.

## Background

Open-section beam elements reduce the three-dimensional continuum to a small set of section resultants, typically the axial force and the two transverse shear resultants.
The corresponding material strain vector has three entries, an axial strain and two engineering shear strains, and the constitutive matrix relates them to the conjugate stress resultants.
With $G=E/[2(1+\nu)]$, the source assembles
$$
\mathbf D^{\mathrm{OS}}=\begin{bmatrix}E&0&0\\0&G&0\\0&0&G\end{bmatrix},\qquad \mathbf s^{\mathrm{OS}}=\mathbf D^{\mathrm{OS}}\mathbf e^{\mathrm{OS}}.
$$
This is the diagonal restriction of isotropic elasticity to the axial and two shear modes, with no Poisson coupling and no dependence on the cross-sectional shape.
The [`OS146`](../Wrapper/OS146.md) wrapper shows the corresponding mapping from a 3D material: it extracts components $(0,3,5)$ of the six-component Voigt vector, namely the axial strain and the two shear strains.
No warping degree of freedom is introduced by this material, so restrained warping and torsional warping stresses are not represented.

!!! warning "implementation limitation"
    The response is diagonal, so axial strain produces no transverse stress and shear strain produces no axial stress.
    Open-section effects that require the section geometry, such as warping torsion, shear-centre offsets and restrained warping, are handled by the element or not at all.

## Syntax

```text title="ElasticOS"
material ElasticOS (1) (2) (3) [4]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# [4] double, density, default: 0.0
```

## Remarks

It has two DoFs.
The elastic stiffness can be expressed as

$$
\mathbf{K}=\begin{bmatrix}
E&0\\
0&\dfrac{E}{2(1+\nu)}
\end{bmatrix}
$$

!!! info "deviation from theory"
    The two-by-two matrix above is not the matrix used by the material.
    The material uses a three-by-three diagonal matrix with entries $E$, $G$ and $G$, where $G=E/[2(1+\nu)]$.

* The three strain entries are the axial strain and two engineering shear strains, and the material is used with open-section beam elements that expect this resultant layout.
* The parser takes absolute values of both the elastic modulus and Poisson's ratio, so negative inputs cannot be used to change the sign of the stiffness.
* The stiffness is constant and the material has no history variables, so `trial_stress` is simply the matrix-vector product with `trial_strain`.
* For a nonlinear axial response with the same shear behaviour use [`OS146S`](../Wrapper/OS146S.md), which wraps a one-dimensional material and keeps an independent shear modulus.

## References

1. [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)
