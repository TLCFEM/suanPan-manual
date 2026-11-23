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

This model is a concrete implementation of the abstract [`NonlinearGurson`](NonlinearGurson.md) family.
It supplies the matrix yield stress and its derivative from a table instead of an analytical expression or an [Expression](../../../../Collection/Define/expression.md) object.
The table is loaded as raw ASCII text and must contain at least two columns.
The first column is the equivalent plastic strain and the second column is the matrix yield stress.
For a strain inside the table the implementation returns the linearly interpolated stress together with the slope of the current segment.

!!! warning "implementation limitation"
    Beyond the last row the implementation returns the last strain coordinate as the yield stress and uses a slope of $$10^{-12}$$.
    The stress is not extrapolated from the second column, so the tabulated range must cover all expected plastic strain.

These two values enter the yield function and the Newton Jacobian of the coupled return mapping.
The void evolution and all other aspects of the response are inherited from [`NonlinearGurson`](NonlinearGurson.md).

## Remarks

The table named by `(4)` is a plain text file with two columns: equivalent plastic strain first, yield stress second.
Linear interpolation between adjacent rows supplies both $$\sigma_y$$ and its derivative with respect to plastic strain, which the return mapping requires.
As in the uniaxial model, a zero $$f_N$$ with a zero initial void fraction reduces the response to ordinary von Mises plasticity.
There is no initial void fraction parameter, so set `initial_history(1)` with the `initial material history` command when a nonzero initial porosity is needed.
Keep the table sorted by increasing plastic strain, since the lookup stops at the first row whose strain exceeds the current value.
A fine spacing near the yield stress improves the accuracy of the piecewise-constant slope.
For an analytical curve use [`ExpGurson`](ExpGurson.md), and for an expression-defined curve use [`CustomGurson`](CustomGurson.md).
Use a three-dimensional solid element such as `C3D8` with this material.

## References

1. A. L. Gurson, Continuum theory of ductile rupture by void nucleation and growth, Part I: yield criteria and flow rules for porous ductile media, *Journal of Engineering Materials and Technology* 99 (1977) 2--15, [doi:10.1115/1.3443401](https://doi.org/10.1115/1.3443401).
2. V. Tvergaard and A. Needleman, Analysis of the cup-cone fracture in a round tensile bar, *Acta Metallurgica* 32 (1984) 157--169, [doi:10.1016/0001-6160(84)90213-X](https://doi.org/10.1016/0001-6160(84)90213-X).
