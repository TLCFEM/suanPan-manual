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

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning   |
|----------------|--------------------|
| S              | total stress       |
| E              | total strain       |
| V              | total strain rate  | 
| SD             | damper stress      |
| ED             | damper strain      |
| VD             | damper strain rate |
| SS             | spring stress      |
| ES             | spring strain      | 
| VS             | spring strain rate |
