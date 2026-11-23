# MassPoint

The `MassPoint` element is used to represent a mass point with translational mass and optional rotational inertia.

## Background

`MassPoint2D` and `MassPoint3D` are convenience wrappers around the general [`Mass`](Mass.md) element that predefine the DoF set of a point mass.
They contribute a constant diagonal mass matrix and no stiffness, so they only enter the inertia term $\mathbf M\ddot{\mathbf u}$ of a dynamic analysis.

The translational magnitude $m$ is placed on all translation DoFs and the optional rotational magnitude $I$ is placed on all rotation DoFs, giving

$$
\mathbf M_e^{2D}=\operatorname{diag}(m,m,I),\qquad
\mathbf M_e^{3D}=\operatorname{diag}(m,m,m,I,I,I).
$$

This corresponds to the lumped rigid-body inertia $T=\tfrac12 m\lVert\dot{\mathbf u}\rVert^2+\tfrac12 I\lVert\mathbf\omega\rVert^2$ with an isotropic inertia tensor.
See [`Mass`](Mass.md) for the distinction between lumped and consistent mass matrices and for a more general DoF assignment.

!!! warning "implementation limitation"
    A single scalar inertia is assigned to every rotational DoF.
    An anisotropic inertia tensor with distinct principal moments cannot be specified with these elements.

## Syntax

```text title="MassPoint"
element MassPoint2D (1) (2) (3) [4]
element MassPoint3D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, node tag
# (3) double, translational mass magnitude
# [4] double, optional, rotational inertia magnitude
```

## Remarks

1. For 2D elements, `DOF::UX` and `DOF::UY` are assigned with the translational mass (equal magnitude), `DOF::URZ` is assigned with the rotational inertia (optional).
2. For 3D elements, `DOF::UX`, `DOF::UY`, and `DOF::UZ` are assigned with the translational mass (equal magnitude), `DOF::URX`, `DOF::URY`, and `DOF::URZ` are assigned with the rotational inertia (optional).
3. `MassPoint` elements are an alternative to `Mass` elements, which are more abstract and allow more general assignment of mass.
4. Omitting `[4]` creates only the translational DoFs and adds no rotational inertia.
5. The same scalar $I$ is used for all rotational DoFs, so distinct per-axis inertia values require several [`Mass`](Mass.md) elements with separate magnitudes.
6. Both magnitudes are constant mass properties, and the lumped mass modifiers skip these elements, as noted on the [`Mass`](Mass.md) page.
