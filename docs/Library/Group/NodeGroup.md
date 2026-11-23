# NodeGroup

A `NodeGroup` collects node tags under a single group tag so that loads, constraints and recorders can target many nodes at once.
It is analogous to a node "set" in ABAQUS.

## Syntax

```text title="NodeGroup"
group NodeGroup (1) (2...)
# (1) int, unique group tag
# (2...) int, tags of nodes to be included
```

## Remarks

1. The `group NodeGroup` form stores the listed node tags directly as the group pool.
2. Nodes can also be selected by rules rather than enumerated by tag via [`generate`](../../Collection/Define/generate.md), `generatebyrule`, `generatebypoint` and `generatebyplane`.
3. A `NodeGroup` can be referenced by group-aware loads such as [`groupcload`](../../Collection/Define/load.md), constraints such as [`grouppenaltybc`](../../Collection/Define/bc.md) and `GroupNode` recorders.

## Example

The following snippet, adapted from `Example/Solver/Ramm2.supan`, constrains one node and applies a load to the group.

```
node 11 2 8
node 12 3 8

group NodeGroup 1 11 12

fix 1 1 1 11

groupcload 1 0 -20 2 1

recorder 1 hdf5 GroupNode U 1
```
