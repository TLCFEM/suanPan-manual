# Concrete21

The `Concrete21` material model implements the smeared rotating crack model for concrete. In general, it takes in-plane
strain vector as the input, converts it into principal strains and calls uniaxial material models to compute uniaxial
stress and stiffness response. These ae rotated back to the nominal direction using the same eigen vectors.

The underlying uniaxial concrete model used is the [`ConcreteTsai`](../Material1D/Concrete/ConcreteTsai.md) model.

## References

1. [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578))

## Syntax

```
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

The formulation can be interpreted via two approaches. One in pure mathematics style and the other from engineering
perspective. Fundamentally, the stress response is an isotropic tensor function of in-plane strain tensor. One can refer
to [10.1002/cnm.1640091105](https://doi.org/10.1002/cnm.1640091105) for a more general derivation of stiffness, which
eventually gives the same expression as shown
in [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578)).

Let $$\varepsilon$$ and $$\sigma$$ be coaxial in-plane strain and stress tensor. Performing eigen decomposition gives
two eigenvalues and eigenvectors.

$$
\varepsilon=\sum_{i=1}^2\hat\varepsilon_in_i\otimes{}n_i,\\ \sigma=\sum_{i=1}^2\hat\sigma_in_i\otimes{}n_i.
$$

In which $$\hat\varepsilon_i$$ and $$\hat\sigma_i$$ are principal strain and stress that are related to each other via
uniaxial material model, viz., $$\hat\sigma_i=f(\hat\varepsilon_i)$$.

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

which is identical to the expression shown
in [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578)).
