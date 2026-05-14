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

Two forms `UDDNewmark` and `UDANewmark` are equivalent.
The following function converts from one to another.

```py
import numpy as np


def inverse(m, s):
    """
    Compute transformed modal weights and poles from a rank-one updated diagonal matrix.

    Parameters
    ----------
    m : array_like, shape (n,)
        Input modal weights. Converted to `np.complex128`.
    s : array_like, shape (n,)
        Input poles. Converted to `np.complex128`.

    Returns
    -------
    rm : np.ndarray, shape (n,), dtype=complex128
        Transformed modal weights.
    rs : np.ndarray, shape (n,), dtype=complex128
        Transformed poles.
    """
    m = np.asarray(m, dtype=np.complex128)
    ones = np.ones_like(m)

    A = np.diag(np.asarray(s, dtype=np.complex128)) + np.outer(m, ones)

    ar, R = np.linalg.eig(A)
    al, L = np.linalg.eig(A.T)

    rs = ar[idx := np.argsort(ar)]
    R = R[:, idx]
    L = L[:, np.argsort(al)]

    rm = np.zeros_like(rs)
    for k in range(rm.size):
        rm[k] = -(ones @ R[:, k]) * (L[:, k] @ m) / (L[:, k] @ R[:, k])

    return rm, rs
```

Since `UDANewmark` applies to inertial terms, if the mass matrix is constant and/or lumped, it will be more performant than `UDDNewmark`, which is typically computationally more costly.
