# TimberPD

Timber Plastic-Damage Model

## Reference

1. [10.1016/j.compstruc.2017.09.010](https://doi.org/10.1016/j.compstruc.2017.09.010)

## Syntax

```
material TimberPD (1) (2...7) (8...10) (11...19) (20) (21) (22) (23) (24) (25) (26) [27]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, E_{xy}, E_{yz}, E_{zx}
# (8...10) double, three poissions ratios: v_{xy}, v_{yz}, v_{zx}
# (11...19) double, nine yield stress
# (20) double, h
# (21) double, r_t^0
# (22) double, n_t
# (23) double, b_t
# (24) double, r_c^0
# (25) double, m_c
# (26) double, b_c
# [27] double, density, default: 0.0
```

## Remarks

1. The yield stress shall be arranged in the following order: $$\sigma_{11}^t$$, $$\sigma_{11}^c$$, $$\sigma_{22}^t$$,
    $$\sigma_{22}^c$$, $$\sigma_{33}^t$$, $$\sigma_{33}^c$$, $$\sigma_{12}^0$$, $$\sigma_{23}^0$$, $$\sigma_{13}^0$$.
2. The original paper documents a comprehensive procedure to determine hardening parameter $$h$$.

The damage evolutions are identical to the original formulation but with different notations.

### Tension Damage Evolution

$$
\omega_t=1-\dfrac{r_t^0}{r_t}\left(1-n_t+n_t\exp{b_t\left(r_t^0-r_t\right)}\right)
$$

### Compression Damage Evolution

$$
\omega_c=b_c\left(1-\dfrac{r_c^0}{r_c}\right)^{m_c}
$$
