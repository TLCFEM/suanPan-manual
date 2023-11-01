# NM2D3

$$N$$-$$M$$ Interaction Inelastic Section (Nonlinear Hardening)

## Reference

1. [10.1061/JSENDH/STENG-12176](http://dx.doi.org/10.1061/JSENDH/STENG-12176)

## Syntax

```text
section NM2D3 (1) (2...12) [(13) (14) (15) ...]
# (1) int, unique section tag
# (2) double, EA
# (3) double, EI
# (4) double, yielding axial force
# (5) double, yielding strong axis moment
# (6) double, d
# (7) double, isotropic hardening modulus, H
# (8) double, isotropic hardening saturation, s
# (9) double, isotropic hardening decay, m
# (10) double, kinematic hardening modulus, K_b
# (11) double, kinematic hardening base, K_a
# (12) double, linear density
# (13) double, a_i
# (14) double, b_i
# (15) double, c_i
```

In the above command, parameters `(13)`, `(14)` and `(15)` form a triplet and can be appended as many groups as analyst
wishes. The surface is assumed to possess the following form,

$$
f=\sum_{i=1}^na_ip^{b_i}m_s^{c_i}-d.
$$

For example, the surface $$f=1.15p^2+m_s^2+3.67p^2m_s^2-c$$ can be expressed as follows.

```
section NM2D3 (1) (2...12) 1.15 2. 0. 1. 0. 2. 3.67 2. 2.
```

The only validation implemented is the number of triplets. The command takes $$3n$$ parameters and interprets them
accordingly. Please make sure the definition is correct.