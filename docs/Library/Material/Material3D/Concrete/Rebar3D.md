# Rebar3D

Orthotropic Material

## Background

This model represents three orthogonal families of smeared reinforcement embedded in a continuum.
Each family is described by a one-dimensional material and a reinforcement ratio, and the three families act in parallel along the global coordinate axes.
The three referenced materials must be one-dimensional material models.

The stiffness contribution of a single family is the product of its reinforcement ratio and the tangent stiffness of the underlying bar material,

$$
\boldsymbol D^i=\rho_i\,E_i^T\,\boldsymbol e_i\otimes\boldsymbol e_i,\qquad
\boldsymbol\sigma=\sum_{i=x,y,z}\rho_i\,\sigma_i\,\boldsymbol e_i,
$$

where $\rho_i$ is the reinforcement ratio, $\sigma_i$ and $E_i^T$ are the stress and tangent modulus returned by the $i$-th one-dimensional material, and $\boldsymbol e_i$ is the corresponding global axis.
Only the three normal stress components are produced; the shear components of stress and stiffness remain zero.
Each one-dimensional material receives the corresponding normal component of the strain vector as its trial strain, so uniaxial effects such as yielding, buckling or damage are inherited directly from the assigned materials.
This is a smeared, perfectly bonded representation: no slip, dowel action or discrete crack interaction is modelled.

!!! warning "implementation limitation"
    The model has zero shear stiffness and cannot stand alone as a three-dimensional material.
    The reinforcement directions are fixed to the global axes unless the model is wrapped in [`Rotation3D`](../../Wrapper/Rotation3D.md).
    The reinforcement ratios are not converted to absolute values, so a negative input is accepted by the parser even though it is physically meaningless.

## Syntax

```text title="Rebar3D"
material Rebar3D (1) (2) (3) (4) (5) (6) (7)
# (1) int, unique material tag
# (2) int, x direction steel material tag
# (3) int, y direction steel material tag
# (4) int, z direction steel material tag
# (5) double, x direction reinforcement ratio
# (6) double, y direction reinforcement ratio
# (7) double, z direction reinforcement ratio
```

The uniform reinforcement is defined along global axes.
To have an arbitrarily aligned layout, users can wrap it into a [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.

## Remarks

- Initialisation fails unless all three referenced material tags exist and are of type `D1`.
- The reinforcement ratios are dimensionless volume fractions and are not converted to absolute values, so negative ratios are accepted by the code but are physically meaningless.
- A ratio of zero effectively removes that reinforcement direction, but a valid one-dimensional material tag must still be supplied.
- The shear stiffness of this model is zero, so it must be combined with a matrix material; use [`Stacked`](../../Wrapper/Stacked.md) to add it to a concrete model such as [`CDP`](CDP.md) or [`CDPM2`](CDPM2.md).
- A common choice is a bilinear or hysteretic one-dimensional steel model for each direction; see [`Bilinear1D`](../../Material1D/vonMises/Bilinear1D.md) and [`SteelBRB`](../../Material1D/Hysteresis/SteelBRB.md) for compatible one-dimensional materials.
- Recorded quantities from the three bar materials are returned in the order x, y and z, which is useful for checking yielding of individual reinforcement directions.

## References

1. Finite element analysis of reinforced concrete beams, ACI Journal, 64(3), 152--163
