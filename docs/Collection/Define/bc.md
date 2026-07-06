# bc

Although called boundary condition, here we only deal with trivial Dirichlet boundary condition.

## Syntax

There are currently several commands to define boundary conditions.

```
fix (1) (2) (3...)
fix2 (1) (2) (3...)
multiplierbc (1) (2) (3...)
penaltybc (1) (2) (3...)
# (1) int, unique tag
# (2) string, dof identifier
# (3...) int, tags of nodes that shall be constrained
```

To apply BCs to node groups, it is possible to use the following commands.

```
groupmultiplierbc (1) (2) (3...)
grouppenaltybc (1) (2) (3...)
# (1) int, unique tag
# (2) string, dof identifier
# (3...) int, tags of groups that shall be constrained
```

## Remark

1.  Both `fix` and `fix2` serve the same purpose but with different approaches. The `fix` command modifies the
    corresponding main diagonal term by multiplying a large number, for example $$10^8$$. The `fix2` command erase the
    column and row of target DoF and set the main diagonal to unity. In both case, the corresponding right hand side
    entry is erased.
2.  The `fix` and `penaltybc` commands is computationally efficient but leads to an ill-conditioned matrix. This may not
    be a problem for direct solvers but will greatly affect the performance of iterative solvers. The penalty number can
    be controlled by [`set`](../Process/set.md) command via `constraint_multiplier` option.
3.  The `fix2` and `multiplierbc` commands requires more operations but the final matrix is well conditioned.
4.  The performance difference is almost negligible. Either one can be used with direct solvers. The error won't
    accumulate as there is a special mechanism to prevent it.
5.  The nontrivial Dirichlet boundary condition is treated as displacement load.

The DoF identifier `(2)` may take the following.
Accepted inputs vary with the selected element type(s) and the problem type.

| identifier       | implies                                                             | of type                          |
|------------------|---------------------------------------------------------------------|----------------------------------|
| `PINNED`, `P`    | `DOF::U1`, `DOF::U2`, `DOF::U3`                                     | displacement                     |
| `ENCASTRE`, `E`  | `DOF::U1`, `DOF::U2`, `DOF::U3`, `DOF::UR1`, `DOF::UR2`, `DOF::UR3` |                                  |
| `XSYMM`, `X`     | `DOF::U1`, `DOF::UR2`, `DOF::UR3`                                   |                                  |
| `YSYMM`, `Y`     | `DOF::UR1`, `DOF::U2`, `DOF::UR3`                                   |                                  |
| `ZSYMM`, `Z`     | `DOF::UR1`, `DOF::UR2`, `DOF::U3`                                   |                                  |
| `1`, `U1`        | `DOF::U1`                                                           |                                  |
| `2`, `U2`        | `DOF::U2`                                                           |                                  |
| `3`, `U3`        | `DOF::U3`                                                           |                                  |
| `4`, `U4`, `UR1` | `DOF::UR1`                                                          |                                  |
| `5`, `U5`, `UR2` | `DOF::UR2`                                                          |                                  |
| `6`, `U6`, `UR3` | `DOF::UR3`                                                          |                                  |
| `FU1`            | `DOF::FU1`                                                          | fluid                            |
| `FU2`            | `DOF::FU2`                                                          |                                  |
| `FU3`            | `DOF::FU3`                                                          |                                  |
| `FUR1`           | `DOF::FUR1`                                                         |                                  |
| `FUR2`           | `DOF::FUR2`                                                         |                                  |
| `FUR3`           | `DOF::FUR3`                                                         |                                  |
| `RADIAL`         | `DOF::RADIAL`                                                       | axisymmetric                     |
| `AXIAL`          | `DOF::AXIAL`                                                        | axisymmetric, rod/beam like      |
| `RS`             | `DOF::RS`                                                           | beam                             |
| `RW`             | `DOF::RW`                                                           | 3D beam                          |
| `DAMAGE`         | `DOF::DAMAGE`                                                       | special damage DoF               |
| `PRESSURE`       | `DOF::PRESSURE`                                                     | special pressure DoF             |
| `TEMPERATURE`    | `DOF::TEMPERATURE`                                                  | thermal DOF                      |
| `WARP`           | `DOF::WARP`                                                         | special warp DoF (in some beams) |

