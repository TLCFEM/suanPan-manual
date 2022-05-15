# BilinearPeric

Bilinear Peric Viscous Plasticity Model

## Theory

The rate of plasticity multiplier is defined as

$$
\dot{\gamma}=\dfrac{1}{\mu}\left(\dfrac{q}{\sigma_y}-1\right)^{\dfrac{1}{\epsilon}}
$$

where $$\epsilon$$ and $$\mu$$ are two material constants, $$\sigma_y$$ is the initial yield stress,
$$q=\sqrt{\dfrac{3}{2}s:s}=\sqrt{3J_2}$$ is the von Mises stress.

The yielding surface is identical to that of the von Mises model.

## Syntax

```
material BilinearPeric (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, yield stress
# (5) double, hardening modulus
# (6) double, mu
# (7) double, epsilon
# [8] double, density, default: 0.0
```
