# Nonviscous01

Uniaxial Nonviscous Damping Material

## References

1. [10.1016/j.ymssp.2024.111156](https://doi.org/10.1016/j.ymssp.2024.111156)

The kernel function is defined as a summation of exponential functions.

$$
g(t)=\sum_{i=1}^n m_i\exp(-s_it)
$$

The parameters $$m_i$$ and $$s_i$$ are complex numbers.

## Syntax

```text
material Nonviscous01 (1) ((2) (3) (4) (5)...)
# (1) int, unique material tag
# (2) double, real part of `m_i`
# (3) double, imaginary part of `m_i`
# (4) double, real part of `s_i`
# (5) double, imaginary part of `s_i`
```

## Example

```text
material Nonviscous01 2 8. 0 2. 0 4. 0 1. 0
```

This defines a kernel function of the following form.

$$
g(t)=8\exp(-2t)+4\exp(-t)
$$
