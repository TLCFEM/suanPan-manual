# CP4I

Bilinear Incompatible Quadrilateral

* Number of Nodes: 4
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2
* Integration Scheme: 2nd Order Gauss
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Background

[`CP4I`](CP4I.md) is the four-node quadrilateral with incompatible modes, the plane counterpart of the Wilson element and the Q6 family.
The compatible displacement is the bilinear interpolation of [`CP4`](CP4.md), giving the strain-displacement matrix $\boldsymbol B_1$.
Four additional strain modes are added through internal degrees of freedom $\boldsymbol\alpha$ that have no nodal counterpart, giving $\boldsymbol\varepsilon=\boldsymbol B_1\boldsymbol a+\boldsymbol B_2\boldsymbol\alpha$.
The four columns of $\boldsymbol B_2$ are built from the global derivatives of the parent-domain function $f=-(\xi^2+\eta^2)$, obtained as $\nabla f=\boldsymbol J^{-1}[-2\xi,-2\eta]^\mathrm T$.
The first column enhances $\varepsilon_{xx}$ with $\partial f/\partial x$, the second enhances $\gamma_{xy}$ with $\partial f/\partial x$, the third enhances $\gamma_{xy}$ with $\partial f/\partial y$, and the fourth enhances $\varepsilon_{yy}$ with $\partial f/\partial y$.

!!! info "deviation from theory"
    The classical Wilson or Q6 element adds two incompatible displacement modes $(1-\xi^2)$ and $(1-\eta^2)$, whereas this implementation adds four assumed strain modes derived from one quadratic function.
    The element name and the documentation retain the incompatible-mode terminology even though the enhancement enters through the strain interpolation.

The mixed equilibrium equations are
$$
\begin{bmatrix}\boldsymbol K_{aa}&\boldsymbol K_{a\alpha}\\ \boldsymbol K_{\alpha a}&\boldsymbol K_{\alpha\alpha}\end{bmatrix}\begin{bmatrix}\boldsymbol a\\ \boldsymbol\alpha\end{bmatrix}=\begin{bmatrix}\boldsymbol f\\ \boldsymbol 0\end{bmatrix}.
$$
Because $\boldsymbol\alpha$ has no external load, it can be condensed out at element level,
$$
\boldsymbol K^\mathrm{eff}=\boldsymbol K_{aa}-\boldsymbol K_{a\alpha}\boldsymbol K_{\alpha\alpha}^{-1}\boldsymbol K_{\alpha a},\qquad \boldsymbol f^\mathrm{eff}=\boldsymbol f-\boldsymbol K_{a\alpha}\boldsymbol K_{\alpha\alpha}^{-1}\boldsymbol 0.
$$
The same condensation is repeated with the current tangent at every iteration, so the formulation works with nonlinear materials.
A $2\times2$ Gauss rule is used, and the extra modes relieve the shear locking of the fully integrated bilinear quad.
The assumed-stress alternatives [`PS`](../Mixed/PS.md) and [`QE2`](../Mixed/QE2.md) achieve a similar improvement without incompatible displacements.

## Syntax

```text title="CP4I"
element CP4I (1) (2...5) (6) [7]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```

## Remarks

* The element has no reduced-integration or nonlinear-geometry switch in the current parser.
* The thickness argument is ignored when the material declares plane strain.
* Static condensation is performed both for the initial stiffness and at every trial state, so the internal parameters follow the material tangent.
* The incompatible modes are internal to the element and do not add global DoFs or mass.
* Distorted quadrilaterals can make $\boldsymbol K_{\alpha\alpha}$ ill conditioned; keep elements reasonably rectangular.
* Compare with [`CP4`](CP4.md) for the plain bilinear quad and with [`QE2`](../Mixed/QE2.md) for a mixed formulation with two enhanced strains.

## References

1. E. L. Wilson, R. L. Taylor, W. P. Doherty and J. Ghaboussi, *Incompatible displacement models*, in *Numerical and Computer Methods in Structural Mechanics*, Academic Press (1973), pp. 43-57.
2. R. L. Taylor, P. J. Beresford and E. L. Wilson, *A non-conforming element for stress analysis*, International Journal for Numerical Methods in Engineering 10(6), 1211-1219 (1976), [doi:10.1002/nme.1620100602](https://doi.org/10.1002/nme.1620100602).
3. T. J. R. Hughes, *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis*, Dover (2000), Section 4.7.
