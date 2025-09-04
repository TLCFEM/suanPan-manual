# ExpTsaiWu

Exponential Hardening Tsai-Wu Model

## References

1. [Tsai-Wu failure criterion](https://en.wikipedia.org/wiki/Tsai%E2%80%93Wu_failure_criterion)
2. [10.1016/S0045-7825(02)00605-9](https://doi.org/10.1016/S0045-7825(02)00605-9)

## Theory

The isotropic hardening rule is defined as

$$
K(\bar\varepsilon_p)=1+a(1-e^{-b\bar\varepsilon_p})
$$

## Syntax

```
material ExpTsaiWu (1) (2...7) (8...10) (11...19) (20) (21) [22]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, G_{xy}, G_{yz}, G_{zx}
# (8...10) double, three poissions ratios: v_{xy}, v_{yz}, v_{xz}
# (11...19) double, nine yield stress
# (20) double, a
# (21) double, b
# [22] double, density, default: 0.0
```
