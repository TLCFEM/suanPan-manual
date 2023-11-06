# NM3D2

$$N$$-$$M$$ Interaction Inelastic Section (Linear Hardening)

## Reference

1. [10.1061/JSENDH/STENG-12176](http://dx.doi.org/10.1061/JSENDH/STENG-12176)

## Syntax

### Option One

```
section NM3D2 (1) (2...11)
# (1) int, unique section tag
# (2) double, EA
# (3) double, strong axis EI
# (4) double, weak axis EI
# (5) double, yielding axial force
# (6) double, yielding strong axis moment
# (7) double, yielding weak axis moment
# (8) double, c
# (9) double, isotropic hardening parameter H
# (10) double, kinematic hardening parameter K
# (11) double, linear density
```

The $$N$$-$$M$$ interaction surface is defined as follows.

$$
f=1.15p^2+m_s^2+m_w^4+3.67p^2m_s^2+3p^6m_w^2+4.65m_s^4m_w^2-c
$$

where $$p$$, $$m_s$$ and $$m_w$$ are normalised axial force and moments about strong and weak axes.
The surface is suitable for I-sections.

### Option Two

One may wish to customise the surface by assigning different weights and orders, it is possible by using the following
syntax.

```
section NM3D2 (1) (2...11) [(12) (13) (14) (15)...]
# (1) int, unique section tag
# (2) double, EA
# (3) double, strong axis EI
# (4) double, weak axis EI
# (5) double, yielding axial force
# (6) double, yielding strong axis moment
# (7) double, yielding weak axis moment
# (8) double, e
# (9) double, isotropic hardening parameter H
# (10) double, kinematic hardening parameter K
# (11) double, linear density
# (12) double, a_i
# (13) double, b_i
# (14) double, c_i
# (15) double, d_i
```

In the above command, parameters `(12)`, `(13)`, `(14)` and `(15)` form a set of parameters and can be appended as many
groups as analyst wishes. The surface is assumed to possess the following form,

$$
f=\sum_{i=1}^na_ip^{b_i}m_s^{c_i}m_w^{d_i}-e.
$$

For example, the previous surface $$f=1.15p^2+m_s^2+m_w^4+3.67p^2m_s^2+3p^6m_w^2+4.65m_s^4m_w^2-c$$ can be equivalently
expressed with the second syntax as follows.

```
section NM3D2 (1) (2...11) 1.15 2. 0. 0. 1. 0. 2. 0. 3.67 2. 2. 0. 3. 6. 0. 2. 4.65 0. 4. 2.
```

The only validation implemented is the number of triplets. The command takes $$4n$$ parameters and interprets them
accordingly. Please make sure the definition is correct.

## Remarks

The true hardening ratio is defined as

$$
\dfrac{H+K}{1+H+K},
$$

since $$H$$ and $$K$$ are hardening ratios based on plastic strain.

## Output Type

This model supports the following additional history variables to be recorded.

| variable label | physical meaning                 |
|----------------|----------------------------------|
| YF             | yielding flag (vector of size 2) |
