# Tie

Multipoint Constraint Implemented As Element

* Number of Nodes: varies
* Number of DoFs: varies

## Syntax

```
element Tie (1) (2) (3) [(4) (5) (6)...]
# (1) int, unique element tag
# (2) double, right hand side of the constraint equation, the constraint is homogeneous if this parameter is zero
# (3) double, penalty number, a relatively large number
# (4) int, node tag
# (5) int, dof tag
# (6) double, weight
```

## Example

Each `Tie` element can have multiple DoFs included. For example, to define the following constraint,

$$
5u_2+6v_4=9,
$$

where $$u_2$$ and $$v_4$$ are horizontal displacement of node `2` and vertical displacement of node `4` in a 2D model,
then

```
element Tie 1 9. 1E8 2 1 5. 4 2 6.
```

In the above command, a large number `1E8` is used as penalty.

The `Tie` element does not care about the geometric implication.
The tied DoFs can be of different types.

To tie a node to a line, consider the [`TranslationConnector`](TranslationConnector.md) element.
