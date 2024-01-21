# ElementalNonviscous

Nonviscous Elemental Damping

## Reference

1. []()

The kernel function is defined as a summation of exponential functions.

$$
g(t)=\sum_{i=1}^n m_i\exp(-s_it)
$$

The parameters $m_i$ and $s_i$ are complex numbers.

## Syntax

```text
modifier ElementalNonviscous (1) (2) ((3) (4) (5) (6)...)
# (1) int, unique modifier tag
# (2) int, element tag
# (3) double, real part of `m_i`
# (4) double, imaginary part of `m_i`
# (5) double, real part of `s_i`
# (6) double, imaginary part of `s_i`

modifier ElementalNonviscousGroup (1) (2) ((3) (4) (5) (6)...)
# (1) int, unique modifier tag
# (2) int, element group tag
# (3) double, real part of `m_i`
# (4) double, imaginary part of `m_i`
# (5) double, real part of `s_i`
# (6) double, imaginary part of `s_i`
```

## Example

```text
modifier ElementalNonviscous 1 1 8. 0 2. 0 4. 0 1. 0
```

This defines a kernel function of the following form.

$$
g(t)=8\exp(-2t)+4\exp(-t)
$$
