# NonlinearHill

Orthotropic Hill Material

This is a wrapper of the [`NonlinearHoffman`](NonlinearHoffman.md) material model.
The two share the same implementation; `NonlinearHill` simply assigns equal tensile and compressive strength in each principal direction.

!!! warning "availability of the command token"
    The C++ class `NonlinearHill` exists in `NonlinearOrthotropic.h`, but the current `MaterialParser.cpp` registers neither `NonlinearHill` nor `NonlinearHoffman`.
    A `material NonlinearHill ...` command therefore cannot create this model in a build that uses the stock parser.
    The formulas below describe the class-level behaviour and may require a custom module or a parser update to be used.

## Background

The Hoffman criterion admits different yield stresses in tension and compression.
Setting $$\sigma_{ii}^t=\sigma_{ii}^c$$ for $$i=1,~2,~3$$ removes its linear terms and recovers the original Hill criterion.
`NonlinearHill` applies this reduction internally: it passes each of the three normal strengths as a paired tensile/compressive value to the Hoffman projection, followed by the three shear strengths.
The nine strengths are thus passed as $\sigma_1,\sigma_1,\sigma_2,\sigma_2,\sigma_3,\sigma_3,\sigma_{12},\sigma_{23},\sigma_{13}$.

!!! info "deviation from theory"
    The implementation passes the paired strengths through the Hoffman projection instead of calling the dedicated Hill projection routine.
    For equal tensile and compressive strengths the two quadratic forms coincide, so the numerical result is unchanged.

## Remarks

The yield criterion, parameter order, hardening requirements and history layout are identical to those of [`NonlinearHoffman`](NonlinearHoffman.md).
Use `NonlinearHoffman` instead when the material shows strength asymmetry between tension and compression.
The material axes can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper and the model is intended for 3D solid elements such as [`C3D8`](../../../Element/Cube/C3D8.md).
