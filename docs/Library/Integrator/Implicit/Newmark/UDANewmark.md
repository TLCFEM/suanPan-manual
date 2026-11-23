# UDANewmark

Newmark Time Integration With Universal Damping on Inertial Forces

`UDANewmark` is the inertial-force counterpart of [`UDDNewmark`](UDNewmark.md).
Both integrators implement a uniform (universal) damping model using a complex-valued kernel, but they apply it to different force vectors.

`UDDNewmark` convolutes the restoring force, whereas `UDANewmark` convolutes the inertial force.
Consequently, `UDANewmark` modifies the mass-related terms of the equation of motion rather than the stiffness-related terms.

The parameters $$m_j$$ and $$s_j$$ define the kernel of the convolution.
The same kernel notation and the damping curve discussed on the [`UDDNewmark`](UDNewmark.md) page apply here.

## Syntax

```text title="UDANewmark"
integrator UDANewmark (1) (2) (3) ((4) (5) (6) (7)...)
# (1) int, unique tag
# (2) double, alpha, typical: 0.25
# (3) double, beta, typical: 0.5
# (4) double, real part of `m_j`
# (5) double, imaginary part of `m_j`
# (6) double, real part of `s_j`
# (7) double, imaginary part of `s_j`
```

Each group of four values defines one term of the kernel.
The kernel is assumed to apply to all DoFs in the system.

The weights $$m_j$$ must have positive real parts and the poles $$s_j$$ must have negative real parts.
The imaginary parts must form conjugate pairs so that the resulting damping force is real-valued.
The parser rejects parameter sets that do not satisfy these conditions.

## Remarks

If only hysteretic and inertial actions are present, `UDANewmark` and `UDDNewmark` are equivalent.
They can be transformed into each other with the mapping given in the [Remarks of the `UDDNewmark` page](UDNewmark.md#remarks).
Use `UDDNewmark` when the damping model is naturally expressed in terms of the restoring force.
Use `UDANewmark` when it is naturally expressed in terms of the inertial force.

The damping model introduces frequency-dependent behaviour.
As with `UDDNewmark`, it may induce dynamic hardening of the system.

## References

1. [10.1016/j.compstruc.2018.10.016](https://doi.org/10.1016/j.compstruc.2018.10.016)
2. [10.31224/8137](https://doi.org/10.31224/8137)
