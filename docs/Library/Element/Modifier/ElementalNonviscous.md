# ElementalNonviscous

Nonviscous Elemental Damping

## References

1. [10.1016/j.ymssp.2024.111156](https://doi.org/10.1016/j.ymssp.2024.111156)

The kernel function is defined as a summation of exponential functions.

$$
g(t)=\sum_{i=1}^n m_i\exp(-s_it)
$$

The parameters $$m_i$$ and $$s_i$$ are complex numbers.

## Background

A nonviscous damping force is the convolution of the velocity history with a kernel, as described on the [`Modifier`](Modifier.md) page.
For an exponential kernel the convolution can be updated recursively instead of storing the whole velocity history.
With $\Delta t$ the time increment, the implementation forms the complex coefficients

$$
p_i=\dfrac{2}{\Delta t}+s_i,\qquad
s_i'=\dfrac{p_i-2s_i}{p_i},\qquad
m_i'=\dfrac{m_i}{p_i},
$$

and advances the element history force by

$$
\boldsymbol f_{d,e}^{n+1}=\boldsymbol f_{d,e}^{n}\operatorname{diag}(s')
+\big(\dot{\boldsymbol u}_e^{n}+\dot{\boldsymbol u}_e^{n+1}\big)\boldsymbol m'^{\mathrm T}.
$$

A diagonal tangent $\operatorname{Re}\big(\sum_i m_i'\big)\boldsymbol I$ is added to the element damping matrix.
Only matrix--vector products are needed, so the cost per step is low and no velocity history is stored.

!!! warning "implementation limitation"
    The added tangent is diagonal.
    Off-diagonal coupling between DoFs in the nonviscous kernel is not represented.

!!! note "developer note"
    The tangent uses only the real part of the summed coefficients.
    The convolution history is advanced with a trapezoidal combination of the current and previous velocities.

The parser requires the coefficients to form conjugate pairs and checks that the kernel decays to zero; a kernel that does not satisfy these conditions is rejected.

## Syntax

```text title="ElementalNonviscous"
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

## Remarks

1. The four coefficients are supplied in the order real and imaginary parts of $m_i$, then real and imaginary parts of $s_i$, and this group is repeated for each exponential term.
2. The imaginary parts must form conjugate pairs, and the kernel must decay to zero, otherwise the parser rejects the modifier.
3. `ElementalNonviscousGroup` takes an element group tag instead of a single element tag and applies the same kernel to all elements in that group.
4. Repeated element tags are detected at initialisation and disable the modifier, since each element can carry only one such history.
5. The modifier applies only in a dynamic analysis and only to elements that permit modification of their nonviscous force and tangent.
