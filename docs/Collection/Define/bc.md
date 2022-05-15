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

1. Both `fix` and `fix2` serve the same purpose but with different approaches. The `fix` command modifies the
   corresponding main diagonal term by multiplying a large number, for example $$10^8$$. The `fix2` command erase the
   column and row of target DoF and set the main diagonal to unity. In both case, the corresponding right hand side
   entry is erased.
2. The `fix` and `penaltybc` commands is computationally efficient but leads to an ill-conditioned matrix. This may not
   be a problem for direct solvers but will greatly affect the performance of iterative solvers. The penalty number can
   be controlled by [`set`](../Process/set.md) command via `constraint_multiplier` option.
3. The `fix2` and `multiplierbc` commands requires more operations but the final matrix is well conditioned.
4. The performance difference is almost negligible. Either one can be used with direct solvers. The error won't
   accumulate as there is a special mechanism to prevent it.
5. The DoF identifier `(2)` takes the following string input: `1`, `2`, `3`, `4`, `5`, `6`, `pinned`, `encastre`
   , `xsymm`, `ysymm`, `zsymm` and the corresponding initials `p`, `e`, `x`, `y`, `z`. The names do not actually reflect
   their meaning, instead, following DoFs would be restrained when string input is given.
  1. `pinned`: 1 2 3
  2. `encastre`: 1 2 3 4 5 6
  3. `xsymm`: 1 5 6
  4. `ysymm`: 2 4 6
  5. `zsymm`: 3 4 5
6. The nontrivial Dirichlet boundary condition is treated as displacement load.
