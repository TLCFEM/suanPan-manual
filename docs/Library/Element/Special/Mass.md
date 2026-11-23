# Mass

Point Mass

* Number of Nodes: 1
* Number of DoFs: varies

## Background

In a dynamic analysis the inertia contribution to equilibrium is $$\mathbf M\ddot{\mathbf u}$$, where the element consistent mass matrix is

$$
\mathbf M_e^c=\int_{\Omega_e}\rho\,\mathbf N^{\mathrm T}\mathbf N\,\mathrm d\Omega_e .
$$

It is built from the same displacement interpolation $$\mathbf N$$ as the stiffness, so it reproduces the kinetic energy of the interpolated field, but it couples neighbouring DoFs.
A lumped mass matrix replaces it by a diagonal matrix whose row sums preserve the total mass,

$$
M^{l}_{ii}=\sum_j M^c_{ij},\qquad
\sum_i M^{l}_{ii}=\int_{\Omega_e}\rho\,\mathrm d\Omega .
$$

A diagonal mass matrix is cheaper and is required by many explicit time integrators, whereas a consistent matrix is generally more accurate for wave propagation.
The `Mass`, `Mass2D` and `Mass3D` elements are already lumped: each selected DoF receives the same scalar magnitude $$m$$ on the diagonal and there is no off-diagonal coupling.

For a rigid body the kinetic energy is

$$
T=\dfrac12 m\,\dot{\mathbf u}\cdot\dot{\mathbf u}+\dfrac12\mathbf\omega\cdot\mathbf I\,\mathbf\omega ,
$$

so rotational inertia appears as additional diagonal entries on the rotation DoFs.
[`MassPoint2D`](MassPoint.md) and [`MassPoint3D`](MassPoint.md) place the translational mass $$m$$ on the translation DoFs and an optional scalar inertia $$I$$ on the rotation DoFs, giving $$\mathrm{diag}(m,m,I)$$ in 2D and $$\mathrm{diag}(m,m,m,I,I,I)$$ in 3D.
Because a single scalar $$I$$ is used, the inertia tensor is isotropic, which is appropriate for a point-like or spherically symmetric mass lump.

!!! warning "implementation limitation"
    A full inertia tensor with distinct principal moments is not supported by the point-mass elements.
    Each assigned DoF receives the same magnitude $$m$$, so off-diagonal mass coupling is absent.

A point mass can also be represented as an external D'Alembert inertia load or as an attribute of a node.
Defining it as an element makes the mass matrix available during assembly, before loads are applied, and keeps point masses in the same tag pool as the other elements.
The element has no stiffness, so it does not contribute to a static analysis.

!!! warning "implementation limitation"
    The lumped mass modifiers `LumpedSimple` and `LumpedScale` skip these elements, so the entered magnitude is used unchanged.

!!! note "developer note"
    `MassBase` sets `modify_mass` to false.

## Syntax

```text title="Mass"
Mass (1) (2) (3) (4...)
element Mass (1) (2) (3) (4...)
# (1) int, unique element tag
# (2) int, node tag
# (3) double, magnitude
# (4...) int, dof tag
```

Point mass is implemented via an element interface that connects only one node.
No stiffness is defined within that element.
Thus, a `Mass` object shares the same tag pool with the other elements.

## Variants

`Mass2D` creates a planar point mass: `Mass2D (1) (2) (3) (4...)` accepts at most three DoF tags, which map to U1, U2 and UR3, and no element is created if a tag larger than three is given.
`Mass3D` creates a spatial point mass with at most six DoF tags, which map to U1, U2, U3, UR1, UR2 and UR3; plain `Mass` is an alias for `Mass3D`.

1. The same magnitude is assigned to every listed DoF, so distinct translational and rotational values require [`MassPoint2D`](MassPoint.md) or [`MassPoint3D`](MassPoint.md).
2. A DoF tag larger than three in 2D or six in 3D is rejected by the parser.
3. The mass matrix is constant and the lumped mass modifiers skip these elements, as discussed on the [`Modifier`](../Modifier/Modifier.md) page.
4. For a consistent mass matrix use a continuum element with a density-bearing material; `Mass` only supplies a lumped diagonal contribution.
