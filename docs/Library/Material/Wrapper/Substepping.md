# Substepping

Adaptive substepping wrapper for an associated material model.

Splits a strain increment into smaller subincrements when the host model fails to converge on the full increment.

## Theory

Rate-independent constitutive integrations based on a return mapping are usually accurate only for sufficiently small strain increments.
When a single increment crosses a sharp yield surface or a rapid softening branch, the local Newton iteration may fail or produce a poor state.
An automatic substepping strategy applies the total increment $$\Delta\mathbf e$$ as a sequence of fractions,

$$
\mathbf e_{k+1}=\mathbf e_k+\delta_k\,\Delta\mathbf e,
\qquad
\sum_k\delta_k=1,
$$

and adjusts the fraction $$\delta_k$$ according to whether the host succeeds.
The implementation keeps two copies of the host, one representing the committed state and one representing the trial state.
At the start of an update the trial copy is recreated from the committed copy, the fraction is initialised to one, and the host is asked to update to $$\mathbf e_{\mathrm{current}}+(\alpha+\delta)\Delta\mathbf e$$, where $$\alpha$$ is the accumulated fraction.
A failed trial resets the success counter and halves the fraction, while a successful trial is committed immediately and advances the accumulated fraction.
Every three consecutive successes the fraction is multiplied by $$1.2$$, and it is always capped by the remaining fraction $$1-\alpha$$.
The process ends when the next fraction falls below the internal tolerance, meaning the full increment has been applied.
Every attempt, successful or not, counts towards `(3)`, and reaching the limit is reported as an error.

This is a success-driven adaptive scheme rather than the truncation-error-controlled family of algorithms proposed by Sloan, so the fraction changes heuristically instead of being selected from an estimated local error.

!!! info "deviation from Sloan's substepping"
    Sloan's method estimates the local truncation error of the stress integration and chooses the substep size to meet a prescribed tolerance.
    The suanPan `Substepping` wrapper does not compute an error estimate, so the substep size follows a fixed heuristic rather than a truncation-error target.
    The reference is included for background only, and the wrapper does not reproduce that algorithm.

!!! note "developer note"
    The wrapper halves the fraction after any failed host update and increases it by a factor of 1.2 after every three successes.

The wrapper forwards material type, density and all state getters and setters to the appropriate host copy, so it can wrap a model of any dimensionality.
Only the strain-based overload of `update_trial_status` is implemented, so rate-dependent hosts that require a strain rate are not driven through their rate overload.

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

The wrapper only helps if the host signals failure by returning an error code, so a host with a very loose internal tolerance will still accept an inaccurate large increment.
Because each successful substep is committed inside the wrapper, a later failure cannot roll back earlier substeps of the same global increment; the global analysis still sees a single trial state.
Use smaller global increments when the attempt limit is reached, since that reduces the number of subincrements required for the same accuracy.
Combine with [PlaneStress](PlaneStress.md) or [Uniaxial](Uniaxial.md) only when the outer reduction itself is accurate, because substepping cannot repair a residual left by a single-pass condensation.

## References

- [10.1002/nme.1620240505](https://doi.org/10.1002/nme.1620240505)
- [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
