# element

The `element` command constructs finite elements.
Please refer to the specific element types for syntax and details.

## General Syntax

In general, the syntax uses the following pattern:

```text
element <name> <tag> <connected_nodes> <associated_material> <other_specific_parameters>
```

## Output Types

All elements support recording the elemental stiffness and mass with the tokens `K` and `M`.
Use the following commands to record them.
The detailed syntax is described on the [Recorder](../../Library/Recorder/Recorder.md) page.

```text
hdf5recorder (1) Element K (2...)
hdf5recorder (1) Element M (2...)
# (1) int, unique recorder tag
# (2...) int, element tags that K or M needs to be recorded
```

The matrices are vectorised.

Most elements do not support recording additional quantities.
There are some exceptions, however, which are documented on the corresponding element pages.

The recording command is forwarded directly to the attached material models.
For example, the [`CP4`](../../Library/Element/Membrane/Plane/CP4.md) element uses second-order Gaussian quadrature, that is, four integration points per element.
Each integration point is assigned a copy of the material model.
If the stress is recorded with a command similar to `plainrecorder 1 Element S 1`, the request is forwarded to the material models of all four integration points.
Each point returns a vector of size 3,
$$\begin{bmatrix}\sigma_{11}&\sigma_{22}&\sigma_{12}\end{bmatrix}$$.
The four vectors are concatenated so that the final record in the file is a row of size 12.

| time | IP1             | IP1             | IP1             | IP2             | IP2             | IP2             | IP3             | IP3             | IP3             | IP4             | IP4             | IP4             |
|------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|
| time | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ | $$\sigma_{11}$$ | $$\sigma_{22}$$ | $$\sigma_{12}$$ |

The detailed quadrature schemes for elements are not well documented at present.
The most commonly used schemes are Gauss and Lobatto with various orders.

## Implementation Details

### Creation

Creating an element validates nothing beyond the scope of the element itself.
For example, suppose the correct syntax is the following.

```text
element MyEle (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, tag of the first node
# (3) int, tag of the second node
# (4) int, tag of the material
```

Then `element MyEle 7 8 9 10` creates an element with tag 7, nodes 8 and 9, and material 10.
In contrast, `element MyEle 7 8 9` or `element MyEle 7 8 9 unexpected_str` fails the creation.
Whether nodes 8 and 9 and material 10 exist is not validated at this point.
Instead, these validations are performed during initialisation, before the analysis stage.
This means the order in which basic components are defined is **not** important.
It is valid to define an element before defining its connected nodes.

### Initialisation

Before performing the analysis, all defined elements are initialised.
During this stage, each element checks that the connected nodes are active and able to accommodate the DoFs required by the element.
Local copies of the attached material models are retrieved from the global storage.
If any mismatch is found, for example, a uniaxial material model assigned to a 3D element, the element is disabled.

### Analysis

During the analysis stage, the global solving algorithm solves the global system and updates the nodal displacements accordingly.
The new nodal displacements are dispatched to all active elements for further analysis.

From the element's perspective, it returns the elemental nodal force vector for the given nodal displacement vector.

### Interaction

The problem domain holds all the information that elements need to update themselves.
Elements do not interact with the global data storage directly.
Instead, they only communicate with the associated nodes and sections/materials.

A complete interaction graph is shown below.
For elements themselves, apart from the connected nodes, they do not share information with any other objects.
Some elements may not even need sections and/or materials.

``` mermaid
graph LR
  A[Domain] -->|update_trial_status| B[Element];
  A -->|update_trial_status| J[Node];
  J -->|get_trial_displacement| B;
  B -->|update_trial_status| D[Section];
  D -->|update_trial_status| F[Material];
  F -->|get_trial_stress| D;
  F -->|get_trial_stiffness| D;
  D -->|get_trial_resistance| B;
  D -->|get_trial_stiffness| B;
  B -->|get_trial_resistance| A;
  B -->|get_trial_stiffness| A;
```
