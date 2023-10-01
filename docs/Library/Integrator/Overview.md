# Overview

The `Integrator` is some middleware between `Solver` (in charge of solving the system) and `Domain` (in charge of
managing the state of the system). It is mainly responsible for time integration in which the proper equation of motion
can be formulated. To fulfill this task, the `Integrator` provides an additional layer and handles the communication
between the `Solver` and the `Domain`, thus, it can also be deemed as a broker between the two. Due to this fact, a
number of different (special) operations, for example, formulating the global damping model, can also be implemented via
an `Integrator`. A number of integrators are implemented.

## Newmark

But how can one determine which `Integrator` to use? The most widely used integrator is (probably)
the [`Newmark`](Newmark/Newmark.md) integrator. Indeed, it is almost the standard practice to use it in earthquake
engineering, and there is no need to justify the choice. But the [`Newmark`](Newmark/Newmark.md) method is not always
the best choice.

## Bathe Two--Step

If energy and momentum conservations matter, the [`BatheTwoStep`](BatheTwoStep.md) integrator provides a very
cost-efficient solution. The performance should be comparable to the [`Newmark`](Newmark/Newmark.md) integrator.

## Generalized-$$\alpha$$

If one wants to customise algorithmic damping, the [`GeneralizedAlpha`](GeneralizedAlpha.md) integrator can be used. By
adjusting two parameters, several other methods can be recovered. Since the equation of motion is satisfied somewhere
within the time step (rather than the beginning/ending), it requires roughly a factor of two more **vector** operations
than the [`Newmark`](Newmark/Newmark.md) integrator. However, vector operations are not costly and are mostly
implemented in a parallel fashion, it is not considered a severe performance issue.

## GSSSS

The most general integrator is the [`GSSSS`](GSSSS.md) integrator. The optimal performance (in terms of overshoot,
energy dissipation/dispersion) can be achieved by using the **U0-V0 Optimal** scheme.

The [`GSSSS`](GSSSS.md) integrator requires an additional iteration to synchronise the state of the system. Thus, the
performance is sightly higher than that of the [`GeneralizedAlpha`](GeneralizedAlpha.md) integrator.

## Central Difference (Not Available)

The explicit central difference method is frequently introduced in textbooks on dynamics due to its simplicity. The
major benefit(s) is that the stiffness matrix does not enter the left-hand side of the equation of motion, which means,
under certain conditions, factorisation of global effective matrix would only be done once. This leads to "very
efficient" solutions.

However, it is in general difficult to meet those conditions. It is **not** implemented, and users are discouraged from
using central difference in seismic engineering.

#### Constant Mass and Damping Matrices

The mass matrix may be constant, but there is no guarantee that the damping matrix is constant. Thus, in the nonlinear
context, it can only be assumed that the left-hand side of the equation of motion would change in each sub-step.

#### Convergence

To ensure convergence, the time step should be very small, and should reduce further if the mesh is refined. The maximum
allowable time step is associated with the minimum period of all elements. If the mass matrix is not fully integrated (
semi-positive definite), the time step would be unnecessarily small.
