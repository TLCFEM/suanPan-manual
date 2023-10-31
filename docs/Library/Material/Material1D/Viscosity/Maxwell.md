# Maxwell

Maxwell Model Using An Iterative Solving Algorithm

This material model does respond to both displacement and velocity.

## Reference

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Syntax

```
material Maxwell (1) (2) (3) [4] [5] [6]
# (1) int, unique tag
# (2) int, damper tag
# (3) int, spring tag
# [4] bool string, if to use matrix formulation, default: false
# [5] int, the maximum unconverged substep allowed, default: 1
# [6] double, local time integration parameter, default: 0.0
```

## Remarks

1. When `[4]` is set to true, the matrix formulation is used, that is, a 3-by-3 matrix is used in local iterations.
   However, the inverse of the Jacobian is not computed numerically, but analytically. When it is set to false, the
   scalar iteration is performed. In general, a scalar algorithm requires fewer floating number operations but may be
   less numerically stable.
2. The parameter `[5]` can be set to a nonzero positive integer to allow some unconverged substeps to be accumulated to
   avoid sharp transition regions that may cause numerical issues. As the result, the response may not be as smooth as
   other regions.
3. The parameter `[6]` is used to control how local strain is integrated. A value of $$0.0$$ indicates it would be
   automatically computed based on the input strain and strain rate increments. A value of $$0.5$$ indicates a linear
   distribution of spring strain over time.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning        |
|----------------|-------------------------|
| SD, SS, S      | stress                  |
| ED             | damper strain           |
| VD             | damper strain rate      |
| ES             | spring strain           | 
| VS             | spring strain rate      |
| E              | total strain            |
| V              | total strain rate       | 
| LITR           | local iteration counter | 
