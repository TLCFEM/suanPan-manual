# LinearViscosity

## Syntax

```text title="LinearViscosity"
modifier LinearViscosity (1) (2) [(3)...]
# (1) int, unique modifier tag
# (2) double, \mu
# [(3)...] int, element tags
```

This modifier applies linear viscosity to elements with the assigned $$\mu$$.

## Background

For each targeted element, the modifier builds a diagonal viscous matrix with $$\mu$$ on the diagonal and computes the damping force as $$\mu$$ times the trial velocity.
It therefore provides element-level damping proportional to the strain rate.
It is applied only in a dynamic analysis and only to elements that allow their viscous properties to be modified.

## Remarks

Because the damping is defined at element level, each element can record its own dissipated energy.
This differs from [`RayleighNewmark`](../../Integrator/Implicit/Newmark/RayleighNewmark.md), which applies Rayleigh damping after global assembly; with that global model the dissipated energy can only be recovered from global quantities, as discussed in [`Recorder`](../../Recorder/Recorder.md).
