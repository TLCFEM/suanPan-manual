# NM3D3

$$N$$-$$M$$ Interaction Inelastic Section (Nonlinear Hardening)

## References

1. [10.1061/JSENDH.STENG-12176](http://dx.doi.org/10.1061/JSENDH.STENG-12176)

## Syntax

```text
section NM3D3 (1) (2...14) [(15) (16) (17) (18)...]
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
# (12) double, kinematic hardening modulus, K_b
# (13) double, kinematic hardening base, K_a
# (14) double, linear density
# (15) double, a_i
# (16) double, b_i
# (17) double, c_i
# (18) double, d_i
```

In the above command, parameters `(15)`, `(16)`, `(17)` and `(18)` form a set and can be appended as many groups as the
analyst wishes.
The surface is assumed to possess the following form,

$$
f=\sum_{i=1}^na_ip^{b_i}m_s^{c_i}m_w^{d_i}-e.
$$

For example, the surface $$f=1.15p^2+m_s^2+m_w^4+3.67p^2m_s^2+3p^6m_w^2+4.65m_s^4m_w^2-c$$ can be expressed as follows.

```
section NM3D3 (1) (2...14) \
1.15 2. 0. 0. \
1. 0. 2. 0. \
1. 0. 0. 4. \
3.67 2. 2. 0. \
3. 6. 0. 2. \
4.65 0. 4. 2.
```

The only validation implemented is the number of triplets.
The command takes $$4n$$ parameters and interprets them accordingly.
Please make sure the definition is correct.
