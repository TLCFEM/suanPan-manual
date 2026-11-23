# interaction

The `interaction` command defines a pairwise interaction between particles for use by molecular dynamics constraints such as `MolecularDynamics2D` and `MolecularDynamics3D`.
Two interaction types are available: `Hertzian` and `FixedParticle`.
Related particle contact constraints are described on the [ParticleCollision](../../Library/Constraint/ParticleCollision.md) page.

## Syntax

```text title="interaction"
interaction (1) (2) ...
# (1) string, interaction type
# (2) int, unique interaction tag
```

## Remarks

1. `Hertzian` takes no arguments beyond the tag and applies a Hertzian contact force between particle pairs.
2. `FixedParticle` takes a penalty multiplier followed by the tags of the particles to be fixed, for example, `interaction FixedParticle 2 1E4 3`.
3. Interaction objects are referenced by tag in molecular dynamics constraints, for example, `constraint MolecularDynamics3D 1 1 2` uses interactions 1 and 2.
