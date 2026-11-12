# Modal Force Recorder

Extract Modal Elastic Forces from an Eigen Analysis

Minimum version: v4.4

The `ModalForce` recorder post-processes the results of a [`Frequency`](../Step/Frequency.md) step and writes the modal elastic forces.
It is the force counterpart of the [`Modal`](ModalRecorder.md) recorder, which writes frequencies, mode shapes, participation factors and effective modal masses.

The recorder stores an HDF5 file.
It does not record a time history; it stores a snapshot of the modal forces computed in the current step when that step is a [`Frequency`](../Step/Frequency.md) step.
Consequently, the recorder should be saved immediately after the eigenanalysis.
If it is also active in a later non-eigen step, the stored modal data is cleared when that step starts recording.

## Syntax

```text title="ModalForceRecorder"
recorder (1) hdf5 ModalForce
# (1) int, unique recorder tag
```

The `hdf5` keyword is required in practice because the modal data is written in HDF5 format.
The application must be compiled with HDF5 support.

Unlike the `Modal` recorder, no DoF identifiers are required.
The recorder writes the force of every extracted mode for all active nodes and all local elements.
The `every` keyword and object tags are not supported; all remaining tokens are ignored.

The recorder must be defined before the `analyze` command and it must be saved explicitly.

```text
recorder 1 hdf5 ModalForce

step frequency 1 10
analyze

save recorder 1
```

`peek recorder 1` prints a short description of the recorder.

Both modal properties and modal forces are often needed.
In that case, define both recorders before the analysis:

```text
recorder 1 hdf5 Modal U1
recorder 2 hdf5 ModalForce

step frequency 1 10
analyze

save recorder 1
save recorder 2
```

Each recorder writes its own file.

## Computed Quantities

For the generalised eigenproblem

$$
\mathbf{K}\mathbf{\phi}_n=\lambda_n\mathbf{M}\mathbf{\phi}_n,
$$

the mode shape is normalised with respect to the mass matrix,

$$
\mathbf{\phi}_n^T\mathbf{M}\mathbf{\phi}_n=1.
$$

The modal elastic force of mode $$n$$ is

$$
\mathbf{f}_n=\mathbf{K}\mathbf{\phi}_n.
$$

The recorder assembles the force element by element,

$$
\mathbf{f}_n=\sum_e\mathbf{K}_e\mathbf{\phi}_{n,e},
$$

rather than using the global stiffness matrix.
The global stiffness matrix is modified when boundary conditions and constraints are processed, whilst the element stiffness matrices are not.
Consequently, the assembled force vector contains the reaction components at restrained DoFs.
On unconstrained DoFs this is the usual elastic restoring force $$\mathbf{K}\mathbf{\phi}_n=\lambda_n\mathbf{M}\mathbf{\phi}_n$$.
On restrained DoFs it gives the reaction that enforces the mode shape, in the same sign convention as the nodal `RF` response.

The force vector corresponds to a unit modal displacement.
To obtain the peak modal force in a response-spectrum analysis, scale it by the corresponding modal coordinate amplitude, for example $$\Gamma_{n,j}S_d(T_n)$$.
The participation factor $$\Gamma_{n,j}$$ is available from the [`Modal`](ModalRecorder.md) recorder.

Modes whose modal mass is numerically zero or negative (for example, spurious modes in a model with an inconsistent mass matrix) are not normalised.
Their modal elastic force is zero.

!!! warning "global force"
    The force components are defined in the **global** coordinate system.
    They are different from the elemental forces for some element types.
    For example, with beam elements, the axial force and the transverse shear force are defined in the local frame, thus additional transformations are needed.

## Output File

The recorder writes

```text
R<tag>-ModalForce.h5
```

to the current output folder.
When the application runs with multiple MPI ranks, the file name is prefixed with the rank, for example

```text
P0-R1-ModalForce.h5
```

The output folder can be changed with the [`output_folder`](OutputFolder.md) attribute before the `save` command.

## Data Layout

Only the forces are stored.
Frequencies and mode shapes are available from the [`Modal`](ModalRecorder.md) recorder.
The HDF5 file contains the following objects.

```text
R1-ModalForce.h5
├── Mode 1                          one group per mode
│   ├── Nodes
│   │   ├── N1                      (n_dof_node_1, 1)
│   │   ├── N2                      (n_dof_node_2, 1)
│   │   └── ...
│   └── Elements
│       ├── E1                      (n_dof_element_1, 1)
│       ├── E2                      (n_dof_element_2, 1)
│       └── ...
├── Mode 2
│   └── ...
└── ...
```

1. Each mode has a group named `Mode 1`, `Mode 2`, etc.
   The group numbering follows the eigenvalue ordering, starting from one.
2. Each mode group contains two groups, `Nodes` and `Elements`.
3. For every active node, `Nodes` contains a dataset `N<tag>`.
   This is the assembled nodal force vector, that is, the sum of the force contributions of all elements attached to the node.
   Here `<tag>` is the node tag, not the node index.
   For example, node 10 produces `Nodes/N10`.
4. For every local element, `Elements` contains a dataset `E<tag>`.
   This is the element force vector

   $$
   \mathbf{f}_{n,e}=\mathbf{K}_e\mathbf{\phi}_{n,e}.
   $$

   Here `<tag>` is the element tag, not the element index.
   For example, element 10 produces `Elements/E10`.
   `E` denotes an element force; it is not a strain component.

The rows of `N<tag>` follow the node-local DoF order, that is, the order of the DoFs in the node's internal DoF list.
The rows of `E<tag>` follow the element-local DoF order, which is the node-by-node order used by the element stiffness matrix.
Typical examples are:

| object type                       | local DoF order                    |
|-----------------------------------|------------------------------------|
| two-dimensional solid node        | `U1`, `U2`                         |
| two-dimensional beam/shell node   | `U1`, `U2`, `UR3`                  |
| three-dimensional solid node      | `U1`, `U2`, `U3`                   |
| three-dimensional beam/shell node | `U1`, `U2`, `U3`, `UR1`, `UR2`, `UR3` |

For a two-node `Spring01` element in a two-dimensional model, the four rows of `E<tag>` are
`[U1 of node i, U2 of node i, U1 of node j, U2 of node j]`.

The dataset length is the total number of DoFs of the node or element, including constrained DoFs.
Constrained components are present in both `N<tag>` and `E<tag>`.
They are generally nonzero because they contain the reaction that enforces the mode shape.

The nodal force can be recovered from the element forces by summing the element contributions at each shared node.
This identity is useful for checking the data layout of a model with a new element type.

## Reading the Data

The following snippet reads the forces of the first mode.

```python
import h5py
import numpy as np

with h5py.File('R1-ModalForce.h5', 'r') as file:
    # node 2 in a two-dimensional model stores [U1, U2]
    nodal_force = file['Mode 1/Nodes/N2'][()].ravel()

    # element 1 stores its nodal DoFs one node after another
    element_force = file['Mode 1/Elements/E1'][()].ravel()
```

For all modes, loop over `file[f'Mode {mode + 1}/Nodes/N{tag}']` and `file[f'Mode {mode + 1}/Elements/E{tag}']`.
Note that Python uses zero-based indexing.

## Parallel Analysis

With multiple MPI ranks, every rank writes its own file.
The assembled nodal force vector `N<tag>` is reduced over all ranks, so each file contains the complete nodal forces for the nodes stored on that rank.
The element force datasets `E<tag>` contain only the local elements of the rank that writes the file.

## Relation to the Other Modal Recorders

The [Eigen recorder](Recorder.md) writes the raw eigenvalues and eigenvectors to `Eigenvalue.h5`.
The [`Modal`](ModalRecorder.md) recorder writes frequencies, mode shapes, participation factors and effective modal masses to `R<tag>-Modal.h5`.
The `ModalForce` recorder writes the modal elastic forces to `R<tag>-ModalForce.h5`.

The three recorders can be defined in the same analysis if all corresponding quantities are needed.

## Example

A complete worked example, including post-processing, modal combination and validation of the element forces, is given in [modal analysis of a shear building](../../Example/Structural/Dynamics/modal-analysis-of-a-shear-building.md).
