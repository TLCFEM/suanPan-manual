# QE2

Mixed Four-Node Quadrilateral Element

* Number of Nodes: 4
* Number of DoFs: 2
* DoF Label: U1, U2
* Supports Body Force
* Integration Scheme: 2nd Order Gauss
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Background

[`QE2`](QE2.md) is Piltner's four-node mixed quadrilateral with two enhanced strain modes.
It is derived from a Hu-Washizu functional in which displacement, strain and stress are interpolated independently.
The stress field uses seven modes assembled from the mapped polynomial vector $$[0,\xi,\eta,\xi\eta]$$ and the seven-term stress interpolation $$\mathbf P$$.
The compatible strain is $$\mathbf\varepsilon_c=\mathbf B\mathbf a$$, and two enhanced strain modes $$\mathbf\varepsilon_e=\mathbf B_I\mathbf\lambda$$ are added, so $$\mathbf\varepsilon=\mathbf B\mathbf a+\mathbf B_I\mathbf\lambda$$.
The independent strain parameters $$\mathbf\alpha$$ and stress parameters $$\mathbf\beta$$ are related through the compliance matrix $$\mathbf A=\mathbf D^{-1}\mathbf P$$.
The discrete equations contain the arrays
$$
\mathbf H=\sum_q\mathbf P_q^\mathrm T\mathbf A_qw_q,\quad \mathbf L=\sum_q\mathbf P_q^\mathrm T\mathbf B_qw_q,\quad \mathbf L_I=\sum_q\mathbf P_q^\mathrm T\mathbf B_{Iq}w_q.
$$
The local unknowns are eliminated by static condensation.
Since $$\mathbf H$$ is symmetric, the condensed stiffness assembled in the code is
$$
\mathbf K^e=\mathbf L^\mathrm T\mathbf H^{-1}\mathbf L-\left(\mathbf L_I^\mathrm T\mathbf H^{-1}\mathbf L\right)^\mathrm T\left(\mathbf L_I^\mathrm T\mathbf H^{-1}\mathbf L_I\right)^{-1}\left(\mathbf L_I^\mathrm T\mathbf H^{-1}\mathbf L\right).
$$
The condensation matrices $$\mathbf L$$, $$\mathbf L_I$$, $$\mathbf H$$ and their inverses are formed once at initialisation from the initial material tangent.
The local stiffness is refreshed from the current trial tangent at every iteration and the reduced matrices are recomputed from it, so the element remains usable with nonlinear materials.
The enhanced modes relieve shear locking and reduce sensitivity to element distortion compared with the bilinear [`CP4`](../Plane/CP4.md).

!!! info "deviation from theory"
    Unlike a fully nonlinear Hu-Washizu element, the enhancement basis does not follow the evolving material stiffness.

!!! note "developer note"
    A fully nonlinear Hu-Washizu element would recompute the compatibility matrix from the current tangent at every iteration.
    Here the condensation matrices are frozen at the initial elastic tangent.

## References

1. [10.1002/nme.1620381102](https://doi.org/10.1002/nme.1620381102)
2. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)

## Syntax

```text title="QE2"
element QE2 (1) (2...5) (6) [7]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```

## Remarks

* The element stores the seven stress parameters, the seven strain parameters and the two enhanced-strain multipliers as history variables.
* The thickness argument is ignored when the material declares plane strain.
* Four Gauss points are used, and the characteristic length is $$\sqrt{A}$$ with $$A$$ the element area.
* Initialization fails if the $$7\times7$$ compatibility matrix is singular, which can happen for severely distorted elements.
* Stress and strain recording returns the mixed fields rather than the raw material response, with the seven components remapped to the Voigt layout.
* [`PS`](PS.md) is cheaper because it has no enhanced strain, while [`CP4I`](../Plane/CP4I.md) uses incompatible modes instead of an assumed stress.
