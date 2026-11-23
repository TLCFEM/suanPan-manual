# Damper01/Damper03

Viscous/Nonviscous Damper

This damper uses **displacement** and **velocity** as inputs, not strain and strain rate, which means element length is not used to compute strain or strain rate.

## Damper01

This `Damper01` is a simple 2D viscous/nonviscous damper.

See this [example](../../../Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md).

* Number of Nodes: 2
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2

## Damper03

This `Damper03` is a simple 3D viscous/nonviscous damper.

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Translation)
* DoF Label: U1, U2, U3

## Background

A viscous damper supplies a force proportional to the relative velocity of its two ends, so on its own it dissipates energy without storing it.
Let $\boldsymbol c$ be the unit vector from node $i$ to node $j$, computed once from the initial coordinates, and define $\Delta\boldsymbol u=\boldsymbol u_j-\boldsymbol u_i$ and $\Delta\boldsymbol v=\boldsymbol v_j-\boldsymbol v_i$.
The element passes the projected displacement and velocity

$$
\epsilon=\boldsymbol c\cdot\Delta\boldsymbol u,\qquad
\dot\epsilon=\boldsymbol c\cdot\Delta\boldsymbol v
$$

to the associated one-dimensional material, which returns a force $N$ and a tangent damping coefficient $c_t=\partial N/\partial\dot\epsilon$.
The element length does not enter these expressions, so $\epsilon$ is a displacement rather than a strain and the material must use a displacement--force or displacement--velocity law.

!!! info "deviation from theory"
    A standard axial bar or dashpot converts the relative velocity into a strain rate by dividing by the member length.
    This element passes the raw projected velocity, so the material coefficient must be given as force per velocity rather than as a viscosity in stress per strain rate.
The assembled resistance and damping matrix are

$$
\boldsymbol R_j=\boldsymbol c\,N,\qquad \boldsymbol R_i=-\boldsymbol R_j,\qquad
\boldsymbol C_e=\begin{bmatrix}\boldsymbol c\\-\boldsymbol c\end{bmatrix}c_t\begin{bmatrix}\boldsymbol c&-\boldsymbol c\end{bmatrix}^{\mathrm T}.
$$

If the material also returns a tangent stiffness, the same rank-one projection is applied to form $\boldsymbol K_e$.
Since the damping matrix is built at element level, the element-level modifiers described on the [`Modifier`](../Modifier/Modifier.md) page can be used to inspect or replace it.

!!! warning "implementation limitation"
    The constructor sets `modify_viscous` to false.
    Element damping modifiers such as `LinearViscosity` and `ElementalLee` skip this element, so its damping must come from the assigned material.

## Syntax

```text title="Damper01"
element Damper01 (1) (2) (3) (4)
element Damper03 (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag of associated (non)viscosity material
```

## Remarks

Both viscous and nonviscous materials can be used for this element, see [Viscosity](../../Material/Material1D/Viscosity/NonlinearViscosity.md).

1. The material sees the projected relative displacement and velocity, so its stiffness has units of force per length and its damping coefficient has units of force per velocity.
2. The direction $\boldsymbol c$ is fixed at initialisation from the initial node coordinates, so a large rigid rotation of the damper is not followed.
3. A material that defines only a viscous force, such as a power-law dashpot, is sufficient; a separate spring can be added with [`Spring01`](Spring01.md) or with the Maxwell model in [`Damper02`](Damper02.md).
4. `Damper05` and `Damper06` feed only the relative velocity and contribute a pure viscous force, whereas `Damper01` and `Damper03` feed both displacement and velocity and may also return a stiffness.

## Variants

`Damper05` is the revised 2D damper: `element Damper05 (1) (2) (3) (4)` takes only the two nodes and one damper material tag, and feeds the material the relative velocity alone instead of both displacement and velocity, so the element length is not used.
`Damper06` is the 3D counterpart with the same four arguments and three translational DoFs per node.
