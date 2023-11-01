# NM2D2

$$N$$-$$M$$ Interaction Inelastic Section (Linear Hardening)

## Reference

1. [10.1061/JSENDH/STENG-12176](http://dx.doi.org/10.1061/JSENDH/STENG-12176)

## Syntax

### Option One

```
section NM2D2 (1) (2...9)
# (1) int, unique section tag
# (2) double, EA
# (3) double, EI
# (4) double, yielding axial force
# (5) double, yielding strong axis moment
# (6) double, c
# (7) double, isotropic hardening parameter H
# (8) double, kinematic hardening parameter K
# (9) double, linear density
```

If the `NM2D2` section is defined by using the above command, it is assumed that the $$N$$-$$M$$ interaction surface is
defined as follows.

$$
f=1.15p^2+m_s^2+3.67p^2m_s^2-c
$$

where $$p$$ and $$m_s$$ are normalised axial force and moment (about strong axis). The surface is suitable for
I-sections.

### Option Two

One may wish to customise the surface by assigning different weights and orders, it is possible by using the following
syntax.

```
section NM2D2 (1) (2...9) [(10) (11) (12) ...]
# (1) int, unique section tag
# (2) double, EA
# (3) double, EI
# (4) double, yielding axial force
# (5) double, yielding strong axis moment
# (6) double, d
# (7) double, isotropic hardening parameter H
# (8) double, kinematic hardening parameter K
# (9) double, linear density
# (10) double, a_i
# (11) double, b_i
# (12) double, c_i
```

In the above command, parameters `(10)`, `(11)` and `(12)` form a triplet and can be appended as many groups as analyst
wishes. The surface is assumed to possess the following form,

$$
f=\sum_{i=1}^na_ip^{b_i}m_s^{c_i}-d.
$$

For example, the previous surface $$f=1.15p^2+m_s^2+3.67p^2m_s^2-c$$ can be equivalently expressed with the second
syntax as follows.

```
section NM2D2 (1) (2...9) 1.15 2. 0. 1. 0. 2. 3.67 2. 2.
```

The only validation implemented is the number of triplets. The command takes $$3n$$ parameters and interprets them
accordingly. Please make sure the definition is correct.

## Remarks

The true hardening ratio is defined as

$$
\dfrac{H+K}{1+H+K},
$$

given that $$H$$ and $$K$$ are hardening ratios based on plastic strain.

## Output Type

This model supports the following additional history variables to be recorded.

| variable label | physical meaning                 |
|----------------|----------------------------------|
| YF             | yielding flag (vector of size 2) |
