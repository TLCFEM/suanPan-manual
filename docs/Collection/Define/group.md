# group

The `group` command constructs a set of nodes to which the corresponding constraints and loads can be applied.
It is similar to the concept of a "set" in ABAQUS.

Please refer to [`generate`](generate.md) for the available commands.

## Remarks

1. The type token after `group` selects the implementation: `NodeGroup`, `CustomNodeGroup`, `ElementGroup`, `GroupGroup` or one of the `generate` forms.
2. These select nodes, custom nodes, elements and other groups respectively; see the corresponding pages in the [model library](../../Library/Overview.md).
3. The same objects can be created by the standalone commands `nodegroup`, `customnodegroup`, `elementgroup`, `groupgroup`, `generate`, `generatebyrule`, `generatebypoint` and `generatebyplane`.
4. Group tags are consumed by group-aware loads, constraints and recorders, and a group can be enabled or disabled by the `enable`/`disable` commands.
