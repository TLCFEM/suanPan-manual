# NM3D3K

$$N$$-$$M$$ Interaction Inelastic Section (Nonlinear Hardening)

## References

1. [10.1061/JSENDH.STENG-12176](http://dx.doi.org/10.1061/JSENDH.STENG-12176)

## Syntax

```text
section NM3D3K (1) (2...18) [(19) (20) (21) (22)...]
# (1) int, unique section tag
# (2) double, EA
# (3) double, strong axis EI
# (4) double, weak axis EI
# (5) double, yielding axial force
# (6) double, yielding strong axis moment
# (7) double, yielding weak axis moment
# (8) double, e
# (9) double, isotropic hardening modulus, H
# (10) double, isotropic hardening saturation, s
# (11) double, isotropic hardening decay, m
# (12) double, kinematic hardening modulus for axial force, K_b
# (13) double, kinematic hardening modulus for strong axis moment, K_b
# (14) double, kinematic hardening modulus for weak axis moment, K_b
# (15) double, kinematic hardening base for axial force, K_a
# (16) double, kinematic hardening base for strong axis moment, K_a
# (17) double, kinematic hardening base for weak axis moment, K_a
# (18) double, linear density
# (19) double, a_i
# (20) double, b_i
# (21) double, c_i
# (22) double, d_i
```

This model implements the hardening rule defined in the appendix of the reference.


