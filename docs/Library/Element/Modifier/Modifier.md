# Modifier

## Brief

Sometimes it is necessary to modify the existing element data. A concrete example is the damping matrix used in dynamic
analyses.

In a standard element, stiffness matrix could be solely computed according to its formulation. However, mass matrix
could be formulated in multiple ways such as consistent, lumped, to name a few. For lumped formulation, there are also
several versions. If the Rayleigh type damping is used, damping matrix shall be related to both mass matrix and
stiffness matrix. Furthermore, the weights shall be computed based on global structure properties, in other words, it is
not possible to determine those weights within element. Besides, other types of damping formulation could also be used.

Such variance existing in element formulation raises a demand of the `Modifier` class. A `Modifier` object can exist
independently and can access and modify some data of the target elements. This provides great convenience in defining
customizable behavior for different elements.

## Remarks

1. For all the following modifiers presented, if no element tag is provided, the modifier would be applied to **all**
   active elements in the domain.
2. All modifiers would be applied in the order of how they are defined. This is because the modified data would be used
   in another modifier, for example, it is possible to apply a lumped mass modifier and then use the modified mass
   matrix to form a Rayleigh damping matrix.

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

where $$M$$ is the mass matrix, $$K_C$$ is the current tangent stiffness matrix (converged from the last step), $$K_I$$
is the initial stiffness and $$K_T$$ is the trial stiffness of current iteration. To retain quadratic convergence rate,
one shall only use $K_I$ and $K_C$. But $K_I$ also leads to unwanted response.

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

The rigid body modes are assumed to be undampened. The modes whose frequencies are higher than the cut-off frequency is
ignored. The Wilson-Penzien approach is applied for each element. Currently, only consistent mass matrix is supported.

```
modifier ElementalModal (1) (2) (3) (4...)
# (1) int, unique modifier tag
# (2) double, cut-off frequency
# (3) double, damping ratio
# (4...) int, element tags
```
