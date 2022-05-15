# Modulated

The `Modulated` amplitude defines the following functions.

$$
A(t)=A_0\Pi_{i=1}^{n}\sin(2\pi\omega_i{}(t-t_0))\quad\text{for}\quad{}t>t_0.
$$

In the above definition, $$t_0$$ is the (pseudo) start time of the step in which the amplitude is defined, $$\omega_i$$
is the circular frequency.

## Syntax

```
amplitude Modulated (1) (2) (3) [(4)...]
# (1) int, unique tag
# (2) double, base amplitude A_0
# (3) double, first frequency \omega_0
# [(4)...] double, optional frequencies for higher modes
```
