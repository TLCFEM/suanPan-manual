# element

The `element` command is used to construct finite elements. Please refer to the specific type of elements for syntax and
details.

## General Syntax

In general, the syntax uses the following pattern:

```text
element <name> <tag> <connected_nodes> <associated_material> <other_specific_parameters>
```

## Implementation Details

### Creation

The creation of any elements does not validate anything beyond the scope of the element. For example, if the correct
syntax appears to be the following.

```text
element MyEle (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, tag of the first node
# (3) int, tag of the second node
# (4) int, tag of the material
```

Then `element MyEle 7 8 9 10` will create an element with tag 7, nodes 8, 9 and material 10, while `element MyEle 7 8 9`
or `element MyEle 7 8 9 unexpected_str` will fail the creation. Whether nodes 8, 9 and material 10 exist or not is not
validated. Instead, these type of validations are performed during the initialisation stage, before the analysis stage.
This means, the order of defining basic components is **not** important. It is valid to define an element before
defining its connected nodes.

### Initialisation

Before performing the analysis, all defined elements will be initialised. During this stage, each element will check the
connected nodes and make sure they are active, and are able to accommodate the DoFs needed by the element. Local copies
of the attached material models will be retrieved from the global storage. If any mismatch is found, for example, a
uniaxial material model is assigned to a 3D element, the element will be disabled.

### Analysis

During the analysis stage, the global solving algorithm solves the global system and updates nodal displacement
accordingly. The new nodal displacement will be dispatched to all active elements for further analysis.

From the element's perspective, it is in charge of returning elemental nodal force vector based on given nodal
displacement vector.
