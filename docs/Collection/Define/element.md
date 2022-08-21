# element

The `element` command is used to construct finite elements. Please refer to the specific type of elements for syntax and
details.

## General Syntax

In general, the syntax uses the following pattern:

```text
element <name> <tag> <connected_nodes> <associated_material> <other_specific_parameters>
```

## Output Types

All elements support record elemental stiffness and mass by tokens `K` and `M`. One can use the following to record 
them. The detailed syntax can be seen in [Record](../../Library/Recorder/Recorder.md) page.

```text
hdf5recorder (1) Element K (2...)
hdf5recorder (1) Element M (2...)
# (1) int, unique recorder tag
# (2...) int, element tags that K or M needs to be recorded
```

The matrices are vectorised.

Most elements do not support additional quantities to be recorded. There are some exceptions, however. The
additional ones will be documented in the specific element documentation.

The recording command will be directly forwarded to the attached material models. Take
the [`CP4`](../../Library/Element/Membrane/Plane/CP4.md) element for instance, it uses a second order Gaussian
quadrature, that is four integration points per element, each one is assigned with a copy of material model. If one
records the stress using a command similar to `plainrecorder 1 Element S 1`, the request will be forwarded to the
material models of all four integration points. Each point returns a vector of size 3,
$$\begin{bmatrix}\sigma_{11}&\sigma_{22}&\sigma_{12}\end{bmatrix}$$, four of those vectors will be concatenated so 
that the final record in the file will be a row of size 12.

| time | IP1             | IP1             | IP1             | IP2             | IP2             | IP2             | IP3             | IP3             | IP3             | IP4             | IP4             | IP4             |
|------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|
| time | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ |

The detailed quadrature schemes for elements are not well documented for the moment. The most used ones are Gauss 
and Lobatto with various orders.

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
