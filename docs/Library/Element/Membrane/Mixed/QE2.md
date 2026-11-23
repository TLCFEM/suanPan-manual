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
The stress field uses seven modes assembled from the mapped polynomial vector $[0,\xi,\eta,\xi\eta]$ and the seven-term stress interpolation $\boldsymbol P$.
The compatible strain is $\boldsymbol\varepsilon_c=\boldsymbol B\boldsymbol a$, and two enhanced strain modes $\boldsymbol\varepsilon_e=\boldsymbol B_I\boldsymbol\lambda$ are added, so $\boldsymbol\varepsilon=\boldsymbol B\boldsymbol a+\boldsymbol B_I\boldsymbol\lambda$.
The independent strain parameters $\boldsymbol\alpha$ and stress parameters $\boldsymbol\beta$ are related through the compliance matrix $\boldsymbol A=\boldsymbol D^{-1}\boldsymbol P$.
The discrete equations contain the arrays
$$
\boldsymbol H=\sum_q\boldsymbol P_q^\mathrm T\boldsymbol A_qw_q,\quad \boldsymbol L=\sum_q\boldsymbol P_q^\mathrm T\boldsymbol B_qw_q,\quad \boldsymbol L_I=\sum_q\boldsymbol P_q^\mathrm T\boldsymbol B_{Iq}w_q.
$$
The local unknowns are eliminated by static condensation.
Since $\boldsymbol H$ is symmetric, the condensed stiffness assembled in the code is
$$
\boldsymbol K^e=\boldsymbol L^\mathrm T\boldsymbol H^{-1}\boldsymbol L-\left(\boldsymbol L_I^\mathrm T\boldsymbol H^{-1}\boldsymbol L\right)^\mathrm T\left(\boldsymbol L_I^\mathrm T\boldsymbol H^{-1}\boldsymbol L_I\right)^{-1}\left(\boldsymbol L_I^\mathrm T\boldsymbol H^{-1}\boldsymbol L\right).
$$
The condensation matrices $\boldsymbol L$, $\boldsymbol L_I$, $\boldsymbol H$ and their inverses are formed once at initialisation from the initial material tangent.
The local stiffness is refreshed from the current trial tangent at every iteration and the reduced matrices are recomputed from it, so the element remains usable with nonlinear materials.
The enhanced modes relieve shear locking and reduce sensitivity to element distortion compared with the bilinear [`CP4`](../Plane/CP4.md).

!!! info "deviation from theory"
    A fully nonlinear Hu-Washizu element would recompute the compatibility matrix from the current tangent at every iteration.
    Here the condensation matrices are frozen at the initial elastic tangent, so the enhancement basis does not follow the evolving material stiffness.

## References

1. R. Piltner and R. L. Taylor, *A quadrilateral mixed finite element with two enhanced strain modes*, International Journal for Numerical Methods in Engineering 38(11), 1783-1808 (1995), [doi:10.1002/nme.1620381102](https://doi.org/10.1002/nme.1620381102).
2. J. C. Simo and T. J. R. Hughes, *Computational Inelasticity*, Springer (1998), Chapter 9.

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
* Four Gauss points are used, and the characteristic length is $\sqrt{A}$ with $A$ the element area.
* Initialization fails if the $7\times7$ compatibility matrix is singular, which can happen for severely distorted elements.
* Stress and strain recording returns the mixed fields rather than the raw material response, with the seven components remapped to the Voigt layout.
* [`PS`](PS.md) is cheaper because it has no enhanced strain, while [`CP4I`](../Plane/CP4I.md) uses incompatible modes instead of an assumed stress.
