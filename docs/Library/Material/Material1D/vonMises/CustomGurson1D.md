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

## Remarks

The expression assigned by `(2)` takes the equivalent plastic strain as its only input and returns two outputs: the yield stress $$\sigma_y$$ and its derivative $$\mathrm{d}\sigma_y/\mathrm{d}\varepsilon^p$$.
The void fraction evolves through both growth of existing voids and strain-controlled nucleation.
With the default $$f_N=0$$ and a zero initial void fraction, no voids nucleate or grow and the response reduces to ordinary von Mises plasticity; a nonzero initial void fraction can be given with the [`initial`](../../../../Collection/Define/initial.md) `material history` command.
