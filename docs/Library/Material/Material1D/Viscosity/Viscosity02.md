# Viscosity02

Viscous Damper

This material model does not respond to strain/displacement.
To represent materials that respond to both displacement and velocity, see [`Maxwell`](Maxwell.md) and [`Kelvin`](Kelvin.md).

See also damper elements [`Damper01`](../../../Element/Special/Damper01.md) and [`Damper02`](../../../Element/Special/Damper02.md).

## References

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Theory

The quadrant damper is implemented.

The damping force is defined as a function of displacement and velocity (or strain and strain rate, depending on what the input is).

$$
\sigma=\text{sign}(\dot\varepsilon)~\eta(\varepsilon,\dot\varepsilon)~|\dot\varepsilon|^\alpha.
$$

The damping coefficient is a function of strain and strain rate that can be expressed as follows, which shows different responses in different quadrants.

$$
\begin{align*} \eta\left(\varepsilon,\dot\varepsilon\right)
&=\dfrac{\eta_1+\eta_2+\eta_3+\eta_4}{4}+\dfrac{\eta_1-\eta_2+\eta_3-\eta_4}{\pi^2}\arctan\left(g_1\varepsilon\right)
\arctan\left(g_2\dot\varepsilon\right)\\[4mm]&+\dfrac{\eta_1-\eta_2-\eta_3+\eta_4}{2\pi}\arctan\left(
g_1\varepsilon\right)+\dfrac{\eta_1+\eta_2-\eta_3-\eta_4}{2\pi}\arctan\left(g_2\dot\varepsilon\right). \end{align*}
$$

The four coefficients $$\eta_1$$ to $$\eta_4$$ are the asymptotic values of the damping coefficient in the four quadrants of the $$(\varepsilon,\dot\varepsilon)$$ plane.
When both arctangent arguments tend to $$+\pi/2$$ the expression returns $$\eta_1$$, and the signs of strain and strain rate then select $$\eta_2$$, $$\eta_3$$ or $$\eta_4$$.
The arctangent interpolation is smooth everywhere, so the model is differentiable and can be used in a Newton solver.
Both steepness factors are converted to absolute values, and the default value of $$10^3$$ makes the transitions between quadrants sharp.
The exponent $$\alpha$$ and the cut-off $$L$$ act exactly as in [`Viscosity01`](Viscosity01.md), including the cubic regularisation near zero velocity.

!!! info "deviation from theory"
    All four coefficients are converted to absolute values, so each asymptotic quadrant coefficient $$\eta_i$$ is non-negative.
    The transition between quadrants is an arctangent interpolation rather than a sharp switch.

## Syntax

```text title="Viscosity02"
material Viscosity02 (1) (2) (3) [4] [5] [6] [7] [8] [9]
# (1) int, unique tag
# (2) double, alpha
# (3) double, damping coefficient \eta_1
# [4] double, damping coefficient \eta_2, default: (3)
# [5] double, damping coefficient \eta_3, default: (3)
# [6] double, damping coefficient \eta_4, default: (3)
# [7] double, steepness factor g_1, default: 1E3
# [8] double, steepness factor g_2, default: 1E3
# [9] double, limit, default: 1.0
```

## Remarks

All four damping coefficients and both steepness factors are converted to absolute values in the constructor.
The optional coefficients `(4)` to `(6)` default to $$\eta_1$$, in which case the quadrant dependence disappears and the model reduces to [`Viscosity01`](Viscosity01.md) with the same exponent.
The steepness factors `[7]` and `[8]` default to $$10^3$$, and smaller values broaden the transition between quadrants.
The exponent `(2)` is passed to the [`NonlinearViscosity`](NonlinearViscosity.md) base class and should not be set to zero for a standalone damper.
Use an element that supplies both strain and strain rate, such as [`Damper01`](../../../Element/Special/Damper01.md) or [`Damper02`](../../../Element/Special/Damper02.md).
