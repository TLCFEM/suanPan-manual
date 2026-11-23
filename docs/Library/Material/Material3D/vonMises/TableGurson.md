# TableGurson

Three-dimensional Gurson porous plasticity model with a tabulated hardening law.

## Syntax

```text title="TableGurson"
material TableGurson (1) (2) (3) (4) (5) (6) (7) (8) (9) [10]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) string, table file name
# (5) double, q1
# (6) double, q2
# (7) double, fn
# (8) double, sn
# (9) double, en
# [10] double, density, default: 0.0
```

## Background

The `TableGurson` model extends von Mises plasticity with a void volume fraction $$f$$ that introduces hydrostatic stress sensitivity and softening.
Its yield function is

$$
F=q^2+2q_1f\sigma_y^2\cosh\left(\dfrac{3q_2p}{2\sigma_y}\right)-\sigma_y^2\left(q_1^2f^2+1\right)=0,
$$

where $$p$$ is the hydrostatic stress, $$q$$ the von Mises equivalent stress and $$\sigma_y$$ the matrix yield stress.
The five Gurson constants have the same meaning as in [`CustomGurson1D`](../../Material1D/vonMises/CustomGurson1D.md): $$q_1$$ and $$q_2$$ scale the void growth term, while $$f_N$$, $$s_N$$ and $$\varepsilon_N$$ define the strain-controlled void nucleation distribution.

## Remarks

The table named by `(4)` is a plain text file with two columns: equivalent plastic strain first, yield stress second.
Linear interpolation between adjacent rows supplies both $$\sigma_y$$ and its derivative with respect to plastic strain, which the return mapping requires.
As in the uniaxial model, a zero $$f_N$$ with a zero initial void fraction reduces the response to ordinary von Mises plasticity.
