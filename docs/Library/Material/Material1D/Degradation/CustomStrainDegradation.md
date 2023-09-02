# CustomStrainDegradation

Strain History Based Degradation With Custom Rules

This model implements the [universal damage model](Degradation.md) assuming the degradation factor depends on
the strain history.

## Syntax

```
material CustomStrainDegradation (1) (2) (3) [4]
# (1) int, unique material tag
# (2) int, host intact material tag
# (3) int, tension degradation expression tag
# [4] int, compression degradation expression tag, default: (3)
```

## Usage

The usage of `CustomStrainDegradation` is identical to [`CustomStressDegradation`](CustomStressDegradation.md).

The degradations for positive/negative strains are defined separately.

$$
D_{pos}=D_{pos}(\varepsilon_{max}),\quad
D_{neg}=D_{neg}(\varepsilon_{min}).
$$

In which $$\varepsilon_{max}$$ is the maximum strain (positive) of the whole loading history,
and $$\varepsilon_{min}$$ is the minimum strain (negative) of the whole loading history.
