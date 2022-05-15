# Logic

Sometimes, it is necessary to apply multiple convergers.

The `Logic` family provides some logical combinations of convergers so that it is convenient to chain arbitrary number
of convergers together.

## Syntax

```
converger LogicAND (1) (2) (3)
converger LogicOR (1) (2) (3)
converger LogicXOR (1) (2) (3)
# (1) int, unique converger tag
# (2) int, tag of first converger in logical operation
# (3) int, tag of second converger in logical operation
```

## Example

Let's assume by default the relative increment of displacement [`RelIncreDisp`](../Relative/RelIncreDisp.md) converger
is preferred. However, when performing a response history analysis, when the first displacement increment of some
substep is close to zero, then a small relative increment of displacement is not achievable due to machine precision. In
this case, we want to add another converger using absolute increment of
displacement [`AbsIncreDisp`](../Absolute/AbsIncreDisp.md) converger so that when absolute increment displacement is
small enough, the analysis is continued.

It is possible to use `LogicOR` to achieve this.

```
converger RelIncreDisp 1 1E-10 10 true
converger AbsIncreDisp 2 1E-10 10 true
converger LogicOR 3 1 2
```

Note the last defined converger in any step will be used for that particular step. In this case, converger `3`
using `LogicOR` would be used.

The following definition **does not** work.

```
converger LogicOR 3 1 2
converger RelIncreDisp 1 1E-10 10 true
converger AbsIncreDisp 2 1E-10 10 true
```

The chained convergers would be initialised recursively. This means it is possible to chain arbitrary number of
convergers together. For example,

```
converger RelIncreDisp 1 1E-10 10 true
converger AbsIncreDisp 2 1E-10 10 true
converger LogicOR 3 1 2
converger AbsResidual 4 1E-10 10 true
converger LogicAND 5 3 4
```

Eventually, the converger `5` will be used, in which convergers `1`, `2` and `4` will be called in order.
