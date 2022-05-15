# Kelvin

Kelvin Model

The `Kelvin` model represents a dashpot and a spring in parallel. This material model does respond to both displacement
and velocity.

## Syntax

```
material Kelvin (1) (2) (3)
# (1) int, unique material tag
# (2) int, damper tag
# (3) int, spring tag
```

## Remarks

1. Elements that pass both strain and strain rate to material models shall be used.
