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

For an element with $$n$$ DoFs and trial velocity $$\dot{\mathbf u}_e$$, the modifier sets

$$
\mathbf C_e=\mu\,\mathbf I_n,\qquad
\mathbf f_{d,e}=\mathbf C_e\dot{\mathbf u}_e=\mu\,\dot{\mathbf u}_e .
$$

This is the simplest member of the element-level damping framework described on the [`Modifier`](Modifier.md) page, where more general damping matrices are discussed.

!!! warning "implementation limitation"
    The damping matrix is diagonal with the same $$\mu$$ on every DoF.
    A full viscous tensor with cross-coupling between directions is not supported.

## Remarks

Because the damping is defined at element level, each element can record its own dissipated energy.
This differs from [`RayleighNewmark`](../../Integrator/Implicit/Newmark/RayleighNewmark.md), which applies Rayleigh damping after global assembly; with that global model the dissipated energy can only be recovered from global quantities, as discussed in [`Recorder`](../../Recorder/Recorder.md).

1. The same value $$\mu$$ is placed on every diagonal entry, so the parameter has units of force per velocity and is not scaled by element size.
2. If no element tag is given, the modifier applies to all active elements in the domain.
3. Elements that disable viscous modification, such as [`Damper01`](../Special/Damper01.md), are skipped and keep their own material damping.
4. For frequency-dependent damping use [`ElementalLee`](ElementalLee.md) or [`ElementalNonviscous`](ElementalNonviscous.md) instead.
