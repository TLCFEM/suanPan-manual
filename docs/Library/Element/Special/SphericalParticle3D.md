# SphericalParticle3D

Spherical DEM Particle in 3D

A discrete-element particle that attaches a sphere of given radius to a single node and carries the properties used by pairwise particle interactions: elastic modulus, Poisson ratio and damping, together with its mass.
The element defines no stiffness of its own; it contributes a constant diagonal mass matrix and exposes its parameters to the DEM contact constraints.

* Number of Nodes: 1
* Number of DoFs: 3 (Translation, Translation, Translation), or 6 if inertia is supplied
* DoF Label: U1, U2, U3, optionally UR1, UR2, UR3
* Element Type: DEM
* Constant Mass Matrix, No Stiffness

## Syntax

```text title="SphericalParticle3D"
element SphericalParticle3D (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique element tag
# (2) int, node tag
# (3) double, particle radius
# (4) double, elastic modulus
# (5) double, Poisson ratio
# (6) double, damping
# (7) double, mass
# [8] double, optional rotational inertia
```

## Remarks

1. With five parameters `(3)...(7)`, the element is `SphericalParticle3D`: it has DoFs U1, U2 and U3 and a mass matrix $$\mathrm{diag}(m,m,m)$$.
2. If the inertia `(8)` is given, `InertialSphericalParticle3D` is created instead: the rotational DoFs UR1, UR2 and UR3 are added and the mass matrix becomes $$\mathrm{diag}(m,m,m,I,I,I)$$.
3. The radius, damping, elastic modulus and Poisson ratio are read by DEM interactions to build the effective radius, damping and modulus of a particle pair, so use a unit system consistent with the rest of the model.
4. Use this element together with an [interaction](../../../Collection/Define/interaction.md) and a `MolecularDynamics3D` constraint, as in the `Other/MD3D` example.

## Example

```text
element SphericalParticle3D 1 1 1. 1e3 .2 1e-4 1.
```
