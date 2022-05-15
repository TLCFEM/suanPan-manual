# RayleighNewmark

Newmark Algorithm With Rayleigh Damping Model

The `RayleighNewmark` integrator is simply a wrapper of the `Newmark` integrator with Rayleigh model implemented on
global level.

**For the moment, MPC cannot be considered in all global damping models.**

```
# valid starting from version 2.x
integrator RayleighNewmark (1) (2) (3) (4) (5) (6) (7)
# (1) int, unique tag
# (2) double, alpha (beta in some references) in Newmark method, normally 0.25
# (3) double, beta (gamma in some references) in Newmark method, normally 0.5
# (4) double, alpha
# (5) double, beta
# (6) double, theta
# (7) double, eta
```

## Theory

By default, the Rayleigh type damping model is used. No matter what other damping modifiers are defined, this integrator
always set the element damping matrix to be

$$
C=\alpha{}M+\beta{}K_C+\theta{}K_I+\eta{}K_T
$$

by the `Rayleigh` modifier in addition to the existing damping matrix defined in the element. In the above formulation,
$$K_C$$ is the current converged stiffness, $$K_I$$ is the initial stiffness of the element, $$K_T$$ is the trial
stiffness of current iteration. Please note if $$K_T$$ is involved, the damping force is then a function of trial
displacement. The quadratic convergence rate is lost then.
