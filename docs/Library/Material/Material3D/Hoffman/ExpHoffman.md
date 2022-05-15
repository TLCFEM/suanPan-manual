# ExpHoffman

Exponential Hardening Hoffman Model

## Theory

The isotropic hardening rule is defined as

$$
K(\bar\varepsilon_p)=1+a(1-e^{-b\bar\varepsilon_p})
$$

## Syntax

```
material ExpHoffman (1) (2...7) (8...10) (11...19) (20) (21) [22]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, E_{xy}, E_{yz}, E_{zx}
# (9...10) double, three poissions ratios: v_{xx}, v_{yy}, v_{zz}
# (11...19) double, nine yield stress
# (20) double, a
# (21) double, b
# [22] double, density, default: 0.0
```
