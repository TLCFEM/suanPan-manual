# CustomViscosity

Viscous Material Using Custom Model

Reference:

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Syntax

```
material CustomViscosity (1) (2)
# (1) int, unique material tag
# (2) int, expression tag
```

## Remarks

The expression needed takes strain and strain rate as the inputs and returns the damping coefficient and its derivatives
as the outputs.

The input size shall be 2 and the output size shall be 3.

## Example

Imaging to model the linear viscous material such that

$$
\sigma=1234\dot{\epsilon},
$$

One can define the expression as

```text
expression SimpleVector 1 x|2 y|3 y[0]:=1234*x[1];y[1]:=0;y[2]:=1234;
```

The strain maps to `x[0]` and the strain rate maps to `x[1]`.

The stress output maps to `y[0]` and its derivatives regarding strain and strain rate maps to `y[1]` and `y[2]`
respectively.
