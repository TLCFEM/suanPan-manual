# Guide

Only general purpose elements for plane strain/stress problems are included.
For other special purpose elements, there are not many options anyway.

## Background

A membrane element models a two-dimensional continuum that carries in-plane normal and shear stress.
The displacement field is $\boldsymbol u=[u_1,u_2]^\mathrm T$ and the small-strain tensor is $\boldsymbol\varepsilon=\operatorname{sym}\nabla\boldsymbol u$.
In Voigt order the strain vector is $\boldsymbol\varepsilon=[\varepsilon_{11},\varepsilon_{22},\gamma_{12}]^\mathrm T$ with $\gamma_{12}=2\varepsilon_{12}$, so that $\boldsymbol\sigma^\mathrm T\boldsymbol\varepsilon=\sigma_{11}\varepsilon_{11}+\sigma_{22}\varepsilon_{22}+\tau_{12}\gamma_{12}$.
The governing equation is $\nabla\cdot\boldsymbol\sigma+\boldsymbol b=\boldsymbol 0$ and the constitutive law is $\boldsymbol\sigma=\boldsymbol D\boldsymbol\varepsilon$, with $\boldsymbol D$ supplied by the assigned material.

The plane assumption is selected by the material rather than by the element token.
Under plane stress $\sigma_{33}=0$ and $\varepsilon_{33}=-\nu(\varepsilon_{11}+\varepsilon_{22})/(1-\nu)$ follows from the constitutive law.
Under plane strain $\varepsilon_{33}=0$ and a reaction stress $\sigma_{33}=\nu(\sigma_{11}+\sigma_{22})$ develops, so the thickness argument is overridden to unity in the implementation.
The axisymmetric family uses a four-component strain vector $[\varepsilon_{rr},\varepsilon_{zz},\varepsilon_{\theta\theta},\gamma_{rz}]$ and replaces $\varepsilon_{33}$ by the hoop strain $\varepsilon_{\theta\theta}=u_r/r$.

!!! info "deviation from theory"
    ABAQUS-style names such as CPS4, CPE3 and CPS8R are only descriptive in the source class comments.
    The element parser registers a single token per geometry for most membrane elements, with plane stress and plane strain distinguished by the material plane type.

All elements on this page are isoparametric, meaning geometry and displacement use the same nodal shape functions $N_a(\xi,\eta)$.
$$
\boldsymbol x=\sum_{a=1}^{n}N_a(\xi,\eta)\,\boldsymbol x_a,\qquad \boldsymbol u=\sum_{a=1}^{n}N_a(\xi,\eta)\,\boldsymbol u_a,\qquad \boldsymbol\varepsilon=\boldsymbol B\boldsymbol a.
$$
Here $\boldsymbol a$ collects the nodal displacements and $B_{ia}=\partial N_a/\partial x_i$ is assembled in Voigt form, with physical derivatives obtained from $\boldsymbol J^{-1}\partial N_a/\partial\boldsymbol\xi$ and $\boldsymbol J=\partial\boldsymbol x/\partial\boldsymbol\xi$.
The element stiffness is evaluated by numerical quadrature,
$$
\boldsymbol K^e=\int_{\Omega^e}\boldsymbol B^\mathrm T\boldsymbol D\boldsymbol B\,t\,\mathrm d\Omega=\sum_{q=1}^{n_q}\boldsymbol B_q^\mathrm T\boldsymbol D_q\boldsymbol B_q\,t\,J_q\,w_q,
$$
where $J_q$ is the Jacobian determinant, $w_q$ the quadrature weight, $t$ the thickness and $n_q$ the number of integration points.

The node-ordering convention is counter-clockwise around the element.
For quadrilaterals node 1 is at $(\xi,\eta)=(-1,-1)$ and nodes 2, 3, 4 follow counter-clockwise.
The 5-, 6- and 7-node quadrilaterals add midside nodes on the bottom, right and top edges in that order, while the 8-node quadrilateral adds the left-edge midside node as well.
For triangles nodes 1 to 3 occupy the vertices and nodes 4 to 6 the corresponding edge midpoints.

Low-order fully integrated elements lock in bending and in nearly incompressible plasticity because their discrete strain space is too rich in volumetric and shear modes.
Reduced integration removes the locking but creates zero-energy hourglass modes that must be stabilised, as implemented in [`CP4`](Plane/CP4.md) through an orthogonal hourglass stiffness.
Mixed and assumed-strain formulations avoid both difficulties, either by assuming the stress field as in [`PS`](Mixed/PS.md) and [`QE2`](Mixed/QE2.md), or by adding internally condensed incompatible modes as in [`CP4I`](Plane/CP4I.md).
The quadratic elements [`CP6`](Plane/CP6.md) and [`CP8`](Plane/CP8.md) improve accuracy on curved boundaries and in bending dominated problems.
The phase-field fracture elements [`DCP3`](PFM/DCP3.md) and [`DCP4`](PFM/DCP4.md) add a nodal damage DoF to a standard displacement interpolation.
The mapped infinite element [`CINP4`](Plane/CINP4.md) extends one parent direction to infinity for unbounded domains, and the couple-stress family [`CS`](CS.md) adds a drilling rotation together with a characteristic length.

## Element selection

Try the following decision tree to find the best membrane element to use.

1. Is the geometry regular or irregular?
   * regular --- use quadrilateral elements that are often more flexible than triangular elements and thus provide better results with the same amount of DoFs
   * irregular --- use triangular elements unless a good mesh can be generated to avoid distorted geometry

## Triangular Elements

1. Is drilling DoF required?
   * yes --- [`Allman`](Drilling/Allman.md)
   * no --- go to Q2
2. Prefer speed or accuracy?
   * speed --- [`CP3`](Plane/CP3.md)
   * accuracy --- [`CP6`](Plane/CP6.md)

Noting that the [`CP3`](Plane/CP3.md) element is very rigid and often requires a very dense mesh to get relatively accurate results, it is not recommended for most applications.

## Quadrilateral Elements

1. Is drilling DoF required?
   * yes --- go to Q2
   * no --- go to Q3
2. Is consistent material stiffness available?
   * yes --- go to Q6
   * no --- [`GQ12`](Drilling/GQ12.md), it does not require local inversion so it works even when the material tangent stiffness is not exact (but global convergence may still be an issue)
3. Used in elastoplastic applications?
   * yes --- normally mixed formulation is better, go to Q4, alternatively displacement based formulation, go to Q5
   * no --- go to Q5
4. Prefer speed or accuracy?
   * speed --- [`PS`](Mixed/PS.md), very cheap to compute, only with a different strain matrix
   * accuracy --- [`QE2`](Mixed/QE2.md), has enhanced strain field, requires more local computation
5. Prefer speed or accuracy?
   * speed --- [`CP4I`](Plane/CP4I.md) or second option [`CP4`](Plane/CP4.md)
   * accuracy --- [`CP8R`](Plane/CP8.md) or second option [`CP8`](Plane/CP8.md)
6. Need faster analysis?
   * yes --- [`SGCMQ`](Drilling/GCMQ.md), GCMQ with no enhanced strain, very cheap to compute, only with a different strain matrix
   * no --- [`GCMQ`](Drilling/GCMQ.md), best coarse mesh accuracy, requires local inversion

## References

1. O. C. Zienkiewicz, R. L. Taylor and J. Z. Zhu, *The Finite Element Method: Its Basis and Fundamentals*, 7th ed., Butterworth-Heinemann (2013), Chapters 8 and 9.
2. T. J. R. Hughes, *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis*, Dover (2000), Chapters 3 and 4.
3. J. C. Simo and T. J. R. Hughes, *Computational Inelasticity*, Springer (1998), Chapter 9.
