# Linear/Ramp

The `Linear` amplitude increases proportionally with time so that

$$
A(t)=V\langle{}t-t_0\rangle\quad\text{for}\quad{}t>t_0.
$$

The `Ramp` amplitude is in fact a simplified version with unit slope. It adopts unit time length no matter what the
current step is and remains unity after that.

$$
A(t)=\left\{\begin{array}{rl}\langle{}t-t_0\rangle,&t<t_0+1,\\1,&t\ge{}t_0+1.\end{array}\right.
$$

The `Ramp` amplitude is the default amplitude that would be used if no valid amplitude is defined.

## Syntax

```
amplitutde Linear (1) (2)
# (1) int, unique amplitude tag
# (2) double, slope V

amplitude Ramp (1)
# (1) int, unique amplitude tag
```

The `Ramp` amplitude would look like this.

<iframe src="https://www.desmos.com/calculator/7nb8pjfljr?embed" width="500" height="500" style="border: 1px solid #ccc" frameborder=0></iframe>
