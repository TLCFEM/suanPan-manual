# Modifier

## Brief

Sometimes it is necessary to modify the existing element data.
A concrete example is the damping matrix used in dynamic analyses.

In a standard element, stiffness matrix could be solely computed according to its formulation.
However, mass matrix could be formulated in multiple ways such as consistent, lumped, to name a few.
For lumped formulation, there are also several versions.
If the Rayleigh type damping is used, damping matrix shall be related to both mass matrix and stiffness matrix.
Furthermore, the weights shall be computed based on global structure properties, in other words, it is not possible to determine those weights within the element.
Besides, other types of damping formulation could also be used.

Such variance existing in element formulation raises a demand of the `Modifier` class.
A `Modifier` object can exist independently and can access and modify some data of the target elements.
This provides great convenience in defining customizable behavior for different elements.

## Background

The semi-discrete equations of motion of a structure are

$$
\boldsymbol M\ddot{\boldsymbol u}+\boldsymbol C\dot{\boldsymbol u}+\boldsymbol K\boldsymbol u=\boldsymbol f ,
$$

with assembled mass, damping and stiffness matrices.
A modifier acts on the element matrices $\boldsymbol M_e$, $\boldsymbol C_e$ and $\boldsymbol K_e$ before assembly, so it can implement choices that an individual element cannot make on its own.

The mass matrix is not unique.
The consistent form

$$
\boldsymbol M_e^c=\int_{\Omega_e}\rho\,\boldsymbol N^{\mathrm T}\boldsymbol N\,\mathrm d\Omega_e
$$

uses the same shape functions $\boldsymbol N$ as the displacement interpolation and preserves the kinetic energy of the interpolated field, but it couples neighbouring DoFs.
A lumped matrix keeps the total mass while removing the coupling,

$$
M^{l}_{ii}=\sum_j M^c_{ij}.
$$

Diagonal mass is cheaper and is required by many explicit integrators, while consistent mass is usually more accurate for wave propagation.
Rotational DoFs carry entries representing the rigid-body kinetic energy $\tfrac12\boldsymbol\omega\cdot\boldsymbol I\boldsymbol\omega$; the point-mass elements on the [`Mass`](../Special/Mass.md) page are already lumped.

The damping matrix is even less uniquely defined.
Rayleigh damping assumes $\boldsymbol C=a\boldsymbol M+b\boldsymbol K$, and the general form used below is a linear combination of mass, initial, current and trial stiffness matrices.
The weights depend on global modal properties and therefore cannot be chosen inside an element; a modifier computes the element damping matrices once and lets the assembly build the global matrix.

Nonviscous damping replaces $\boldsymbol C\dot{\boldsymbol u}$ by a hereditary convolution,

$$
\boldsymbol f_d(t)=\int_0^t\boldsymbol g(t-\tau)\dot{\boldsymbol u}(\tau)\,\mathrm d\tau .
$$

With an exponential kernel $\boldsymbol g(t)=\sum_k\boldsymbol m_k e^{-s_k t}$ the integral can be advanced recursively from the current and previous velocities without storing the whole history, which is the idea behind [`ElementalNonviscous`](ElementalNonviscous.md).
A related approach forms a bell-shaped frequency-dependent damping ratio from mass and stiffness matrices at element level, as in [`ElementalLee`](ElementalLee.md), whereas [`LinearViscosity`](LinearViscosity.md) simply sets a diagonal element damping matrix proportional to velocity.

!!! info "deviation from theory"
    An element-level damping matrix is assembled from the modified element matrices, whereas a global Rayleigh model forms the damping matrix after global assembly.
    The two approaches do not in general give the same modal damping ratios for the same coefficients.

## Remarks

1. For all the following modifiers presented, if no element tag is provided, the modifier would be applied to **all** active elements in the domain.
2. All modifiers would be applied in the order of how they are defined.
   This is because the modified data would be used in another modifier, for example, it is possible to apply a lumped mass modifier and then use the modified mass matrix to form a Rayleigh damping matrix.
3. The lumped mass modifiers operate on element mass matrices; the lumped point masses themselves are defined by [`Mass`](../Special/Mass.md) and [`MassPoint2D`](../Special/MassPoint.md).
4. The elemental damping modifiers [`ElementalLee`](ElementalLee.md), [`ElementalNonviscous`](ElementalNonviscous.md) and [`LinearViscosity`](LinearViscosity.md) work on element matrices, so each element can record its own dissipated energy.
   In a global model such as [`RayleighNewmark`](../../Integrator/Implicit/Newmark/RayleighNewmark.md) the dissipated energy can only be recovered from global quantities.
5. Dynamic modifiers are applied only in a dynamic analysis and only to elements that allow the corresponding matrix to be modified.

## Simple Lumped Mass

```
modifier LumpedSimple (1) (2...)
# (1) int, unique modifier tag
# (2...) int, element tags
```

## Scale Lumped Mass

```
modifier LumpedScale (1) (2...)
# (1) int, unique modifier tag
# (2...) int, element tags
```

## Rayleigh Damping

The damping matrix would be defined as

$$
C=aM+bK_C+cK_I+dK_T,
$$

where $$M$$ is the mass matrix, $$K_C$$ is the current tangent stiffness matrix (converged from the last step), $$K_I$$ is the initial stiffness and $$K_T$$ is the trial stiffness of current iteration.
To retain quadratic convergence rate, one shall only use $K_I$ and $K_C$.
But $K_I$ also leads to unwanted response.

```
modifier Rayleigh (1) (2) (3) (4) (5) (6...)
# (1) int, unique modifier tag
# (2) double, a
# (3) double, b
# (4) double, c
# (5) double, d
# (6...) int, element tags
```

## Elemental Modal Damping

The rigid body modes are assumed to be undamped.
The modes whose frequencies are higher than the cut-off frequency are ignored.
The Wilson-Penzien approach is applied for each element.
Currently, only consistent mass matrix is supported.

```
modifier ElementalModal (1) (2) (3) (4...)
# (1) int, unique modifier tag
# (2) double, cut-off frequency
# (3) double, damping ratio
# (4...) int, element tags
```
