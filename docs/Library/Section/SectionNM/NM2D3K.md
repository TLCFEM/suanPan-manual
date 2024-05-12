# NM2D3K

$$N$$-$$M$$ Interaction Inelastic Section (Nonlinear Hardening)

## References

1. [10.1061/JSENDH.STENG-12176](http://dx.doi.org/10.1061/JSENDH.STENG-12176)

## Syntax

```text
section NM2D3K (1) (2...14) [(15) (16) (17) ...]
# (1) int, unique section tag
# (2) double, EA
# (3) double, EI
# (4) double, yielding axial force
# (5) double, yielding strong axis moment
# (6) double, d
# (7) double, isotropic hardening modulus, H
# (8) double, isotropic hardening saturation, s
# (9) double, isotropic hardening decay, m
# (10) double, kinematic hardening modulus for axial force, K_b
# (11) double, kinematic hardening modulus for strong axis moment, K_b
# (12) double, kinematic hardening base for axial force, K_a
# (13) double, kinematic hardening base for strong axis moment, K_a
# (14) double, linear density
# (15) double, a_i
# (16) double, b_i
# (17) double, c_i
```

This model implements the hardening rule defined in the appendix of the reference.
