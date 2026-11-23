# Customisation

A number of universal wrappers are provided for uniaxial material models.
Analysts can flexibly combine an arbitrary number of simple material models to behave under a certain rheology structure.

The [`Parallel`](../Wrapper/Parallel.md) and [`Sequential`](../Wrapper/Sequential.md) wrappers can be used to create models that are rate independent.

## Rate-Independent Composition

Both wrappers take a list of 1D material tags and behave internally as a single 1D material.
`Parallel` applies a common strain to every constituent and adds their stresses.
`Sequential` enforces a common stress and accumulates their strains, solving for the strain share of each constituent at every step.
Neither wrapper may contain a viscosity-related model, since they are intended only for rate-independent hysteretic models.

## Rate-Dependent Composition

Rate dependence is not assembled with `Parallel` or `Sequential`.
Use the dedicated viscous materials, such as [`Kelvin`](../Material1D/Viscosity/Kelvin.md) (spring and dashpot in parallel), [`Maxwell`](../Material1D/Viscosity/Maxwell.md) (spring and dashpot in series), or [`Viscosity01`](../Material1D/Viscosity/Viscosity01.md) and [`Viscosity02`](../Material1D/Viscosity/Viscosity02.md) for standard viscous laws.
When the damping law is user defined, [`CustomViscosity`](../Material1D/Viscosity/CustomViscosity.md) supplies it through an expression.

## Substepping

The [`Substepping`](../Wrapper/Substepping.md) wrapper can be placed around a host model whose return mapping converges only for small strain increments.
It adaptively subdivides the increment and retries failed substeps with a smaller factor.

## Example

A Ramberg--Osgood spring and a bilinear hysteretic spring can be combined in parallel, and the result protected by substepping.

```text
material RambergOsgood 1 2E3 100
material Bilinear1D 2 2E3 10 .01
material Parallel 3 1 2
material Substepping 4 3
```

The element then refers to tag 4 instead of the individual constituents.
