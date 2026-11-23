# GroupGroup

A `GroupGroup` combines several existing groups into a single group.
It is the nested counterpart of [`NodeGroup`](NodeGroup.md) and [`ElementGroup`](ElementGroup.md).

## Syntax

```text title="GroupGroup"
group GroupGroup (1) (2...)
# (1) int, unique group tag
# (2...) int, tags of groups to be included
```

## Remarks

1. Each referenced group is initialised first, so groups that define their members by rules are resolved before they are combined.
2. The members of all referenced groups are merged into the new pool with duplicates removed.
3. Groups can be nested, since a `GroupGroup` may itself reference another `GroupGroup`.
4. Referenced group tags that are not present in the domain are simply skipped.

## Example

The following snippet combines two node groups into one group containing nodes 1 through 6.

```
group NodeGroup 1 1 2 3
group NodeGroup 2 4 5 6

group GroupGroup 3 1 2
```
