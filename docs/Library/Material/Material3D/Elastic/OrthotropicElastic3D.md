# OrthotropicElastic3D

Orthotropic Elastic Material

The `OrthotropicElastic3D` model implements three-dimensional linear elasticity with three mutually orthogonal planes of material symmetry.

## Syntax

```text title="OrthotropicElastic3D"
material OrthotropicElastic3D (1) (2...7) (8...10) [11]
# (1) int, unique tag
# (2..7) double, six moduli
# (8...10) double, three Poisson's ratios
# [11] double, density, default: 0.0
```

## Background

Hooke's law is written in the material axes using a compliance matrix.
With the nine constants grouped as six moduli followed by three Poisson's ratios, the normal compliance is

$$
\begin{bmatrix}
\varepsilon_{11}\\ \varepsilon_{22}\\ \varepsilon_{33}
\end{bmatrix}=
\begin{bmatrix}
1/E_1 & -\nu_{12}/E_1 & -\nu_{13}/E_1\\
-\nu_{12}/E_1 & 1/E_2 & -\nu_{23}/E_2\\
-\nu_{13}/E_1 & -\nu_{23}/E_2 & 1/E_3
\end{bmatrix}
\begin{bmatrix}
\sigma_{11}\\ \sigma_{22}\\ \sigma_{33}
\end{bmatrix},\qquad
\gamma_{ij}=\tau_{ij}/G_{ij}.
$$

## Remarks

The ordering follows the standard notation (11, 22, 33, 12, 23, 13), so the three shear moduli satisfy $$G_{ij}=G_{ji}$$ while the Poisson's ratios satisfy $$\nu_{ij}\neq\nu_{ji}$$.
The compliance matrix must be positive definite for a physically admissible response.
For direction-independent stiffness use [`IsotropicElastic3D`](IsotropicElastic3D.md); the material axes can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.
