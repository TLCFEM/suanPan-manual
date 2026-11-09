# Balloon1D

Uniaxial Balloon Model

Both this model and [Balloon3D](../../Material3D/vonMises/Balloon.md) share the same definitions of parameters.
Both models shall yield the same uniaxial behaviour if the same parameter set is used.

## References

1. [10.31224/6937](https://doi.org/10.31224/6937)

## Syntax

```text title="Balloon1D"
material Balloon1D (1) (2...24) (25) [(26) (27) (28)...]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, k_r
# (4) double, load reversal memory size
# (5 6 7 8) double, u bound, initial, linear, saturation, rate
# (9 10 11 12) double, fm bound, initial, linear, saturation, rate
# (13 14 15 16) double, fc bound, initial, linear, saturation, rate
# (17 18 19 20) double, am bound, initial, linear, saturation, rate
# (21 22 23 24) double, ac bound, initial, linear, saturation, rate
# (25) double, density
# (26) string, token, one of '-fc', '-ac', '-na', '-nd', '-memory'
# (27 28) double, saturation and rate, omitted for '-memory'
```

## Theory

See [Balloon3D](../../Material3D/vonMises/Balloon.md) for more details.
