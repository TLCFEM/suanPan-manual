# suspend

The `suspend` command ends the activity of the given constraints, loads or convergence criteria at the current step.
The tagged objects remain in the model but are no longer applied from the current step onward.

## Syntax

```text title="suspend"
suspend (1) [2...]
# (1) string, object type: constraint, load or criterion
# [2...] int, tags
```

## Remarks

The end step of each tagged object is set to the current step tag, so it is considered active only for earlier steps.
