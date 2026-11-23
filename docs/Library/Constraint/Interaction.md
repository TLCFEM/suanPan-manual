# Interaction

The `interaction` command defines reusable pairwise laws for molecular-dynamics particle simulations.
It is referenced by tag from [`MolecularDynamics2D`](MolecularDynamics2D.md) or [`MolecularDynamics3D`](MolecularDynamics3D.md).

## Syntax

```text title="Interaction"
interaction Hertzian (1)
interaction FixedParticle (1) (2) (3...)
# (1) int, unique interaction tag
# (2) double, penalty multiplier for FixedParticle
# (3...) int, tags of particle elements to be fixed
```

## Types

`Hertzian` implements normal contact between colliding pairs of spherical particles.
The repulsive force grows with the effective modulus and the compression, which is the overlap of the two radii, and a damping term based on the relative normal velocity dissipates energy until the particles separate.

`FixedParticle` holds the listed particle elements in place by constraining their DoFs, adding `multiplier` times the element mass to the mass matrix diagonal and `multiplier` times the elastic modulus to the stiffness matrix diagonal for an implicit integrator.

## Remarks

Only active interactions are collected when the molecular-dynamics constraint is initialised.
The molecular-dynamics constraints require the full or sparse matrix storage scheme.

## Example

```text
element SphericalParticle2D 1 1 1. 1e3 .2 1e-4 1.
interaction Hertzian 1
interaction FixedParticle 2 1e4 1
constraint MolecularDynamics2D 1 1 2
```
