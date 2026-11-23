# EB31OS

Elastic 3D Beam With Open Section

* Number of Nodes: 2
* Number of DoFs: 7 (Translation, Translation, Translation, Rotation, Rotation, Rotation, WARPING)
* DoF Label: U1, U2, U3, UR1, UR2, UR3, WARP

## Theory

[`EB31OS`](EB31OS.md) is the elastic three-dimensional open-section beam element and is the closed-form counterpart of [`B31OS`](B31OS.md).
It uses Vlasov thin-walled beam theory, in which torsion of an open section couples the twist $$\phi$$ with an axial warping displacement so that the cross-section has an additional warping degree of freedom.
The seven nodal DoFs are $$(U_1,U_2,U_3,UR_1,UR_2,UR_3,WARP)$$, and the `B3DOSL` or `B3DOSC` [orientation](Orientation.md) maps them to the nine local deformations $$\begin{bmatrix}u&\theta_{zi}&\theta_{zj}&\theta_{yi}&\theta_{yj}&\phi_i&\phi_j&\phi_i'&\phi_j'\end{bmatrix}$$.
The axial and bending parts are the usual $$EA/L$$, $$4EI_z/L$$, $$2EI_z/L$$, $$4EI_y/L$$ and $$2EI_y/L$$ terms.
The coupled torsion–warping stiffness is formed from the St. Venant torsional constant $$J$$ and the warping constant $$I_w$$, with the end-twist terms equal to $$\left(12EI_w/L^2+1.2GJ\right)/L$$ and the warping-rate terms equal to $$4EI_w/L+2GJL/15$$.
Here $$E$$ is the elastic modulus, $$G$$ is the shear modulus, $$A$$ is the area, $$I_z$$ and $$I_y$$ are the strong- and weak-axis moments of inertia, and $$L$$ is the element length.
The stiffness is assembled once and held constant by the `ConstantStiffness` mechanism, so no section definition or integration points are required.

## Syntax

```text title="EB31OS"
element EB31OS (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) [12]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) double, elastic modulus, E
# (5) double, shear modulus, G
# (6) double, area, A
# (7) double, major/strong axis moment of inertia, I_z
# (8) double, minor/weak axis moment of inertia, I_y
# (9) double, torsional constant, J
# (10) double, warping constant, I_w
# (11) int, orientation tag
# [12] bool, nonlinear geometry switch, default: false
```

## Remarks

1. Please check [`orientation`](Orientation.md) for its definition, for example, `B3DOSL` and `B3DOSC`.
2. To use the corotational formulation for nonlinearity, please attach a corotational formulation enabled `orientation`.
3. The seven property values in arguments `(4)` to `(10)` are $$E$$, $$G$$, $$A$$, $$I_z$$, $$I_y$$, $$J$$ and $$I_w$$, and they must be given in a consistent unit system.
4. During initialisation the element rejects an orientation whose type is not `B3DOS` or whose nonlinear-geometry flag disagrees with argument `[12]`.
5. See [`B31OS`](B31OS.md) for the section-based inelastic version and the [Beam Element Overview](Beam.md) for the meaning of the local deformations.
