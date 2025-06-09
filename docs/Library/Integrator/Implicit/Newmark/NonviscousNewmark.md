# NonviscousNewmark

Newmark Time Integration With Nonviscous Damping

## References

1. [10.1016/j.ymssp.2024.111156](https://doi.org/10.1016/j.ymssp.2024.111156)

## Syntax

```
integrator NonviscousNewmark (1) (2) (3) ((4) (5) (6) (7)...)
# (1) int, unique tag
# (2) double, alpha, typical: 0.25
# (3) double, beta, typical: 0.5
# (4) double, real part of `m_i`
# (5) double, imaginary part of `m_i`
# (6) double, real part of `s_i`
# (7) double, imaginary part of `s_i`
```

## Theory

The parameters $$m_i$$ and $$s_i$$ are two complex numbers that define the kernel function.

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

As of writing, the referenced algorithm is probably the most efficient algorithm for nonviscous damping as there is no explicit integration of the convolution integral.
