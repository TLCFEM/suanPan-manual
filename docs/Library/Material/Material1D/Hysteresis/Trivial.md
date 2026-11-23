# Trivial

Zero Response Material

The `Trivial` material defines 1D zero response.
The stress and stiffness outputs will be zero for all strain inputs.

## Background

A zero-response material is the neutral element of a material assembly, so adding it in parallel does not change the response and placing it in series imposes no additional constraint.
The implementation stores only the strain and returns zero stress and zero stiffness, so no state determination or local iteration is required.

## Syntax

```text title="Trivial"
material Trivial (1)
# (1) int, unique material tag
```

## Remarks

- Both the stress and the tangent stiffness are identically zero for every strain, and no density or history data are required.
- The implementation installs a constant-stiffness modifier, so the zero tangent is reported consistently to the global solver.
- The material is useful as a placeholder for inactive degrees of freedom or as a null component in a parallel or serial assembly.
- It can be driven with `materialTest1D` to verify that a model returns zero response.

## Example

```
material Trivial 1
materialTest1D 1 1E-3 10 20 10
```
