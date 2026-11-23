# use

The `use` command selects the current integrator, solver or converger by tag.

## Syntax

```text title="use"
use (1) (2)
# (1) string, object type: Integrator, Solver or Converger
# (2) int, object tag
```

## Remarks

The selected object must already exist in the domain, otherwise the command has no effect.
