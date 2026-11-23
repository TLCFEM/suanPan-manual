# ConcreteTable

Concrete Material With Table Input

## Syntax

```text title="ConcreteTable"
material ConcreteTable (1) (2) (3) [4] [5]
# (1) int, unique material tag
# (2) string, tension backbone file name
# (3) string, compression backbone file name
# [4] double, middle point parameter [0,1], default: 0.2
# [5] double, density, default: 0.0
```

## Background

`ConcreteTable` replaces the analytic backbone functions of [`ConcreteTsai`](ConcreteTsai.md) and [`ConcreteExp`](ConcreteExp.md) with piecewise linear interpolation of two two-column tables.
Each file lists strain in the first column and stress in the second, and both are read as plain ASCII matrices during initialization.
The tension table is supplied first and the compression table second, and the parser stores their absolute values with the compression sign restored.
The initial stiffness is taken as the average of the first secant slopes of the two tables.
The compression peak strain is located at the minimum tabulated stress and the tension peak strain at the maximum tabulated stress.
Beyond the last tabulated point the stress stays at the final value with a near-zero tangent, which prevents unbounded extrapolation.
The hysteresis rules, residual strains and crack-closing transition are inherited from [`SimpleHysteresis`](../Hysteresis/SimpleHysteresis.md), so the middle point parameter has the same meaning as in the other simple concrete models.

!!! warning "implementation limitation"
    The backbone is piecewise linear, so the tangent is discontinuous at every tabulated point.
    Beyond the last tabulated point the returned stress is taken from the last entry of the strain column rather than the stress column, and the tangent is effectively zero.
    The model does not read the element characteristic length, so tabulated softening must be scaled by the analyst for mesh objectivity.

!!! note "developer note"
    Beyond the last tabulated point the tangent is set to $10^{-10}$.

## Remarks

Both files must contain exactly two columns, with strains in the first column and stresses in the second.
The compression file is normally written with negative strain and stress values, but the parser takes absolute values and reapplies the signs internally.
The tension file should contain monotonically increasing positive strains and stresses so that interpolation and crack-strain detection behave as intended.
The first two rows of each table set the initial stiffness, so they should lie in the elastic range.
The middle point parameter `[4]` is clamped to $[0,1]$ and controls the size of the hysteresis loop in the inherited rules.
A denser table gives a smoother backbone at the cost of slower interpolation.
The density `[5]` defaults to zero.

## Example

```text
material ConcreteTable 1 T.txt C.txt
materialTest1D 1 1E-4 50 100 120 140 160 180
```

This is the configuration used in `Example/Material/ConcreteTable.supan`.

## References

1. [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook)
