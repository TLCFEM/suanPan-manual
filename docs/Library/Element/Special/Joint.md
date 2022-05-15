# Joint

Joint Element

The `Joint` is a joint element that uses **displacement** as inputs.

* Number of Nodes: 2
* Number of DoFs: varies

## Syntax

```
element Joint (1) (2) (3) (4...)
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4...) int, material tags
```

## Remarks

The `Joint` element defines a joint connecting two nodes that can coincide with each other regarding their coordinates.
The relative displacement is used as strain input. Thus, the corresponding material model shall be defined to use
displacement and force. Note in the current implementation the global horizontal and vertical displacements are passed
to the material models to compute the response.

The number of connected degrees of freedom can vary based on the number of tags of material models assigned to the
element. The material models are used for each DoF sequentially according to the definition. If one wants to define a
joint tagged `5` between node `1` and node `2` using material `3` for the first four DoFs, the following command can be
used.

```
element Joint 5 1 2 3 3 3 3
```
