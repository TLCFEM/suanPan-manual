# initial

The `initial` command can be used to define initial conditions for nodes, material models, etc.

## Syntax

For nodal properties:

```
initial displacement (1) (2) [3...]
initial velocity (1) (2) [3...]
initial acceleration (1) (2) [3...]
# (1) double, magnitude
# (2) int, dof
# [3...] int, node tags
```

For material properties:

```
initial history (1) [2...]
# (1) int, material model tag
# [2...] double, initial history vector
```

## Remarks

Proper initial nodal conditions are important for dynamic analysis. Some time integration algorithms are sensitive to
initial conditions. For example, if a standard sinusoidal wave is used as excitation, its initial displacement and
acceleration are zeros so nothing needs to be changed. However, its initial velocity shall be unity, if it is not set to
unity, the results may oscillate.

Some material models supports user-defined initial history variables. It could be useful when it comes to model for
example rolled/annealed metal. Different material models may have different layout of storage of history variables.
Please refer to the specific model for details.
