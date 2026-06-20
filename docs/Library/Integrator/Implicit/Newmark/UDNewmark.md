# UDNewmark

Newmark Time Integration With Uniform/Universal Damping

## References

1. [10.1016/j.compstruc.2018.10.016](https://doi.org/10.1016/j.compstruc.2018.10.016)
2. [todo: to be added]()

## Syntax

```
integrator UDDNewmark (1) (2) (3) ((4) (5) (6) (7)...)
integrator UDANewmark (1) (2) (3) ((4) (5) (6) (7)...)
# (1) int, unique tag
# (2) double, alpha, typical: 0.25
# (3) double, beta, typical: 0.5
# (4) double, real part of `m_i`
# (5) double, imaginary part of `m_i`
# (6) double, real part of `s_i`
# (7) double, imaginary part of `s_i`
```

## Theory

The parameters $$m_j$$ and $$s_j$$ are two complex numbers that define the kernel function.

$$
g(t)=\sum_{j=1}^nm_je^{-s_jt}.
$$

For example, if the kernel contains two exponential functions such that

$$
g(t)=(1+9i)e^{-(2+8i)t}+(3+7i)e^{-(4+6i)t},
$$

then the command shall be defined as

```text
integrator UDDNewmark 1 .25 .5 1 9 2 8 3 7 4 6
```

It is assumed that the kernel is applied to all DoFs in the system.

These parameters contribute to the energy dissipation action in the system.
Assuming free vibration and no velocity related forces, the equation of motion can be expressed as follows.

$$
\left\{\begin{array}{l}
\mathbf{M}\ddot{\mathbf{u}}+\mathbf{K}\mathbf{u}+\sum\mathbf{f}_j+\cdots=\mathbf{0},\\
\dot{\mathbf{f}}_j=-s_j\mathbf{f}_j+m_j\mathbf{y}.
\end{array}\right.
$$

* For `UDDNewmark`, $$\mathbf{y=Ku}$$. The real part of $$m_j$$ shall be negative.
* For `UDANewmark`, $$\mathbf{y=M\ddot{u}}$$. The real part of $$m_j$$ shall be positive.

Using the paremeter set for `UDDNewmark`, the specific damping factor as defined in [10.1016/j.compstruc.2018.10.016](https://doi.org/10.1016/j.compstruc.2018.10.016) can be expressed as

$$
\zeta(\omega)=-\sum\dfrac{m_j\omega}{s_j^2+\omega^2}.
$$

One can customize the specific damping curve using various numerical methods.

## Remarks

Two forms `UDDNewmark` and `UDANewmark` are equivalent if only hysteretic and inertial actions exist.
The following function converts from one to another.

```py
import numpy as np


def map(m, s):
    """
    Transform damping coefficients between UDD and UDA.
    """
    m, s = np.asarray(m, np.complex128), np.asarray(s, np.complex128)

    scalar = 1 - np.sum(ms := m / s)
    poles, ev = np.linalg.eig(np.diag(s) * scalar + np.outer(ms, s))

    ev = ev[:, idx := np.argsort(poles)]
    poles = poles[idx]

    ms = s @ ev * np.linalg.solve(ev, ms) / (-scalar * poles)
    s = poles / scalar

    return ms * s, s


print(map([-2], [10])) # UDD -> UDA
```
