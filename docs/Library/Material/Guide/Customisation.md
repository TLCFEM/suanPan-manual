# Customisation

A number of universal wrappers are provided for uniaxial material models.
Analysts can flexibly combine an arbitrary number of simple material models to behave under a certain rheology structure.

The [`Parallel`](../Wrapper/Parallel.md) and [`Sequential`](../Wrapper/Sequential.md) wrappers can be used to create models that are rate independent.

## Model Categories

A uniaxial material can be classified by whether its response depends on time or loading rate.
Elastic and rate-independent hysteretic models return a stress that is a function of strain and history only, so repeating a displacement path at a different speed gives the same stress--strain loop.
Plasticity models such as [`Bilinear1D`](../Material1D/vonMises/Bilinear1D.md), damage models and phenomenological hysteresis models such as [`BoucWen`](../Material1D/Hysteresis/BoucWen.md) belong to this group.
Rate-dependent models return a damping coefficient in addition to a stress and require an element that supplies strain rate.
The dashpot family [`Viscosity01`](../Material1D/Viscosity/Viscosity01.md), [`Viscosity02`](../Material1D/Viscosity/Viscosity02.md), [`BilinearViscosity`](../Material1D/Viscosity/BilinearViscosity.md) and [`CustomViscosity`](../Material1D/Viscosity/CustomViscosity.md) respond only to velocity.
The rheological models [`Kelvin`](../Material1D/Viscosity/Kelvin.md) and [`Maxwell`](../Material1D/Viscosity/Maxwell.md) combine a spring and a dashpot and respond to both strain and strain rate.
Wrappers such as [`Parallel`](../Wrapper/Parallel.md), [`Sequential`](../Wrapper/Sequential.md) and [`Substepping`](../Wrapper/Substepping.md) modify how a material is embedded rather than adding a new constitutive law.

!!! info "deviation from theory"
    The `Sequential` wrapper solves for strain shares under a common stress using current trial stiffnesses, which is a static series assembly and not the rate-dependent Maxwell rheology.
    The `Parallel` wrapper forwards strain rate to its constituents, so it can assemble viscous branches even though rate-independent composition is the usual use.

## Choosing a Model

Choose a rate-independent hysteretic model when the measured loops are insensitive to loading frequency and only the backbone and the unloading rule are known.
Choose a viscous or rheological model when creep, stress relaxation, velocity-dependent force or a damping matrix contribution is part of the response.
For concrete, the rule-based [`ConcreteCM`](../Material1D/Concrete/ConcreteCM.md) and [`ConcreteTsai`](../Material1D/Concrete/ConcreteTsai.md) reproduce cyclic loops, while the damage-plasticity [`ConcreteK4`](../Material1D/Concrete/ConcreteK4.md) tracks stiffness degradation through a damage variable.
For metals, the guide in [`Metal`](Metal.md) summarises hardening rules and the Bauschinger effect.
The element must be compatible with the material interface, because the strain-only update of a dashpot is deliberately rejected.

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

## Remarks

The `Parallel` wrapper also overrides the two-argument update and forwards both strain and strain rate to its constituents, so it can assemble parallel rheologies when the element supplies strain rate.
The `Sequential` wrapper implements only the strain-only update, so it cannot host a viscous constituent.
When an element supplies strain only, a viscous constituent inside any wrapper fails because dashpots reject that update, which is why the wrappers are normally restricted to rate-independent models.
Constituent materials are accessed by tag, so every material used inside a wrapper must be defined before the wrapper itself.
The density reported by `Parallel` is the sum of the constituent densities, which matters in dynamic analyses.

## References

1. Chang, T. L. (2023), Constitutive Modelling Cookbook, [online](https://github.com/TLCFEM/constitutive-modelling-cookbook).
