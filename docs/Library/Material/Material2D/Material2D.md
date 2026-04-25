# Material2D

All 2D material models support the following basic output types.

| variable label | physical meaning                                |
| -------------- | ----------------------------------------------- |
| SP             | principal stress components (plane stress only) |
| EP             | principal strain components (plane strain only) |
| S              | stress components (plane stress only)           |
| E              | strain components (plane strain only)           |
| HIST           | history vector                                  |
| YF             | yield flag                                      |

Depending on the specific material model, additional output types may be available.

!!! warning "incomplete response"
    It is difficult, if not impossible, to track the magnitudes of the out-of-plane components.
    Here, we are referring to $\sigma_{33}$ in plane strain models and $\varepsilon_{33}$ in plane stress models.
    All 2D models cannot reliably record those components and all quantities that depend on those.

The history vector is a vector of variadic length that stores the necessary history variables for the material model.
Different material models may have different history variable storage layout.

!!! warning "better to use wrapper with 3D models"
    It is discouraged to directly use 2D material models unless they are specifically designed for 2D problems.
    In all other cases, it is recommended to use wrappers that wrap around 3D models.
