# Modal Recorder

Extract Modal Properties from an Eigen Analysis

Minimum version: v4.4

The `Modal` recorder post-processes the results of a [`Frequency`](../Step/Frequency.md) step and writes the modal properties that are commonly used in structural dynamics:

1. natural frequencies,
2. mass-normalised mode shapes,
3. modal participation factors,
4. effective modal masses,
5. modal elastic forces, including reactions.

The recorder stores an HDF5 file.
It does not record a time history; it stores a snapshot of the modal properties computed in the current step when that step is a [`Frequency`](../Step/Frequency.md) step.
Consequently, the recorder should be saved immediately after the eigenanalysis.
If it is also active in a later non-eigen step, the stored modal data is cleared when that step starts recording.

## Syntax

```text title="ModalRecorder"
recorder (1) hdf5 Modal (2...)
# (1) int, unique recorder tag
# (2...) string, at least one DoF identifier
```

The `hdf5` keyword is required in practice because the modal data is written in HDF5 format.
The application must be compiled with HDF5 support.

The DoF identifiers define the directions of the influence vector(s) used for the participation factors and effective masses.
The following identifiers are supported.

| identifier              | meaning                                                       |
|-------------------------|---------------------------------------------------------------|
| `U1`, `1`               | translation along DoF 1                                       |
| `U2`, `2`               | translation along DoF 2                                       |
| `U3`, `3`               | translation along DoF 3                                       |
| `U4`, `4`, `UR1`        | rotation about DoF 1                                          |
| `U5`, `5`, `UR2`        | rotation about DoF 2                                          |
| `U6`, `6`, `UR3`        | rotation about DoF 3                                          |
| `P`, `PINNED`           | `U1`, `U2`, `U3`                                              |
| `E`, `ENCASTRE`         | `U1`, `U2`, `U3`, `UR1`, `UR2`, `UR3`                         |
| `X`, `XSYMM`            | `U1`, `UR2`, `UR3`                                            |
| `Y`, `YSYMM`            | `UR1`, `U2`, `UR3`                                            |
| `Z`, `ZSYMM`            | `UR1`, `UR2`, `U3`                                            |

Duplicated directions are removed and the remaining directions are sorted before the modal properties are computed.
At least one valid direction must be given.
For example,

```text
recorder 1 hdf5 Modal U1
recorder 2 hdf5 Modal U1 U2 UR3
recorder 3 hdf5 Modal E
```

The recorder must be defined before the `analyze` command and it must be saved explicitly.

```text
step frequency 1 10
analyze

save recorder 1
```

`peek recorder 1` prints a short description of the recorder.
Note that `every` and object tags are not supported for this recorder; all remaining tokens are interpreted as DoF identifiers.

## Computed Quantities

For the generalised eigenproblem

$$
\mathbf{K}\boldsymbol{\phi}_n=\lambda_n\mathbf{M}\boldsymbol{\phi}_n,
$$

define the mass-normalised mode shape

$$
\boldsymbol{\phi}_n^T\mathbf{M}\boldsymbol{\phi}_n=1.
$$

The recorder computes the following quantities for mode $$n$$ and direction $$j$$.

| quantity                 | symbol                  | definition                                                                    |
|--------------------------|-------------------------|-------------------------------------------------------------------------------|
| natural frequency        | $$f_n$$                 | $$f_n=\dfrac{\sqrt{\lambda_n}}{2\pi}$$                                        |
| mode shape               | $$\boldsymbol{\phi}_n$$ | mass-normalised, $$\boldsymbol{\phi}_n^T\mathbf{M}\boldsymbol{\phi}_n=1$$     |
| participation factor     | $$\Gamma_{n,j}$$        | $$\Gamma_{n,j}=\boldsymbol{\phi}_n^T\mathbf{M}\mathbf{r}_j$$                  |
| effective modal mass     | $$m_{n,j}$$             | $$m_{n,j}=\Gamma_{n,j}^2$$                                                    |
| modal elastic force      | $$\mathbf{f}_n$$        | $$\mathbf{f}_n=\mathbf{K}\boldsymbol{\phi}_n$$                                |

In the above, $$\mathbf{r}_j$$ is the unit influence vector in direction $$j$$.
For example, for `U1`, every active `U1` DoF receives a unit entry and all other entries are zero.

!!! note
    The frequency is stored in hertz.
    The eigenvalue can be recovered as $$\lambda_n=(2\pi f_n)^2$$.

The sign of a mode shape is arbitrary: an eigenvector can be multiplied by $$-1$$ without changing any physical result.
Consequently, the sign of the corresponding participation factor is also arbitrary.
The effective mass is not affected by the sign.

The modal elastic force is assembled from the element stiffness matrices,

$$
\mathbf{f}_n=\sum_e\mathbf{K}_e\boldsymbol{\phi}_{n,e},
$$

rather than from the global stiffness matrix, because the global matrix is modified when boundary conditions and constraints are processed.
On unconstrained DoFs this is the usual elastic restoring force $$\mathbf{K}\boldsymbol{\phi}_n=\lambda_n\mathbf{M}\boldsymbol{\phi}_n$$.
On restrained DoFs it gives the reaction that enforces the mode shape, in the same sign convention as the nodal `RF` response.
The force vector corresponds to a unit modal displacement.
To obtain the peak modal force in a response-spectrum analysis, scale it by the corresponding modal coordinate amplitude, for example $$\Gamma_{n,j}S_d(T_n)$$.

If the full set of modes is computed, the effective masses in a given direction sum to the total mass mobilised by the unit influence vector,

$$
\sum_n m_{n,j}=\mathbf{r}_j^T\mathbf{M}\mathbf{r}_j.
$$

This identity is useful for checking that enough modes have been extracted.

Modes whose modal mass is numerically zero or negative (for example, spurious modes in a model with an inconsistent mass matrix) are not normalised.
Their modal elastic force remains zero.

## Output File

The recorder writes

```text
R<tag>-Modal.h5
```

to the current output folder.
When the application runs with multiple MPI ranks, the file name is prefixed with the rank, for example

```text
P0-R1-Modal.h5
```

The output folder can be changed with the [`output_folder`](OutputFolder.md) attribute before the `save` command.

## Data Layout

The HDF5 file contains the following objects.

```text
R1-Modal.h5
├── Frequency                       (n_mode, 1)
├── U1                              one group per requested direction
│   ├── ParticipationFactor         (n_mode, 1)
│   └── EffectiveMass               (n_mode, 1)
├── U2
│   ├── ParticipationFactor
│   └── EffectiveMass
├── Mode 1                          one group per mode
│   ├── N1                          (n_dof_node_1, 1)
│   ├── F1                          (n_dof_node_1, 1)
│   ├── N2                          (n_dof_node_2, 1)
│   ├── F2                          (n_dof_node_2, 1)
│   └── ...
├── Mode 2
│   └── ...
└── ...
```

1. `Frequency` stores one natural frequency per row in hertz.
2. Each requested direction has a group named after the canonical DoF identifier, for example `U1`, `U2` or `UR3`.
   Numeric aliases such as `1` or `6` are accepted in the command, but the group always uses the canonical name.
   The group contains the participation factors and effective masses for all modes in that direction.
   Both datasets have one row per mode.
3. Each mode has a group named `Mode 1`, `Mode 2`, etc.
   The group numbering follows the eigenvalue ordering, starting from one.
4. For every active node, the mode group contains two datasets:
    - `N<tag>` is the nodal mode shape,
    - `F<tag>` is the nodal modal elastic force, including reactions.

   Here `<tag>` is the node tag, not the node index.
   For example, node 10 produces `N10` and `F10`.

The rows of `N<tag>` and `F<tag>` follow the node-local DoF order, that is, the order of the DoFs in the node's internal DoF list.
Typical examples are:

| node type                         | local DoF order                    |
|-----------------------------------|------------------------------------|
| two-dimensional solid             | `U1`, `U2`                         |
| two-dimensional beam/shell        | `U1`, `U2`, `UR3`                  |
| three-dimensional solid           | `U1`, `U2`, `U3`                   |
| three-dimensional beam/shell      | `U1`, `U2`, `U3`, `UR1`, `UR2`, `UR3` |

The dataset length is the total number of DoFs of that node, including constrained DoFs.
Constrained components are present in both datasets.
They are zero in `N<tag>` because the mode shape vanishes at a restrained DoF, while in `F<tag>` they contain the corresponding reaction and are generally nonzero.
For example, in a two-dimensional model every node stores two rows, `[U1, U2]`; the `U1` component is row 0 and the `U2` component is row 1.
Note that Python uses zero-based indexing.

This layout means that all nodal mode-shape data are available without knowing the global equation numbering.
It also means that the row order must be interpreted together with the element types that activate the node DoFs.
If only a single translational direction is of interest, it is often convenient to use a model in which that direction is the first local DoF, as in the example below.

## Reading the Data

The following snippet reads all modal properties from a file written by recorder tag `1` for direction `U1`.

```python
import h5py
import numpy as np

with h5py.File('R1-Modal.h5', 'r') as file:
    frequency = file['Frequency'][()].ravel()
    participation = file['U1/ParticipationFactor'][()].ravel()
    effective_mass = file['U1/EffectiveMass'][()].ravel()

    # node 2 contributes rows [U1, U2] in a two-dimensional model
    mode_shape = np.column_stack([
        file[f'Mode {mode + 1}/N2'][()].ravel()[0]
        for mode in range(frequency.size)
    ])
```

For a two-dimensional model, `N2[0]` is the `U1` mode-shape component of node 2 and `N2[1]` is the `U2` component.

## Relation to the Eigen Recorder

The [Eigen recorder](Recorder.md) writes the raw eigenvalues and eigenvectors to `Eigenvalue.h5`.
The `Modal` recorder writes a separate file with the processed modal quantities.
Both recorders can be defined in the same analysis if the raw eigenvectors are also needed.

## Example

A complete worked example, including post-processing, modal combination and validation against a response history analysis, is given in [modal analysis of a shear building](../../Example/Structural/Dynamics/modal-analysis-of-a-shear-building.md).
