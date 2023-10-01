# NonviscousNewmark

Newmark Time Integration With Nonviscous Damping

## Syntax

```
integrator NonviscousNewmark (1) (2) (3) ((4) (5) (6) (7)...)
# (1) int, unique tag
# (2) double, alpha, typical: 0.25
# (3) double, beta, typical: 0.5
# (4-7) double, real and imaginary parts of m and s
```

## Theory

The parameters $$m$$ and $$s$$ are two complex numbers that define the kernel function.

$$
g(t)=\sum_{i=1}^nm_ie^{-s_it}.
$$

For example, if the kernel contains two exponential functions such that

$$
g(t)=(1+9i)e^{-(2+8i)t}+(3+7i)e^{-(4+6i)t},
$$

then the command shall be defined as

```text
integrator NonviscousNewmark 1 .25 .5 1 9 2 8 3 7 4 6
```

It is assumed that the kernel is applied to all DoFs in the system.
