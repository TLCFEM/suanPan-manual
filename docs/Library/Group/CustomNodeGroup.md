# CustomNodeGroup

Select and collect nodes into a group based on a custom criterion.

## Syntax

```
CustomNodeGroup (1) (2)
# (1) int, unique group tag
# (2) int, expression tag
```

## Example

The `CustomNodeGroup` uses an [`expression`](../../Collection/Define/expression.md) to determine whether a given node shall be included in the group.

It uses the coordinates of the target node (with size adjusted) as the input and the expression shall return a positive value if the node shall be included in the group. Otherwise, it shall return a negative value.

The following example selects all nodes with `x` coordinate greater than 0.5.

```
expression SimpleScalar 1 x if(x>0.5)1;else-1;
customnodegroup 1 1
```

The following example selects all nodes with `x` coordinate greater than 0.5 and `y` coordinate less than 0.5.

```
expression SimpleScalar 1 x|y if(x>0.5&y<0.5)1;else-1;
customnodegroup 1 1
```

Of course, the expression can be more complicated when the expression text is given in a file.
