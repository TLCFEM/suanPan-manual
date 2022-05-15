# LinearDamage

Linear Damage Degradation With Cut-offs

## Syntax

```
material LinearDamage (1) (2) (3) (4) [5]
# (1) int, unique material tag
# (2) int, associated material tag
# (3) double, start strain
# (4) double, end strain
# [5] double, end damage value, default: 0.0
```

## Theory

In this model, the equivalent total strain is used to characterize the damage development, namely, $$d=f(\varepsilon_
{eq})$$. Then the final response is defined as

$$
\mathbf\sigma=d\mathbf{\bar\sigma},
$$

where $$\mathbf{\bar\sigma}$$ is the intact stress response of the associated material model.

The final stiffness can be derived as

$$
\mathbf{K}=\dfrac{\mathrm{d}\mathbf{\sigma}}{\mathrm{d}\mathbf{\varepsilon}}=\dfrac{\mathrm{d}\mathbf{\bar\sigma}}{\mathrm{d}\mathbf{\varepsilon}}d+\mathbf{\bar\sigma}\otimes\dfrac{\mathrm{d}d}{\mathrm{d}\mathbf{\varepsilon}}=\mathbf{\bar{K}}d+\mathbf{\bar\sigma}\otimes\dfrac{\mathrm{d}d}{\mathrm{d}\mathbf{\varepsilon}}.
$$
