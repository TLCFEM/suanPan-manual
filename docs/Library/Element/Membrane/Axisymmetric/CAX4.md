# CAX4

Axisymmetric Linear Quadrilateral

* Number of Nodes: 4
* Number of DoFs: 2
* DoF Label: RADIAL, AXIAL

## Background

[`CAX4`](CAX4.md) models a body of revolution by discretising its meridional $(r,z)$ section with four-node quadrilaterals.
The only nodal DoFs are the radial displacement $u_r$ and the axial displacement $u_z$; the circumferential displacement vanishes by symmetry.
A material point is described by the triple $(r,\theta,z)$ and the nonzero small-strain components are
$$
\varepsilon_{rr}=\frac{\partial u_r}{\partial r},\qquad \varepsilon_{zz}=\frac{\partial u_z}{\partial z},\qquad \varepsilon_{\theta\theta}=\frac{u_r}{r},\qquad \gamma_{rz}=\frac{\partial u_r}{\partial z}+\frac{\partial u_z}{\partial r}.
$$
The hoop strain $\varepsilon_{\theta\theta}$ is the essential difference from plane strain: a radial displacement changes the radius of the material circle and therefore its circumference.
The strain vector is ordered as $\boldsymbol\varepsilon=[\varepsilon_{rr},\varepsilon_{zz},\varepsilon_{\theta\theta},\gamma_{rz}]^\mathrm T$, and the material must return a $4\times4$ tangent matrix for the axisymmetric plane type.

With the isoparametric interpolation $\boldsymbol x=\sum_aN_a\boldsymbol x_a$ and $\boldsymbol u=\sum_aN_a\boldsymbol u_a$, the strain-displacement matrix contains one extra row,
$$
\boldsymbol B_a=\begin{bmatrix}
N_{a,r}&0\\
0&N_{a,z}\\
N_a/r&0\\
N_{a,z}&N_{a,r}
\end{bmatrix}.
$$
The volume element of the revolve is $\mathrm dV=2\pi r\,\mathrm dA=2\pi r\,J\,\mathrm d\xi\,\mathrm d\eta$, so the quadrature weight at each Gauss point is $2\pi r_q J_q w_q$.
The implementation evaluates $r_q$ by interpolating the four nodal radii with the quadratic monomial vector $[1,\xi,\eta,\xi\eta]$, which reproduces the exact bilinear geometry.
The stiffness and resistance are
$$
\boldsymbol K^e=\sum_{q=1}^{4}2\pi r_qJ_qw_q\,\boldsymbol B_q^\mathrm T\boldsymbol D_q\boldsymbol B_q,\qquad \boldsymbol f^e=\sum_{q=1}^{4}2\pi r_qJ_qw_q\,\boldsymbol B_q^\mathrm T\boldsymbol\sigma_q.
$$
The default quadrature is the full $2\times2$ Gauss rule, and no reduced-integration token is registered for [`CAX4`](CAX4.md) in the element parser.

Because the hoop strain contains $1/r$, the formulation is singular on the symmetry axis and the Gauss points should stay at positive radius.

!!! warning "implementation limitation"
    The implementation does not special-case an element that crosses the axis of revolution.
    A Gauss point at or very near zero radius produces an unbounded hoop-strain row in $\boldsymbol B$ and an ill-conditioned stiffness.

The linear triangle [`CAX3`](CAX3.md) evaluates all quantities at the element centroid radius, whereas [`CAX8`](CAX8.md) uses an 8-node quadratic interpolation and a higher-order rule.
The plane-stress and plane-strain counterparts of the same interpolation are [`CP4`](../Plane/CP4.md) and [`CP8`](../Plane/CP8.md).

## Syntax

```text title="CAX4"
element CAX4 (1) (2...5) (6)
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
```

## Remarks

* The assigned material must declare an axisymmetric plane type; [`CAX4`](CAX4.md) rejects a plane-stress or plane-strain material at initialisation.
* The nodal DoF labels are `RADIAL` and `AXIAL`, so boundary conditions must be applied to those labels rather than to `U1` and `U2`.
* The element has no thickness argument because the physical volume is obtained by revolving the section through $2\pi$.
* Full $2\times2$ Gauss integration is used, which makes the element locking-prone in bending and in nearly incompressible plasticity; use [`CAX8`](CAX8.md) for higher accuracy.
* The parser hardcodes the nonlinear-geometry switch to false, so the current command path evaluates only the small-strain axisymmetric formulation.

!!! info "deviation from theory"
    The element print routine reports a Total Lagrangian option, but no parser token exposes that switch for `CAX4`.
    The nonlinear branch exists in the class but is unreachable from an `element CAX4` command.

* Avoid placing Gauss points on the axis of revolution because the hoop strain $u_r/r$ is singular there.

## References

1. O. C. Zienkiewicz, R. L. Taylor and J. Z. Zhu, *The Finite Element Method: Its Basis and Fundamentals*, 7th ed., Butterworth-Heinemann (2013), Chapter 9.
2. T. J. R. Hughes, *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis*, Dover (2000), Section 3.8.
3. J. C. Simo and T. J. R. Hughes, *Computational Inelasticity*, Springer (1998), Chapter 9.
