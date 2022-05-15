# PolyElastic1D

Polynomial Based Uniaxial Nonlinear Elastic

## Syntax

```
material PolyElastic1D (1) [(2)...]
# (1) int, unique material tag
# (2) double, polynomial parameters, a_n
```

## Theory

The stress response is defined as a polynomial function of strain on the positive strain ($$\varepsilon>0$$).

$$
\sigma=a_1\varepsilon+a_2\varepsilon^2+a_3\varepsilon^3\cdots
$$

The response is always an odd function so that

$$
\sigma\left(\varepsilon\right)=-\sigma\left(-\varepsilon\right)
$$

For example, if one wants to define

$$
\sigma=4\varepsilon+6\varepsilon^2+2\varepsilon^3,
$$

the following command shall be used.

```
material PolyElastic1D 1 4. 6. 2.
```

Please note density is not supported in this model.