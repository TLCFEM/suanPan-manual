# Viscosity01

Viscous Damper

The damping force is defined as a function of velocity (or strain rate, depends on what the input is). This material
model does not respond to strain/displacement. To represent materials that respond to both displacement and velocity,
see [`Maxwell`](Maxwell.md) and [`Kelvin`](Kelvin.md).

See this [example](../../../../Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md).

See also damper elements [`Damper01`](../../../Element/Special/Damper01.md)
and [`Damper02`](../../../Element/Special/Damper02.md).

$$
\sigma=\text{sign}(\dot\varepsilon)~\eta~|\dot\varepsilon|^\alpha.
$$

The damping coefficient is constant.

## Syntax

```
material Viscosity01 (1) (2) (3)
# (1) int, unique tag
# (2) double, alpha
# (3) double, damping coefficient
```
