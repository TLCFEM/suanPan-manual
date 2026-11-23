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
    Here, we are referring to $$\sigma_{33}$$ in plane strain models and $$\varepsilon_{33}$$ in plane stress models.
    All 2D models cannot reliably record those components and all quantities that depend on those.

The history vector is a vector of variadic length that stores the necessary history variables for the material model.
Different material models may have different history variable storage layouts.

!!! warning "better to use wrapper with 3D models"
    It is discouraged to directly use 2D material models unless they are specifically designed for 2D problems.
    In all other cases, it is recommended to use wrappers that wrap around 3D models.

## Background

A two-dimensional material receives a three-component strain vector and returns a three-component stress vector.
The components are ordered as $$(\varepsilon_{11},\varepsilon_{22},\gamma_{12})$$ and $$(\sigma_{11},\sigma_{22},\tau_{12})$$, where $$\gamma_{12}=2\varepsilon_{12}$$ is the engineering shear strain and $$\tau_{12}=\sigma_{12}$$ is the shear stress.
Using engineering shear makes the stiffness matrix symmetric for isotropic linear elasticity and allows the same Voigt notation as the six-component 3D case.

Three reduction assumptions are used in suanPan.
Under plane stress, $$\sigma_{33}=\tau_{23}=\tau_{13}=0$$ and $$\varepsilon_{33}$$ is a dependent quantity, so the stress vector is complete but the out-of-plane strain is not recorded.
Under plane strain, $$\varepsilon_{33}=\gamma_{23}=\gamma_{13}=0$$ and $$\sigma_{33}$$ is a dependent quantity, so the strain vector is complete but the out-of-plane stress is not recorded unless the material reconstructs it explicitly, as [`Elastic2D`](Elastic2D.md) does for `MISES` and `S` output.
Under axisymmetry, the vector is $$(\varepsilon_{rr},\varepsilon_{\theta\theta},\varepsilon_{zz},\gamma_{rz})$$ and may contain four entries, as in [`AxisymmetricElastic`](AxisymmetricElastic.md), and the element must generate the hoop strain $$u_r/r$$.

The base class tags each material with a `PlaneType`, namely `S` for plane stress, `E` for plane strain, `A` for axisymmetry and `N` for models that are not tied to either in-plane assumption.
The tag controls which derived output quantities the base class can produce: `S` and `SP` are available for `PlaneType::S`, while `E` and `EP` are available for `PlaneType::E`.
Models tagged `N`, such as [`Concrete21`](Concrete21.md) and [`Concrete22`](Concrete22.md), do not receive automatic stress or strain output from the base class.
`HIST` returns the current history vector and `YF` returns one if any history entry is non-zero, which means `YF` is a history-activity flag rather than a strict yield indicator.

!!! info "deviation from theory"
    `YF` is computed by testing whether any entry of the history vector differs from zero.
    It is not the value of a yield function and can be one for a model that has only an accumulated-strain history variable.

A 2D material is updated by `update_trial_status(strain)`, committed by `commit_status()`, restored by `reset_status()` and reinitialised by `clear_status()`.
Nonlinear models perform a local iteration inside `update_trial_status` and return the algorithmic (consistent) tangent in `trial_stiffness`, because the global Newton iteration converges quadratically only if the tangent is differentiated consistently with the local update.
For example, [`DuncanSelig`](DuncanSelig.md) solves a local Newton system with line search and obtains its tangent from the same Jacobian, while [`Concrete21`](Concrete21.md) rotates the principal stiffness back to global axes.

The recommended way to use a three-dimensional law in a two-dimensional analysis is a wrapper rather than a native 2D model.
The [`PlaneStress`](../Wrapper/PlaneStress.md), [`PlaneStrain`](../Wrapper/PlaneStrain.md) and [`Axisymmetric`](../Wrapper/Axisymmetric.md) wrappers embed a 3D material, enforce the appropriate constraints on the full six-component strain vector and return the corresponding stress and stiffness submatrix.
This preserves the out-of-plane state inside the 3D material, which is essential for pressure-dependent or path-dependent models such as the Cam-Clay family.
Native 2D models should be reserved for formulations that are genuinely two-dimensional, such as the smeared crack models or the Duncan--Selig hyperbolic soil model.

!!! warning "implementation limitation"
    A native 2D model cannot recover the out-of-plane component once it has been eliminated from the strain vector.
    Quantities that depend on $$\sigma_{33}$$ in plane strain or on $$\varepsilon_{33}$$ in plane stress are therefore unavailable or reconstructed approximately.

Use membrane elements from the [CP4](../../Element/Membrane/Plane/CP4.md) and [CP8](../../Element/Membrane/Plane/CP8.md) families for plane problems, and [CAX4](../../Element/Membrane/Axisymmetric/CAX4.md) or [CAX8](../../Element/Membrane/Axisymmetric/CAX8.md) for axisymmetric problems.
The element does not decide between plane stress and plane strain in suanPan; the material's plane type does, and a plane-strain material forces unit thickness in elements that otherwise accept a thickness argument.
Reduced integration avoids volumetric locking for nearly incompressible plane-strain response but introduces hourglass modes that must be controlled by the element formulation.

## References

1. [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)
2. [ISBN 978-1-932159-75-2](https://search.worldcat.org/search?q=bn:9781932159752)
