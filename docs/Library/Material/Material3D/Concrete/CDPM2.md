# CDPM2

CDPM2 model for concrete model.

## Reference

1. [10.1016/j.ijsolstr.2013.07.008](https://doi.org/10.1016/j.ijsolstr.2013.07.008)
2. [10.1016/j.ijsolstr.2005.05.038](https://doi.org/10.1016/j.ijsolstr.2005.05.038)

## Remarks

1. The Lode angle dependency is removed for simplicity.
2. The isotropic damage is implemented.
3. The anisotropic damage is implemented.
4. For detailed explanations of parameters, please refer to
   Reference [1](https://doi.org/10.1016/j.ijsolstr.2013.07.008).
5. The default `CDPM2` uses isotropic damage.
6. The token `CDPM2ANISO` uses anisotropic damage.
7. If damage is activated, both tension and compression use exponential damage model, the degradation is controlled by
   parameters [14] and [15]. The characteristic length can be accounted for by modifying [14].

Details of implementation can be seen in the corresponding section
in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf)

## Syntax

```text
material CDPM2 (1) [2-16]
material CDPM2NO (1) [2-16]
material CDPM2ISO (1) [2-16]
material CDPM2ANISO (1) [2-16]
# (1) int, unique material tag
# [2] double, elastic modulus, default: 3E4
# [3] double, poissons ratio, default: 0.3
# [4] double, tension strength (positive), default: 3.0
# [5] double, compression strength (positive), default: 10.0
# [6] double, q_h0, initial hardening factor, default: 0.3
# [7] double, h_p hardening ratio, default: .01
# [8] double, d_f, default: .85
# [9] double, a_h, hardening related parameter, default: 0.08
# [10] double, b_h, hardening related parameter, default: 0.003
# [11] double, c_h, hardening related parameter, default: 2.0
# [12] double, d_h, hardening related parameter, default: 1E-6
# [13] double, a_s, ductility related parameter, default: 5.0
# [14] double, e_ft, tension softening parameter, default: 2E-4
# [15] double, e_fc, compression softening parameter, default: 1E-4
# [16] double, density, default: 0.0
```
