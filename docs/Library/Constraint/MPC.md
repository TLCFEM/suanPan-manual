# MPC

The Lagrange multiplier method can be used to define constraints. Extra storage is required for the so-called auxiliary
bordered stiffness matrix. The constraint is satisfied exactly.

Although the `MPC` object belongs to the `Constraint` class, it behaves like a `Load` object. Hence, a
proper `Amplitude` object is required to be present. If `0` is assigned to `[2]`, a default ramp function will be
assigned automatically.

**Users are not expected to assign boundary conditions via `MPC` constraint or `Tie` element.**

## Syntax

```
mpc (1) (2) (3) [(4) (5) (6))...]
# (1) int, unique constraint tag
# (2) int, amplitude tag, can be zero
# (3) double, right hand side of the constraint equation, the constraint is homogeneous if this parameter is zero
# (4) int, node tag
# (5) int, dof tag
# (6) double, weight
```