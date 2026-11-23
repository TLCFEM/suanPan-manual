# initial

The `initial` command defines initial conditions for nodes, material models and other objects.

## Syntax

For nodal properties:

```text title="initial"
initial displacement (1) (2) [3...]
initial velocity (1) (2) [3...]
initial acceleration (1) (2) [3...]
# (1) double, magnitude
# (2) int, dof
# [3...] int, node tags
```

For material properties:

```text title="initial"
initial material history (1) [2...]
# (1) int, material model tag
# [2...] double, initial history vector
```

## Short Forms

The keywords `disp`, `vel` and `acc` are short forms of `displacement`, `velocity` and `acceleration` respectively.

The `angularvelocity` (or `avel`) keyword initialises a rigid-body rotation about a reference node.

```text title="initial"
initial angularvelocity (1) (2) [3...]
initial avel (1) (2) [3...]
# (1) double, three components of the angular velocity vector
# (2) int, reference node tag
# [3...] int, tags of nodes whose initial velocities are set
```

The velocity assigned to each listed node is the cross product of the angular velocity vector and the node position relative to the reference node.

## Remarks

Proper initial nodal conditions are important for dynamic analysis.
Some time integration algorithms are sensitive to initial conditions.
For example, if a standard sinusoidal wave is used as excitation, its initial displacement and acceleration are zero, so nothing needs to be changed.
Its initial velocity, however, must be unity.
If it is not set to unity, the results may oscillate.

Some material models support user-defined initial history variables.
This can be useful when modelling, for example, rolled or annealed metal.
Different material models may store history variables in different layouts.
Please refer to the specific model for details.
