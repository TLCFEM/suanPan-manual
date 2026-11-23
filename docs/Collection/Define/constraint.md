# constraint

The `constraint` command defines a constraint between nodes or between a node and a geometric entity.
Please refer to the specific constraint types for the available syntax.

All constraints are processed in **parallel**.

Most constraints are implemented using both the penalty function and the Lagrange multiplier methods.
A brief discussion of the differences can be found on the [Constraint](../../Library/Constraint/Constraint.md) page.

## Syntax

```text title="constraint"
constraint (1) (2) ...
# (1) string, constraint type
# (2) int, unique constraint tag
```

## Short Forms

The leading `constraint` keyword can be replaced by a dedicated first-level command with the same arguments.

| Shortcut | Equivalent constraint type |
|----------|----------------------------|
| `mpc` | `MPC` |
| `fixedlength2d`, `fixedlength3d` | `FixedLength2D`, `FixedLength3D` |
| `maxforce2d`, `maxforce3d` | `MaxForce2D`, `MaxForce3D` |
| `maxgap2d`, `maxgap3d` | `MaxGap2D`, `MaxGap3D` |
| `mingap2d`, `mingap3d` | `MinGap2D`, `MinGap3D` |
| `nodefacet`, `nodeline` | `NodeFacet`, `NodeLine` |
| `finiterigidwall`, `finiterigidwallpenalty`, `finiterigidwallmultiplier` | the corresponding `FiniteRigidWall*` types |
| `finiterestitutionwall`, `finiterestitutionwallpenalty` | the corresponding `FiniteRestitutionWall*` types |
| `rigidwallpenalty`, `rigidwallmultiplier` | `RigidWallPenalty`, `RigidWallMultiplier` |
| `particlecollision2d`, `particlecollision3d` | `ParticleCollision2D`, `ParticleCollision3D` |
| `moleculardynamics2d`, `moleculardynamics3d` | `MolecularDynamics2D`, `MolecularDynamics3D` |
| `sleeve2d`, `sleeve3d` | `Sleeve2D`, `Sleeve3D` |
