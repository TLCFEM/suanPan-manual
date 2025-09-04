# CustomHoffman

Hoffman Model With Custom Isotropic Hardening

## Syntax

```
material CustomHoffman (1) (2...7) (8...10) (11...19) (20) [21]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, G_{xy}, G_{yz}, G_{zx}
# (8...10) double, three poissions ratios: v_{xy}, v_{yz}, v_{xz}
# (11...19) double, nine yield stress
# (20) int, isotropic hardening expression tag
# [21] double, density, default: 0.0
```

***The expressions shall be able to compute derivatives.***
