# CoulombFriction

The `CoulombFriction` is a 1D viscous material that shall be used with, for example, the [`Damper01`](../../../Element/Special/Damper01.md) element.

## Syntax

```text title="CoulombFriction"
material CoulombFriction (1) (2) (3)
# (1) int, unique material tag
# (2) double, C
# (3) double, alpha
```

## Theory

The stress is constant as long as the velocity is not zero.

$$
\sigma=C\cdot\text{sign}\left(\dot\varepsilon\right)\qquad\text{if~}\dot\varepsilon\neq0.
$$

In order to avoid discontinuity, the sigmoid function is used.

$$
\sigma=\dfrac{2C}{\pi}\cdot\arctan\left(\alpha\cdot\dot\varepsilon\right).
$$

The factor $$\alpha$$ is used to control the steepness of the transition region.
The prefactor $2C/\pi$ is chosen so that the regularised law tends to the ideal force $C$ as $|\dot\varepsilon|\to\infty$.
The tangent damping is obtained by differentiation,

$$
c=\dfrac{\mathrm d\sigma}{\mathrm d\dot\varepsilon}=\dfrac{2C\alpha}{\pi\left[1+\left(\alpha\dot\varepsilon\right)^2\right]}.
$$

It is largest at zero velocity, where $c_0=2C\alpha/\pi$, and decays to zero at large velocity.
This velocity-dependent tangent is what allows the nonsmooth friction law to be used in a Newton-based finite element analysis.
In the limit $\alpha\to\infty$ the arctangent approaches the sign function and the ideal Coulomb law is recovered, at the cost of a very steep transition that may require small time steps.
In the opposite limit of small $\alpha$ the response becomes nearly linear and viscous over a broad velocity range.
Unlike a viscous dashpot, the force saturates at $C$, so the energy dissipated per cycle depends mainly on the displacement amplitude rather than on the loading frequency.

!!! warning "implementation limitation"
    There is no stick regime in this model.
    At zero velocity the regularised force is exactly zero, and the limiting value $C$ is approached only asymptotically as the velocity grows.
    A static friction threshold different from the kinetic force cannot be represented.

## Remarks

Both `(2)` and `(3)` are converted to absolute values in the constructor, so their signs do not matter.
The parameter $C$ is the limiting friction force with units of stress, or of force when the model is attached to a damper element that reports force.
The parameter $\alpha$ has units of inverse velocity and sets the velocity scale $\dot\varepsilon_c=1/\alpha$ over which the force builds up.
A typical calibration chooses $C$ from the measured sliding force and then increases $\alpha$ until the transition is sharp enough without impairing convergence.
The model ignores strain and history, so it cannot reproduce stick-slip with a static friction threshold different from the kinetic one.
It must be attached to an element that supplies strain rate, such as [`Damper01`](../../../Element/Special/Damper01.md) or [`Damper02`](../../../Element/Special/Damper02.md).
The implementation resides in the `Material/Material1D/Hysteresis` folder of the source tree but is registered by the parser under the name `CoulombFriction`.
For a friction damper with post-yield hardening use [`BilinearViscosity`](BilinearViscosity.md) instead.

## References

1. Wriggers, P. (2006), Computational Contact Mechanics, Springer, [doi:10.1007/3-540-30315-4](https://doi.org/10.1007/3-540-30315-4).
