# PolyElastic1D

Polynomial Based Uniaxial Nonlinear Elastic

## Syntax

```text title="PolyElastic1D"
material PolyElastic1D (1) [(2)...]
# (1) int, unique material tag
# (2) double, polynomial parameters, a_n
```

## Theory

The stress response is defined as a polynomial function of strain for positive strain ($$\varepsilon>0$$).

$$
\sigma=a_1\varepsilon+a_2\varepsilon^2+a_3\varepsilon^3\cdots
$$

The response is always an odd function so that

$$
\sigma\left(\varepsilon\right)=-\sigma\left(-\varepsilon\right)
$$

Writing the coefficients as $$a_1,a_2,\dots,a_m$$, the implementation evaluates the odd extension

$$
\sigma(\varepsilon)=\operatorname{sign}(\varepsilon)\sum_{i=1}^{m}a_i|\varepsilon|^i,
$$

so that even powers also contribute an odd and continuous backbone.

!!! info "deviation from theory"
    A power term with even $$i$$ is not the ordinary polynomial $$a_i\varepsilon^i$$ but $$a_i\operatorname{sign}(\varepsilon)|\varepsilon|^i$$.
    Thus the coefficient $$a_2$$ contributes $$a_2\varepsilon|\varepsilon|$$ and not $$a_2\varepsilon^2$$.

!!! note "developer note"
    The odd extension is obtained by forming all powers of $$|\varepsilon|$$ and negating the accumulated stress when the strain is negative.

The consistent tangent stiffness is

$$
E_T(\varepsilon)=\sum_{i=1}^{m} i\,a_i\,|\varepsilon|^{i-1},
$$

which is continuous and even in $$\varepsilon$$, with $$E_T(0)=a_1$$.
The initial stiffness is therefore set to the first coefficient $$a_1$$.

For example, if one wants to define

$$
\sigma=4\varepsilon+6\varepsilon^2+2\varepsilon^3,
$$

the following command shall be used.

```
material PolyElastic1D 1 4. 6. 2.
```

Please note density is not supported in this model.

!!! warning "implementation limitation"
    Every numeric argument after the tag is treated as a polynomial coefficient, and the density is fixed at zero.
    There is no way to supply a density through this command, so the model cannot contribute mass in a dynamic analysis.

!!! note "developer note"
    `new_polyelastic1d` hard-codes the density to zero and forwards every remaining token as a polynomial coefficient.

## Remarks

The coefficients are passed as a list of doubles and are used without conversion to absolute values.
The first coefficient is the initial stiffness, so a positive $$a_1$$ is needed for a stable initial response.
Even-power coefficients introduce a curvature discontinuity at the origin even though the stress and the tangent remain continuous.
The model is path independent and has no history variables, but it does not support a density argument.
High-order polynomials can oscillate strongly outside the fitted strain range and should be used with caution.
For a bounded backbone use [`Tanh1D`](Tanh1D.md), and for a polynomial with an independent stiffness parameter use [`CustomElastic1D`](CustomElastic1D.md).
