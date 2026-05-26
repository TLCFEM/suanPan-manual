# UDNewmark

Newmark Time Integration With Uniform/Universal Damping

## References

1. [10.1016/j.compstruc.2018.10.016](https://doi.org/10.1016/j.compstruc.2018.10.016)

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

$$
\left\{\begin{array}{l}
\mathbf{M}\ddot{\mathbf{u}}+\mathbf{K}\mathbf{u}+\sum\mathbf{f}_j=\mathbf{0},\\
\dot{\mathbf{f}}_j=-s_j\mathbf{f}_j+m_j\mathbf{y}.
\end{array}\right.
$$

* For `UDDNewmark`, $$\mathbf{y=Ku}$$. The real part of $$m_j$$ shall be negative.
* For `UDANewmark`, $$\mathbf{y=M\ddot{u}}$$. The real part of $$m_j$$ shall be positive.

The specific damping factor as defined in [10.1016/j.compstruc.2018.10.016](https://doi.org/10.1016/j.compstruc.2018.10.016) can be expressed as

$$
\zeta(\omega)=-\sum\dfrac{m_j\omega}{s_j^2+\omega^2}.
$$

## Remarks

Two forms `UDDNewmark` and `UDANewmark` are equivalent if only hysteretic and inertial actions exist.
The following function converts from one to another.

```py
import numpy as np

class Damping:
    def __init__(self, m, s):
        m_tmp = np.asarray(m, dtype=np.complex128)
        s_tmp = np.asarray(s, dtype=np.complex128)
        self.m = m_tmp[idx := np.argsort(s_tmp)]
        self.s = s_tmp[idx]

    def pair(self):
        return np.real_if_close(self.m), np.real_if_close(self.s)

    def convert(self):
        scalar = 1 + np.sum(self.m)

        poles, ev = np.linalg.eig(
            np.diag(self.s) * scalar - np.outer(self.m, self.s)
        )

        ev = ev[:, idx := np.argsort(poles)]
        poles = poles[idx]

        return Damping(
            self.s @ ev * np.linalg.solve(ev, self.m) / (-scalar * poles),
            poles / scalar,
        )

    @staticmethod
    def map(m, s):
        m = np.asarray(m, dtype=np.complex128)
        s = np.asarray(s, dtype=np.complex128)
        m, s = Damping(-m / s, s).convert().pair()
        return -m * s, s

print(Damping.map([-2], [10])) # UDD -> UDA
```

Since `UDANewmark` applies to inertial terms, if the mass matrix is constant and/or lumped, it will be more performant than `UDDNewmark`, which is typically computationally more costly.
