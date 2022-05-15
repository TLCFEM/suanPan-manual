# BilinearHoffman

Bilinear Hardening Hoffman Model

## Syntax

```
material BilinearHoffman (1) (2...7) (8...10) (11...19) [20] [21]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, E_{xy}, E_{yz}, E_{zx}
# (8...10) double, three poissions ratios: v_{xx}, v_{yy}, v_{zz}
# (11...19) double, nine yield stress
# [20] double, hardening ratio, default: 0.0
# [21] double, density, default: 0.0
```
