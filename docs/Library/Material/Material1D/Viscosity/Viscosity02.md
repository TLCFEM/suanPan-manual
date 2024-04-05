# Viscosity02

Viscous Damper

This material model does not respond to strain/displacement. To represent materials that respond to both displacement
and velocity, see [`Maxwell`](Maxwell.md) and [`Kelvin`](Kelvin.md).

See also damper elements [`Damper01`](../../../Element/Special/Damper01.md)
and [`Damper02`](../../../Element/Special/Damper02.md).

## References

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Theory

The quadrant damper is implemented.

The damping force is defined as a function of displacement and velocity (or strain and strain rate, depends on what the
input is).

$$
\sigma=\text{sign}(\dot\varepsilon)~\eta(\varepsilon,\dot\varepsilon)~|\dot\varepsilon|^\alpha.
$$

The damping coefficient is a function of strain and strain rate that can be expressed as follows, which shows different
response in different quadrants.

$$
\begin{align*} \eta\left(\varepsilon,\dot\varepsilon\right)
&=\dfrac{\eta_1+\eta_2+\eta_3+\eta_4}{4}+\dfrac{\eta_1-\eta_2+\eta_3-\eta_4}{\pi^2}\arctan\left(g_1\varepsilon\right)
\arctan\left(g_2\dot\varepsilon\right)\\[4mm]&+\dfrac{\eta_1-\eta_2-\eta_3+\eta_4}{2\pi}\arctan\left(
g_1\varepsilon\right)+\dfrac{\eta_1+\eta_2-\eta_3-\eta_4}{2\pi}\arctan\left(g_2\dot\varepsilon\right). \end{align*}
$$

## Syntax

```
material Viscosity02 (1) (2) (3) [4] [5] [6] [7] [8]
# (1) int, unique tag
# (2) double, alpha
# (3) double, damping coefficient \eta_1
# [4] double, damping coefficient \eta_2, default: (3)
# [5] double, damping coefficient \eta_3, default: (3)
# [6] double, damping coefficient \eta_4, default: (3)
# [7] double, steepness factor g_1, default: 1E3
# [8] double, steepness factor g_2, default: 1E3
```
