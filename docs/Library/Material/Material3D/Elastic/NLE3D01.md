# NLE3D01

Nonlinear Elastic 3D Model

## Syntax

```
material NLE3D01 (1) (2) (3) (4) (5) [6]
# (1) int, unique material tag
# (2) double, bulk modulus
# (3) double, reference strain
# (4) double, reference stress
# (5) double, m
# [6] double, density, default: 0.0
```

## Theory

The strain energy potential is expressed as

$$
W=\dfrac{9}{2}K\varepsilon_v^2+\dfrac{\varepsilon_0\sigma_0}{1-m}\left(\dfrac{\varepsilon_p}{\varepsilon_0}\right)^{(
1-m)},
$$

where $$K$$ is the bulk modulus, $$\varepsilon_0$$ is the reference strain, $$\sigma_0$$ is the reference stress and
$$m\in[0,1]$$ is an exponent controls nonlinearity. The volumetric strain $$\varepsilon_v$$ and equivalent strain
$$\varepsilon_p$$ are expressed as

$$
\varepsilon_v=\text{trace}\left(\varepsilon\right),\qquad\varepsilon_p=\sqrt{\dfrac{2}{3}\varepsilon_d:
\varepsilon_d}.
$$
