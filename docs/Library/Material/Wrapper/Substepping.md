# Substepping

Adaptive substepping wrapper for an associated material model.

Splits a strain increment into smaller subincrements when the host model fails to converge on the full increment.

## Syntax

```text title="Substepping"
material Substepping (1) (2) [3]
# (1) int, unique material tag
# (2) int, associated material tag
# [3] int, maximum iteration, default: 20
```

## Remarks

`Substepping` makes a copy of the host material and drives it through a sequence of subincrements.
If a trial subincrement fails, the increment factor is halved and the substep is retried.
After three consecutive successful substeps, the increment factor is increased by a factor of 1.2.
The process ends once the full strain increment has been applied.
If the number of attempts reaches `(3)`, the update fails with an error message; the default limit of 20 is set in the input parser.

The wrapper adopts the material type, density, stiffness and history of the host model, so it can wrap any material whose return mapping is reliable only for small increments.
Typical applications include sharp yield surfaces and rapid softening, where a single large increment would otherwise fail to converge.
