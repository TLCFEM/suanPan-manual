# Overview

## Per Step Configurations

As mentioned in [Structure](../../Basic/Structure.md), the commands used between two steps belong to the first step.
It means the following.

```text
# first step of duration 4.0
step static 1 4.0

# anything defined here belongs to the first step 
# including convergers, integrators, solvers, solver settings, etc.

# second step of duration 4.0
step static 2 4.0

# anything defined here belongs to the first step 
# including convergers, integrators, solvers, solver settings, etc.

# maybe more steps
step static 3 4.0
```

Similar to ABAQUS, one can use different settings for different steps.
For example, for the following snippet,

```text
# first step of duration 4.0
step static 1 4.0

set ini_step_size .1
set fixed_step_size true

converger RelIncreDisp 1 1E-10 3 1

# second step of duration 4.0
step static 2 4.0

set ini_step_size 1.0
set fixed_step_size false

converger AbsIncreDisp 2 1E-8 10 1
```

one can interpret the above as follows.

1. Step 1
    1. Use an initial step size of $$0.1$$.
    2. Fix the step size to $$0.1$$. Since the duration is $$4.0$$, the total number of substeps is $$40$$.
    3. Use a relative displacement increment [RelIncreDisp](../../Library/Converger/Relative/RelIncreDisp.md) converger
       with a tolerance of $$10^{-10}$$.
2. Step 2
    1. Use an initial step size of $$1.0$$.
    2. Allow the step size to vary. The algorithm would automatically adjust the step size to satisfy the convergence
       criteria.
    3. Use an absolute displacement increment [AbsIncreDisp](../../Library/Converger/Absolute/AbsIncreDisp.md) converger
       with a tolerance of $$10^{-8}$$.

## Inheriting from Previous Steps

For convergers, integrators and solvers, if there are no corresponding objects defined in the current step, the objects
of the previous step are inherited if the previous step defines them, otherwise default ones will be used.

```text
# first step of duration 4.0
step static 1 4.0

# a valid converger is defined in the first step
converger RelIncreDisp 1 1E-10 3 1

# second step of duration 4.0
step static 2 4.0

# some other settings
```

Since there is no converger defined in the second step, the converger defined in the first step will be used in the
second step.

```text
# first step of duration 4.0
step static 1 4.0

# second step of duration 4.0
step static 2 4.0

# a valid converger is defined in the second step
converger RelIncreDisp 1 1E-10 3 1
```

For the above, since there is no converger defined in the first step, the default converger will be used in the first
step. The converger defined in the second step will not affect the first step.

!!! Warning
    The solver settings are not inherited. They must be defined in each step.
    This is because if two steps use the same solver settings, it's likely that it is possible to combine two steps into
    one step. If two steps are intended, it is likely that the solver settings are different.
