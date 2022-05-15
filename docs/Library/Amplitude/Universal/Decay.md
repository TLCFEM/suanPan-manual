# Decay

The `Decay` amplitude uses a decaying exponential function.

$$
A(t)=A_0\exp(-\dfrac{t-t_o}{t_d})\quad\text{for}\quad{}t>t_0.
$$

## Syntax

```
amplitude Decay (1) (2) (3)
# (1) int, unique amplitude tag
# (2) double, initial amplitude A_0
# (3) double, speed control parameter t_d
```