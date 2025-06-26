# Overview

The `Integrator` is some middleware between `Solver` (in charge of solving the system) and `Domain` (in charge of
managing the state of the system). It is mainly responsible for time integration in which the proper equation of motion
can be formulated. To fulfill this task, the `Integrator` provides an additional layer and handles the communication
between the `Solver` and the `Domain`, thus, it can also be deemed as a broker between the two. Due to this fact, a
number of different (special) operations, for example, formulating the global damping model, can also be implemented via
an `Integrator`. A number of integrators are implemented.

## Implicit Methods

### Newmark

But how can one determine which `Integrator` to use?
The most widely used integrator is (probably) the [`Newmark`](Implicit/Newmark/Newmark.md) integrator.
Indeed, it is almost the de-facto method to use it in structural dynamics, and there is no need to justify the choice.

But the [`Newmark`](Implicit/Newmark/Newmark.md) method is not always the best choice.
The second-order accuracy and algorithmic damping cannot coexist in the Newmark method.
And it is sensitive to initial conditions, if wrong ones are assigned, it can at most be first-order accurate.
If there are no special needs and the target system is 'well-behaving', one may still use the Newmark method.

### Bathe Two-Step

If energy and momentum conservations matter, the [`BatheTwoStep`](Implicit/BatheTwoStep.md) integrator provides a very cost-efficient solution.
The performance should be comparable to the Newmark integrator.
It has the same second-order accuracy and controllable algorithmic damping.
It is effectively a two-step method, and it alternates between a trapezoidal step and a backward Euler step.

### Generalized-$$\alpha$$

If one wants to customise algorithmic damping in a single step method, the [`GeneralizedAlpha`](Implicit/GeneralizedAlpha.md) integrator can be used.
By adjusting two parameters, several other methods can be recovered.
Since the equation of motion is satisfied somewhere within the time step (rather than the beginning/ending), it requires roughly a factor of two more **vector** operations than the [`Newmark`](Implicit/Newmark/Newmark.md) integrator.
However, vector operations are not costly and are mostly implemented in a parallel fashion, it is not considered a severe performance issue.

### GSSSS

The most general integrator is the [`GSSSS`](Implicit/GSSSS.md) integrator.
The optimal performance (in terms of overshoot, energy dissipation/dispersion) can be achieved by using the **U0-V0 Optimal** scheme.

The [`GSSSS`](Implicit/GSSSS.md) integrator requires an additional iteration to synchronise the state of the system.
Thus, the performance is sightly higher than that of the [`GeneralizedAlpha`](Implicit/GeneralizedAlpha.md) integrator.

## Explicit Methods

### Central Difference (Not Available)

The explicit central difference method is frequently introduced in textbooks on dynamics due to its simplicity.
The major benefit(s) is that the stiffness matrix does not enter the left-hand side of the equation of motion, which means, under certain conditions, factorisation of global effective matrix would only be done once.
This leads to "very efficient" solutions.

However, it is in general difficult to meet those conditions.
It is **not** implemented, and users are discouraged from using central difference in seismic engineering.


### Tchamwa

The [`Tchamwa`](Explicit/Tchamwa.md) integrator is a generalization of the central difference method.
It provides a first-order accurate solution with controllable numerical dissipation.


### Explicit Bathe Two-Step

The [explicit](Explicit/BatheExplicit.md) version of the Bathe two-step integrator is available.
It is a second-order accurate method with controllable numerical dissipation.

### Explicit Generalized-$$\alpha$$

The [explicit](Explicit/GeneralizedAlphaExplicit.md) version of the generalized-$$\alpha$$ integrator is also available.

## Does Order of Accuracy Matter?

It is complicated.

For linear problems, the order of accuracy can be directly reflected in the numerical results.
If accuracy matters, choosing a method that possesses higher order of accuracy would have a direct impact on the results.
In this case, it indeed matters.

For nonlinear problems in which nonlinear material models are involved, it probably does not matter.
The reason is that, in most implementations of nonlinear material models, particularly those following the conventional return mapping algorithm, the local integration is often done using the implicit Euler method, which is a first-order accurate method.
This makes the material model the bottleneck of the accuracy.

It is thus very likely that even if a higher-order accurate integrator is used, the results would not be more accurate than those obtained using a first-order accurate method.
To summarise, as a general rule, for nonlinear problems, algorithmic damping and numerical performance are more important.
If the implementation of the material model is known to be second-order accurate, then it is worth considering a higher-order accurate integrator.
Otherwise, using a first-order accurate integrator is sufficient.
