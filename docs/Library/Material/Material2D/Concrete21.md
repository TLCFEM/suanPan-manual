# Concrete21

The `Concrete21` material model implements the smeared rotating crack model for concrete.
In general, it takes the in-plane strain vector as the input, converts it into principal strains and calls uniaxial material models to compute uniaxial stress and stiffness response.
These are rotated back to the nominal direction using the same eigenvectors.

The underlying uniaxial concrete model used is the [`ConcreteTsai`](../Material1D/Concrete/ConcreteTsai.md) model.

## Background

Smeared crack models replace discrete cracks by a continuous degradation of the material over a finite element.
In the rotating crack formulation the crack normals are not fixed in the material but follow the current principal strain directions, so that no shear stress is generated on a rotating crack surface.
The two-dimensional implementation assumes coaxial strain and stress tensors, which makes it possible to represent the in-plane response by two independent uniaxial constitutive laws written in the principal strain space.
Poisson coupling between the principal directions is deliberately omitted, so the initial in-plane stiffness is diagonal with entries $E$ and $E/2$ rather than a plane-stress or plane-strain isotropic tensor.

!!! info "deviation from theory"
    Isotropic concrete would have an initial plane-stress stiffness with off-diagonal terms $\nu E/(1-\nu^2)$ and shear modulus $E/[2(1+\nu)]$.
    This model instead uses independent principal springs with no Poisson ratio, so biaxial confinement and lateral expansion are not represented.

This is a plane-stress-type material with `PlaneType::N`, and it is intended for reinforced concrete membrane elements under monotonic or reversed in-plane loading.

## References

1. Crisfield, M. A. and Wills, J. (1989), "Analysis of R/C Panels Using Different Concrete Models", Journal of Engineering Mechanics, 115(3), 578--597, [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578)).
2. Jirásek, M. and Zimmermann, T. (1998), "Rotating Crack Model with Transition to Scalar Damage", Journal of Engineering Mechanics, 124(3), 277--284, [10.1061/(ASCE)0733-9399(1998)124:3(277)](https://doi.org/10.1061/(ASCE)0733-9399(1998)124:3(277)).
3. Chen, W. F. and Han, D. J. (2007), "Plasticity for Structural Engineers", J. Ross Publishing, ISBN 978-1-932159-75-2, Chapter 7.

## Syntax

```text title="Concrete21"
material Concrete21 (1) (2) (3) (4) (5) (6) (7) (8) (9) [10]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, compression strength, should be negative but sign insensitive
# (4) double, tension strength, should be positive but sign insensitive
# (5) double, NC
# (6) double, NT
# (7) double, middle point
# (8) double, strain at compression strength
# (9) double, strain at tension strength
# [10] double, density, default: 0.0
```

## Theory

The formulation can be interpreted via two approaches.
One in pure mathematics style and the other from engineering perspective.
Fundamentally, the stress response is an isotropic tensor function of in-plane strain tensor.
One can refer to [10.1002/cnm.1640091105](https://doi.org/10.1002/cnm.1640091105) for a more general derivation of stiffness, which eventually gives the same expression as shown in [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578)).

Let $$\varepsilon$$ and $$\sigma$$ be coaxial in-plane strain and stress tensor.
Performing eigen decomposition gives two eigenvalues and eigenvectors.

$$
\varepsilon=\sum_{i=1}^2\hat\varepsilon_in_i\otimes{}n_i,\\ \sigma=\sum_{i=1}^2\hat\sigma_in_i\otimes{}n_i.
$$

Here $$\hat\varepsilon_i$$ and $$\hat\sigma_i$$ are principal strain and stress that are related to each other via uniaxial material model, viz., $$\hat\sigma_i=f(\hat\varepsilon_i)$$.

Given that the Poisson's effect is not considered, the in-plane stiffness can be expressed as

$$
K=\sum_
{i=1}^2\dfrac{\mathrm{d}\hat\sigma_i}{\mathrm{d}\hat\varepsilon_i}n_i\otimes{}n_i\otimes{}n_i\otimes{}n_i+\dfrac{1}{2}\dfrac{\hat\sigma_1-\hat\sigma_2}{\hat\varepsilon_1-\hat\varepsilon_2}(
n_1\otimes{}n_2+n_2\otimes{}n_1)\otimes(n_1\otimes{}n_2+n_2\otimes{}n_1).
$$

If one arranges second order tensors $$n_i\otimes{}n_j$$ into Voigt form, then we define the transformation matrix

$$
T_{3\times3}=\begin{bmatrix}n_1\otimes{}n_1&n_2\otimes{}n_2&n_1\otimes{}n_2+n_2\otimes{}n_1\end{bmatrix},
$$

then

$$
K=T\hat{K}T^\mathrm{T},
$$

where

$$
\hat{K}=\begin{bmatrix}\dfrac{\mathrm{d}\hat\sigma_1}{\mathrm{d}\hat\varepsilon_1}&&\\&\dfrac{\mathrm{d}\hat\sigma_2}{\mathrm{d}\hat\varepsilon_2}&\\&&\dfrac{1}{2}\dfrac{\hat\sigma_1-\hat\sigma_2}{\hat\varepsilon_1-\hat\varepsilon_2}\end{bmatrix},
$$

which is identical to the expression shown in [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578)).

### Implementation in `Concrete21`

The source builds two instances of [`ConcreteTsai`](../Material1D/Concrete/ConcreteTsai.md) with identical parameters and drives them with the two principal strains of the current total strain vector.
The crack orientation is recomputed from the current strain at every trial update, so the axes rotate with the strain field.
The principal stresses are rotated back with the same transformation matrix, giving $\boldsymbol\sigma=\mathbf T^{\mathrm T}\hat{\boldsymbol\sigma}$ and $\mathbf K=\mathbf T^{\mathrm T}\hat{\mathbf K}\mathbf T$.
The shear entry of $\hat{\mathbf K}$ is the secant $\tfrac12(\hat\sigma_1-\hat\sigma_2)/(\hat\varepsilon_1-\hat\varepsilon_2)$, with a fallback to the initial shear modulus $E/2$ when the two principal strains coincide or the expression is not finite.

!!! warning "implementation limitation"
    The shear term is a secant between the two principal responses and is not the exact derivative of the rotated stress update when the principal axes move.
    The fallback to $E/2$ at equal principal strains shows that this entry is a regularised approximation rather than a consistent tangent.

Because the two uniaxial laws carry their own loading and unloading history, the rotating crack model reproduces hysteretic behaviour under load reversal without any additional two-dimensional hardening rule.

## Remarks

* `(2)` is the elastic modulus, `(3)` is the compressive strength and `(4)` is the tensile strength, all of which are converted to absolute values by the underlying uniaxial model.
* `(5)` `NC` and `(6)` `NT` are the Tsai backbone exponents for compression and tension, both clipped to at least one, where larger values give a more sharply peaked response.
* `(7)` is the middle point that sets the strain at which the unloading branch reverses, `(8)` is the strain at compressive peak and `(9)` is the strain at tensile peak.
* There is no Poisson's ratio argument, so the initial normal stiffness is $E$ in each principal direction and the initial shear stiffness is $E/2$.
* The model is tagged `PlaneType::N`, so `HIST` and `YF` are the only standard outputs available from [Material2D](Material2D.md); combine it with [`Rebar2D`](Rebar2D.md) through the [`Laminated`](../Wrapper/Laminated.md) wrapper for reinforced concrete panels.
* Strain softening in the uniaxial backbones localises into a single element layer without fracture-energy regularisation, so results depend on mesh size.
* For a fixed crack orientation with post-cracking shear transfer use [`Concrete22`](Concrete22.md); for scalar damage coupled to an arbitrary 3D law use [`IsotropicDamage`](../Material3D/Damage/IsotropicDamage.md).
