# ExpGurson

See also the corresponding section in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf).

## Syntax

```
material ExpGurson (1) (2) (3) (4) (5) [6] [7] [8] [9] [10] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, yield stress
# (5) double, n
# [6] double, q1, default: 1.0
# [7] double, q2, default: 1.0
# [8] double, fn, default: 0.0
# [9] double, sn, default: 1.0
# [10] double, en, default: 0.0
# [11] double, density, default: 0.0
```

## Remarks

Due to that the yield function has the quadratic term $$q^2$$, it shall be noted that the unit of the model shall be
selected carefully. For example, if the yield stress is $$1000~\mathrm{MPa}$$ and $$\mathrm{Pascal}$$ is used as the
unit for stress, then the input number is $$10^9$$, the square of which is greater than $$10^{16}$$ so that the yield
function likely overflows.
