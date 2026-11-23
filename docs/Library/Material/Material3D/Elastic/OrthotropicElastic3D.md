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

The three Young's moduli $$E_1,E_2,E_3$$, the three shear moduli $$G_{12},G_{23},G_{13}$$ and the three independent Poisson's ratios $$\nu_{12},\nu_{23},\nu_{13}$$ are the nine independent constants of linear orthotropic elasticity.
The complementary ratios follow from reciprocity as $$\nu_{ji}=\nu_{ij}E_j/E_i$$ for $$i\neq j$$, so only three Poisson's ratios need to be supplied.
In the Voigt ordering $$(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{12},\gamma_{23},\gamma_{13})$$ the stiffness matrix has the form

$$
\mathbf D=\begin{bmatrix}\mathbf C&0\\0&\operatorname{diag}(G_{12},G_{23},G_{13})\end{bmatrix},
\qquad \mathbf C=\begin{bmatrix}1/E_1&-\nu_{12}/E_1&-\nu_{13}/E_1\\-\nu_{12}/E_1&1/E_2&-\nu_{23}/E_2\\-\nu_{13}/E_1&-\nu_{23}/E_2&1/E_3\end{bmatrix}^{-1}.
$$

The implementation inverts the $$3\times3$$ compliance block numerically and writes the shear moduli into the last three diagonal entries.
Positive definiteness requires positive moduli together with $$|\nu_{12}|<\sqrt{E_1/E_2}$$, $$|\nu_{23}|<\sqrt{E_2/E_3}$$, $$|\nu_{13}|<\sqrt{E_1/E_3}$$ and

$$
1-\nu_{12}\nu_{21}-\nu_{23}\nu_{32}-\nu_{13}\nu_{31}-2\nu_{12}\nu_{23}\nu_{31}>0.
$$

## Remarks

The ordering follows the standard notation (11, 22, 33, 12, 23, 13), so the three shear moduli satisfy $$G_{ij}=G_{ji}$$ while the Poisson's ratios satisfy $$\nu_{ij}\neq\nu_{ji}$$.
The compliance matrix must be positive definite for a physically admissible response.
For direction-independent stiffness use [`IsotropicElastic3D`](IsotropicElastic3D.md); the material axes can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.

The six moduli are read in the order $$E_1,E_2,E_3,G_{12},G_{23},G_{13}$$ and the three Poisson's ratios in the order $$\nu_{12},\nu_{23},\nu_{13}$$.
The shear ordering follows the element Voigt convention $$(\gamma_{12},\gamma_{23},\gamma_{13})$$, so the labels $$G_{xy},G_{yz},G_{zx}$$ in the syntax block denote $$G_{12},G_{23},G_{13}$$.
Unlike [`IsotropicElastic3D`](IsotropicElastic3D.md), the constructor does not take absolute values, so negative or zero inputs are not corrected and can produce a non-positive-definite stiffness.

!!! warning "implementation limitation"
    The elastic constants are not validated.
    A singular compliance matrix or inconsistent Poisson ratios therefore produce a non-physical stiffness without a diagnostic.

Setting all $$E_i=E$$, all $$G_{ij}=E/[2(1+\nu)]$$ and all $$\nu_{ij}=\nu$$ recovers isotropic elasticity.
Any 3D solid element that passes a six-component strain vector can use this model, for example [`C3D8`](../../../Element/Cube/C3D8.md).

## Example

```text
material OrthotropicElastic3D 1 1.2E5 1E4 1E4 7E3 3.5E3 7E3 0.3 0.4 0.3
```

## References

1. [ISBN 978-1-56032-712-7](https://search.worldcat.org/search?q=bn:9781560327127)
2. [ISBN 978-0-8493-1592-3](https://search.worldcat.org/search?q=bn:9780849315923)
