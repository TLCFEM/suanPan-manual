# NonlinearHill

Orthotropic Hill Material

This is a wrapper of the [`NonlinearHoffman`](NonlinearHoffman.md) material model.
The two share the same implementation; `NonlinearHill` simply assigns equal tensile and compressive strength in each principal direction.

## Background

The Hoffman criterion admits different yield stresses in tension and compression.
Setting $$\sigma_{ii}^t=\sigma_{ii}^c$$ for $$i=1,~2,~3$$ removes its linear terms and recovers the original Hill criterion.
`NonlinearHill` applies this reduction internally: it passes each of the three normal strengths as a paired tensile/compressive value to the Hoffman projection, followed by the three shear strengths.

## Remarks

The yield criterion, parameter order, hardening requirements and history layout are identical to those of [`NonlinearHoffman`](NonlinearHoffman.md).
Use `NonlinearHoffman` instead when the material shows strength asymmetry between tension and compression.
