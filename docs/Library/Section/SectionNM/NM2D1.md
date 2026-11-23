# NM2D1

$$N$$-$$M$$ Interaction Elastic Section

## References

1. [10.1061/JSENDH.STENG-12176](http://dx.doi.org/10.1061/JSENDH.STENG-12176)

## Background

`NM2D1` is the elastic member of the `SectionNM` family, it describes axial force and bending moment interaction at a member end using only `EA`, `EI` and the linear density.
Unlike the inelastic sections, it has no yield surface or history variables, the resistance is the initial stiffness times the deformation at every step.
The initial stiffness has off-diagonal terms between the two bending deformation components, so the section reproduces the elastic coupling of the N–M interaction formulation.

## Syntax

```text title="NM2D1"
section NM2D1 (1) (2) (3) (4)
# (1) int, unique section tag
# (2) double, EA
# (3) double, EI
# (4) double, linear density
```

## Remarks

`SectionNM` models take elemental deformation and resistance rather than sectional elongation and curvature, so `NM2D1` must be used with 2D N–M elements such as `NMB21`.
Use `NM2D2` or `NM2D3` for linear hardening and `NM2D3K` for nonlinear hardening, all of which define a yield surface and track history variables.
The corresponding three-dimensional elastic section is `NM3D1`.

## Example

The following is adapted from `Example/Section/NM2D1.supan`.

```text
node 1 0 0
node 2 2 0
node 3 1 0
section NM2D1 1 10 1E3 0.
element NMB21 1 1 3 1
element NMB21 2 3 2 1
```
