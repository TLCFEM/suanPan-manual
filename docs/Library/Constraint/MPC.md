# MPC

General Multiple Point Constraint

The Lagrange multiplier method can be used to define constraints.
Extra storage is required for the so-called auxiliary bordered stiffness matrix.
The constraint is satisfied exactly.

Although the `MPC` object belongs to the `Constraint` class, it behaves like a `Load` object.
Hence, a proper `Amplitude` object is required to be present.
If `0` is assigned to `(2)`, a default ramp function will be assigned automatically.

!!! warning "no bc"
    It is not expected to assign boundary conditions via `MPC` constraint or `Tie` element.


The `MPC` is a general-purpose constraint that enforces the following condition:

$$
\sum\omega_iu_i=A,
$$

where $$u_i$$ are target displacements (designated by node tag and DoF token), $$\omega_i$$ are the corresponding weights and $$A$$ is the magnitude that is controlled by the attached `Amplitude`.

## Syntax

```text title="MPC"
mpc (1) (2) (3) [(4) (5) (6)...]
constraint mpc (1) (2) (3) [(4) (5) (6)...]
# (1) int, unique constraint tag
# (2) int, amplitude tag, can be zero
# (3) double, right hand side of the constraint equation, the constraint is homogeneous if this parameter is zero
# (4) int, node tag
# (5) string, dof token
# (6) double, weight
```

For example, to enforce identical displacement between `U1` of node `101` and `U2` of node `102`, one can use the following definition.

```text
constraint mpc 1 0 0. 101 u1 1. 102 u2 -1,
```