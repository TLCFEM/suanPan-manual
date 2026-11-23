# MolecularDynamics3D

The `MolecularDynamics3D` constraint runs a molecular-dynamics particle simulation in three dimensions.
It builds a cell list of active DEM particle elements and applies the referenced [`interaction`](Interaction.md) objects to each neighbouring pair.

## Syntax

```text title="MolecularDynamics3D"
MolecularDynamics3D (1) (2...)
constraint MolecularDynamics3D (1) (2...)
# (1) int, unique constraint tag
# (2...) int, tags of active interactions to apply
```

## Theory

Particles are represented by `SphericalParticle3D` elements, each providing radius, elastic modulus, Poisson ratio, damping and mass.
The cell size is twice the largest particle radius in the model.
For each candidate pair, an `InteractionPair` combines the two particles into effective mass, radius, modulus and damping values before the interactions are evaluated.

## Remarks

Only active elements of type `DEM` are included in the neighbour search.
Only active interactions referenced by the given tags are applied.
The full or sparse matrix storage scheme is required.

## Example

```text
node 1 0 0 0
element SphericalParticle3D 1 1 1. 1e3 .2 1e-4 1.
interaction Hertzian 1
constraint MolecularDynamics3D 1 1
```
