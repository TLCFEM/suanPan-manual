# Overview

The `Integrator` acts as middleware between `Solver` and `Domain`.
It is mainly responsible for time integration in which the proper equation of motion can be formulated.
The `Integrator` provides an additional layer and handles the communication between the `Solver` and the `Domain`.
It can also be deemed as a broker between the two components.
A number of different operations, like formulating the global damping model, can be implemented via an `Integrator`.
Several integrators are available in the framework.

## Implicit Methods

Implicit methods utilize displacement as the primary unknown variable.
Consequently, the equation of motion is typically formulated in the following manner:

$$
\bar{\mathbf{K}}\delta\mathbf{u}=\mathbf{R}
$$

Within this formulation, $\bar{\mathbf{K}}$ represents the effective stiffness matrix.

### Newmark

Choosing the right `Integrator` depends on your specific application.
The [`Newmark`](Implicit/Newmark/Newmark.md) integrator is the most widely used method.
It is the de-facto standard in structural dynamics and requires no justification for its selection.

However, the [`Newmark`](Implicit/Newmark/Newmark.md) method is not always the best choice.
Second-order accuracy and algorithmic damping cannot coexist in this method.
It is **sensitive** to initial conditions and drops to first-order accuracy if wrong ones are assigned.
You may still use it if there are no special needs and the target system is well-behaving.

### Bathe Two-Step

The [`BatheTwoStep`](Implicit/BatheTwoStep.md) integrator provides a very cost-efficient solution if energy and momentum conservation matter.
Its computational performance is highly comparable to the Newmark integrator.
It features the same second-order accuracy along with controllable algorithmic damping.
It functions as a two-step method that alternates between a trapezoidal step and a backward Euler step.

### Generalized-$$\alpha$$

The [`GeneralizedAlpha`](Implicit/GeneralizedAlpha.md) integrator can be used to customize algorithmic damping in a single-step method.
Several other methods can be recovered by adjusting its two parameters.
It requires roughly twice as many vector operations as the [`Newmark`](Implicit/Newmark/Newmark.md) integrator because the equation of motion is satisfied within the time step.
This is not considered a severe performance issue since vector operations are inexpensive and implemented in parallel.

### GSSSS

The most general option available is the [`GSSSS`](Implicit/GSSSS.md) integrator.
Optimal performance regarding overshoot, energy dissipation, and dispersion is achieved using the **U0-V0 Optimal** scheme.

The [`GSSSS`](Implicit/GSSSS.md) integrator requires an additional iteration to synchronize the state of the system.
Consequently, its computational cost is slightly higher than that of the [`GeneralizedAlpha`](Implicit/GeneralizedAlpha.md) integrator.

### Others

There are other methods implemented as well.

## Explicit Methods

Explicit methods utilize acceleration as the primary unknown variable rather than displacement.
Consequently, the equation of motion is typically formulated in the following manner:

$$
\bar{\mathbf{M}}\delta\mathbf{a}=\mathbf{R}
$$

Within this formulation, $\bar{\mathbf{M}}$ represents the effective mass matrix.
The explicit nature of these methods stems from the fact that this matrix fundamentally excludes the future stiffness matrix $\mathbf{K}_{n+1}$.

### Central Difference (Not Available)

The explicit central difference method is frequently introduced in dynamics textbooks due to its simplicity.
The major benefit is that the stiffness matrix does not enter the left-hand side of the equation of motion.
This means factorization of the global effective matrix would only be done once under certain conditions.
This characteristic leads to very efficient solutions.

However, it is generally difficult to meet those specific conditions.
It is **not** implemented in this framework, and users are discouraged from using central difference in seismic engineering.

### Tchamwa

The [`Tchamwa`](Explicit/Tchamwa.md) integrator is a generalization of the central difference method.
It provides a first-order accurate solution featuring controllable numerical dissipation.

### Explicit Bathe Two-Step

The [explicit](Explicit/BatheExplicit.md) version of the Bathe two-step integrator is available.
It is a second-order accurate method that includes controllable numerical dissipation.

### Explicit Generalized-$$\alpha$$

The [explicit](Explicit/GeneralizedAlphaExplicit.md) version of the generalized-$$\alpha$$ integrator is also available.

### Others

There are other methods as well.

## Does Order of Accuracy Matter?

The answer to this question is complicated.

The order of accuracy is directly reflected in the numerical results for linear problems.
Choosing a method with a higher order of accuracy has a direct impact if precision matters.
In this specific case, the order of accuracy indeed matters.

It probably does not matter for nonlinear problems where nonlinear material models are involved.
The local integration is often done using the implicit Euler method in most implementations of nonlinear material models.
The implicit Euler method is only a first-order accurate method.
This local integration makes the material model the bottleneck for overall accuracy.

The results would likely not be more accurate than a first-order method even if a higher-order integrator is used.
Algorithmic damping and numerical performance are more important as a general rule for nonlinear problems.
It is worth considering a higher-order accurate integrator if the material model implementation is known to be second-order accurate.
Using a first-order accurate integrator is completely sufficient otherwise.
