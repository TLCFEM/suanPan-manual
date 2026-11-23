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

```text title="Nonviscous01"
material Nonviscous01 (1) ((2) (3) (4) (5)...)
# (1) int, unique material tag
# (2) double, real part of `m_i`
# (3) double, imaginary part of `m_i`
# (4) double, real part of `s_i`
# (5) double, imaginary part of `s_i`
```

## Theory

This material implements the nonviscous damping algorithm proposed in the reference.
As of writing, the referenced algorithm is probably the most efficient algorithm for nonviscous damping as there is no explicit integration of the convolution integral.

For arbitrary kernel functions $$g(t)$$, the damping force $$F_d$$ is given by

$$
F_d(t)=\int_0^t{}g(t-\tau)\dot{u}(\tau)\mathrm{d}\tau.
$$

The proposed algorithm converts the above convolution integral into a summation of differential equations.
By further operations, the algorithm modifies the existing damping force (viscous damping, or zero if there is no damping other than the nonviscous damping) and the corresponding damping matrix to achieve the best accuracy and computational efficiency.

Details can be seen in the referenced paper.

By defining a uniaxial material model, it can be used in 1D analyses with damper elements.

For the exponential kernel used here each complex pole $s_i$ contributes an internal state that is updated recursively.
With a step size $\Delta t$ the implementation forms

$$
t_i=2+\Delta t\,s_i,\qquad
p_i=\dfrac{4-t_i}{t_i}=\dfrac{2-\Delta t\,s_i}{2+\Delta t\,s_i},\qquad
q_i=\dfrac{\Delta t\,m_i}{t_i},
$$

and advances a complex internal variable $z_i$ according to

$$
z_{i,n+1}=z_{i,n}p_i+q_i\left(\dot u_n+\dot u_{n+1}\right),
$$

so that the damping force is

$$
F_{d,n+1}=\operatorname{Re}\left(\sum_i z_{i,n+1}\right).
$$

The factor $p_i$ has modulus below one for a decaying kernel, which makes the recursion stable.
The tangent damping returned to the element is $\operatorname{Re}\sum_i q_i$, and its initial value depends on the initial step size through $\operatorname{Re}\sum_i \Delta t_0 m_i/(2+\Delta t_0 s_i)$.
A viscous dashpot corresponds to the distributional limit $g(t)=\eta\,\delta(t)$, so the exponential-kernel representation generalises [`Viscosity01`](Viscosity01.md).

!!! warning "implementation limitation"
    The kernel is restricted to a finite sum of complex exponentials, so a general kernel has to be fitted by such a sum before use.
    The recursion is a trapezoidal-type discretisation of the convolution integral rather than an exact integration.
    Both the tangent damping and the initial damping depend on the time step, so changing the step size changes the apparent damping.

## Remarks

The parameters are supplied in groups of four, namely the real and imaginary parts of $m_i$ followed by the real and imaginary parts of $s_i$.
The imaginary parts may be set to zero to obtain a purely real exponential kernel, as in the example below.
The real parts of the decay parameters $s_i$ should be positive so that the kernel fades with time.
The number of terms controls both the accuracy of the kernel approximation and the cost of each step.
The material depends only on strain rate and ignores strain, like the other dashpots in this section.
Because the tangent damping depends on the step size through $\Delta t$, large changes in time step change the apparent damping.
Use an element that supplies strain rate, such as [`Damper01`](../../../Element/Special/Damper01.md) or [`Damper02`](../../../Element/Special/Damper02.md).

## Example

```text
material Nonviscous01 2 8. 0 2. 0 4. 0 1. 0
```

This defines a kernel function of the following form.

$$
g(t)=8\exp(-2t)+4\exp(-t)
$$
