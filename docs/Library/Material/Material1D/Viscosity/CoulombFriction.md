# CoulombFriction

The `CoulombFriction` is a 1D viscous material that shall be used with for
example [`Damper01`](../../../Element/Special/Damper01.md) element.

## Syntax

```
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