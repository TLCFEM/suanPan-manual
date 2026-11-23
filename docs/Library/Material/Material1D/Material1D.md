# Material1D

In addition to the default output types supported by all materials, all uniaxial material models support the following basic output types.

| variable label | physical meaning         |
| -------------- | ------------------------ |
| SP             | principal stress         |
| EP             | principal strain         |
| EEP            | principal elastic stress |
| PEP            | principal plastic strain |

All principal values are identical to the normal ones for uniaxial material models.

Depending on the specific material model, additional output types may be available.

The history vector is a vector of variadic length that stores the necessary history variables for the material model.
Different material models may have different history variable storage layouts.

## Background

A uniaxial material model reduces the constitutive response at an integration point to one stress component and one strain component.
The base [`Material`](../Overview.md) class stores the strain, the strain rate, the stress, the stress rate and a history vector in two copies.
The current state is the last converged state and the trial state is the state updated during equilibrium iterations.
A trial update that fails an iteration is discarded by `reset_status`, whereas a converged trial state is promoted by `commit_status`.
The `clear_status` method restores both states to the initial condition at the start of a new analysis.
Because the strain and stress are scalars, the tangent stiffness is a symmetric scalar and the `Material1D` constructor marks it as such.
The axial strain is positive in tension and negative in compression, and the same convention applies to the axial stress.
The secant stiffness is the ratio of stress to strain, whereas the tangent stiffness is the derivative of stress with respect to strain and is the quantity used to assemble the stiffness matrix in a Newton--Raphson iteration.
Path-independent models such as [`Elastic1D`](Elastic/Elastic1D.md) store no history variables, while path-dependent models use the history vector to remember envelope points and internal variables.
The density is inherited from the base class and is used only in mass and damping related computations.

The principal output labels are aliases that are mapped onto the basic scalar outputs.
Thus `SP` returns the same value as `S`, `EP` the same as `E`, `EEP` the same as `EE`, and `PEP` the same as `PE`.
Models without a plastic decomposition may still report `PEP`, in which case the value is typically zero.

## Remarks

A one-dimensional material can be assigned directly to the truss elements [`T2D2`](../../Element/Truss/T2D2.md) and [`T3D2`](../../Element/Truss/T3D2.md).
For section-based elements the material must be referenced by a one-dimensional section such as [`TrussSection`](../../Section/Section1D/TrussSection.md) or a fibre section.
A scalar tangent stiffness is sufficient only for uniaxial kinematics, so the same material must not be assigned to a multi-dimensional continuum element.

!!! warning "implementation limitation"
    The `Material1D` constructor fixes the material type to `MaterialType::D1` and calls `set_symmetric(true)`.
    The tangent stiffness is therefore stored and used as a symmetric scalar.
    The class does not provide the tensor-valued stiffness required by a two- or three-dimensional continuum element.

The history layout is model specific, so history variables should be interpreted only with the documentation of the chosen material.
Wrapper models such as those in [`Degradation`](Degradation/Degradation.md) add their own history variables while forwarding the strain to a host material.
The elastic material families are documented in [`Elastic1D`](Elastic/Elastic1D.md), while stiffness loss is documented in [`Degradation`](Degradation/Degradation.md).
