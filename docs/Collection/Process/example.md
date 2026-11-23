# example

The `example` command establishes and executes a minimum example automatically.
It builds a two-node elastic truss under tension, solves a static step, and reports the nodal force.

## Syntax

```text title="example"
example
```

## Remarks

The command takes no arguments and builds the model in a new domain, leaving the current model untouched.
Each command is echoed to the terminal and followed by a one-second pause before it is processed.
The model uses two nodes, an `Elastic1D` material with modulus 52, and a `T2D2` truss element with area 93.
The reported force at node 2 is P = UEA/L = 1.4 * 52 * 93 / 2 = 3385.2.
