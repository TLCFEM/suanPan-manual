# CustomGurson1D

Uniaxial Gurson porous plasticity model with a user-defined hardening law.

## Syntax

```text title="CustomGurson1D"
material CustomGurson1D (1) (2) (3) (4) [5] [6] [7] [8] [9] [10]
# (1) int, unique material tag
# (2) int, expression tag
# (3) double, elastic modulus
# (4) double, Poisson's ratio
# [5] double, q1, default: 1.0
# [6] double, q2, default: 1.0
# [7] double, fn, default: 0.0
# [8] double, sn, default: 1.0
# [9] double, en, default: 0.0
# [10] double, density, default: 0.0
```

## Background

The `CustomGurson1D` model describes ductile failure by void growth and nucleation in a von Mises matrix.
Its yield function is

$$
F=\sigma^2+2q_1f\sigma_y^2\cosh\left(\dfrac{q_2}{2}\dfrac{\sigma}{\sigma_y}\right)-\sigma_y^2\left(q_1^2f^2+1\right)=0,
$$

where $$f$$ is the void volume fraction and $$\sigma_y$$ the current matrix yield stress.
The constants $$q_1$$ and $$q_2$$ scale the void contribution, $$f_N$$ is the total volume fraction of nucleating voids, and $$s_N$$ and $$\varepsilon_N$$ are the standard deviation and mean strain of the normal nucleation distribution.

The void fraction evolves by growth of existing voids and by strain-controlled nucleation,

$$
\Delta f=(1-f)\Delta\varepsilon_v^p+\dfrac{f_N}{s_N\sqrt{2\pi}}\exp\left[-\dfrac{1}{2}\left(\dfrac{\varepsilon_m^p-\varepsilon_N}{s_N}\right)^2\right]\Delta\varepsilon_m^p,
$$

where $$\varepsilon_m^p$$ is the matrix equivalent plastic strain.
The associated flow rule, the work-equivalence relation for $$\varepsilon_m^p$$ and the full implicit residual system are given in [`NonlinearGurson1D`](NonlinearGurson1D.md).
This model differs from [`ExpGurson1D`](ExpGurson1D.md) only in the way the pair $$(\sigma_y,\mathrm{d}\sigma_y/\mathrm{d}\varepsilon_m^p)$$ is obtained.

!!! warning "implementation limitation"
    The assigned expression must return exactly two values, the yield stress and its derivative with respect to the matrix equivalent plastic strain.
    There is no void coalescence term and no automatic fracture or element-deletion criterion.
    The void fraction is clamped to $$[0,1]$$ during the return mapping, and the $$f^2$$ coefficient is fixed to $$q_1^2$$.

## Remarks

The expression assigned by `(2)` takes the equivalent plastic strain as its only input and returns two outputs: the yield stress $$\sigma_y$$ and its derivative $$\mathrm{d}\sigma_y/\mathrm{d}\varepsilon^p$$.
The void fraction evolves through both growth of existing voids and strain-controlled nucleation.
With the default $$f_N=0$$ and a zero initial void fraction, no voids nucleate or grow and the response reduces to ordinary von Mises plasticity; a nonzero initial void fraction can be given with the [`initial`](../../../../Collection/Define/initial.md) `material history` command.

The expression tag `(2)` must refer to a vector-valued expression with one input and two outputs, returning the yield stress and its derivative in that order.
The expression is looked up during initialisation, so it must be defined before the material is first used.
The derivative must be supplied by the expression itself, since the return mapping does not approximate it.
The default parameters are $$E=200$$, $$\nu=0.3$$, $$q_1=1$$, $$q_2=1$$, $$f_N=0$$, $$s_N=1$$, $$\varepsilon_N=0$$ and zero density.
The void fraction is clamped to $$[0,1]$$ during iteration and can be recorded with the `VF` output type.
There is no void coalescence or automatic element deletion, so failure must be interpreted from the recorded void fraction.

## References

1. [10.1115/1.3443401](https://doi.org/10.1115/1.3443401)
2. [10.1016/0001-6160(84)90213-X](https://doi.org/10.1016/0001-6160(84)90213-X)
