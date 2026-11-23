# NonlinearHill

Orthotropic Hill Material

This is a wrapper of the [`NonlinearHoffman`](NonlinearHoffman.md) material model.
The two share the same implementation; `NonlinearHill` simply assigns equal tensile and compressive strength in each principal direction.

!!! warning "availability of the command token"
    Neither `NonlinearHill` nor `NonlinearHoffman` is registered as a command token, so a `material NonlinearHill ...` command cannot create this model.
    The formulas below describe the model behaviour and may require a custom module or a parser update to be used.

## Background

The Hoffman criterion admits different yield stresses in tension and compression.
Setting $$\sigma_{ii}^t=\sigma_{ii}^c$$ for $$i=1,~2,~3$$ removes its linear terms and recovers the original Hill criterion.
`NonlinearHill` applies this reduction internally: it passes each of the three normal strengths as a paired tensile/compressive value to the Hoffman projection, followed by the three shear strengths.
The nine strengths are thus passed as $\sigma_1,\sigma_1,\sigma_2,\sigma_2,\sigma_3,\sigma_3,\sigma_{12},\sigma_{23},\sigma_{13}$.

!!! note "developer note"
    For equal tensile and compressive strengths the Hoffman and Hill quadratic forms coincide.
    The paired strengths are passed through the Hoffman projection rather than a dedicated Hill projection routine.

## Remarks

The yield criterion, parameter order, hardening requirements and history layout are identical to those of [`NonlinearHoffman`](NonlinearHoffman.md).
Use `NonlinearHoffman` instead when the material shows strength asymmetry between tension and compression.
The material axes can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper and the model is intended for 3D solid elements such as [`C3D8`](../../../Element/Cube/C3D8.md).
