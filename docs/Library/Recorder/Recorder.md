# Recorder

Record Model Response

The available output types are listed in [OutputType](OutputType.md) file.

To control the folders to which the recorder will write the output, please check [OutputFolder](OutputFolder.md) file.

Not all quantities at every time step need to be stored. Only those explicitly specified will be stored as history
output.

Currently, there are several types of recorders. Analysts can choose to record either **element response** at
integration points (strain, stress, etc., some elements support response at elemental nodes) or **nodal response** at
model nodes (displacement, velocity, acceleration, reaction, etc.). The third type supports the output of the summation
of the same quantity of several nodes/elements. Alternatively, analyst can recorder global quantities such as global
stiffness/mass, global kinetic energy, etc.

## Syntax

Two types of format are supported. The output file can be either plain text or HDF5 file if the program is compiled with
HDF5 support. The general form to define a record is as follows.

```
recorder (1) plain (2) (3) [every 4] [5...]
recorder (1) hdf5 (2) (3) [every 4] [5...]
# (1) int, unique recorder tag
# (2) string, recorder type
# (3) string, object type that needs to be recorded
# [4] int, optional argument with leading keyword "every" to indicate the interval of recording,
# for example: "every 10" means the recorder will record the response every ten converged substeps.
# [5...] int, tags of elements/nodes, etc.
```

Alternatively, it is possible to use the following two equivalences.

```
plainrecorder (1) (2) (3) [every 4] [5...]
hdf5recorder (1) (2) (3) [every 4] [5...]
```

There are some recorder types that do not need tags of elements/nodes as they record the response of the whole model.

## Eigen Recorder

```
# to record eigenvalues and eigenvectors if current step is an eigenanalysis step
recorder (1) plain Eigen
recorder (1) hdf5 Eigen
# (1) int, unique recorder tag
```

## Frame Recorder

```
# to record response of the whole model, this one only supports HDF5
recorder (1) hdf5 Frame (3) [every 4]
# (1) int, unique recorder tag
# (3) string, object type that needs to be recorded
# [4] int, optional argument with leading keyword "every" to indicate the interval of recording,
# for example: "every 10" means the recorder will record the response every ten converged substeps.
```

## Visualization Recorder

```
# to record response of the whole model and write to VTK files for visualisation, this one is enabled only with VTK support.
recorder (1) plain Visualisation (3) [every 4]
recorder (1) hdf5 Visualisation (3) [every 4]
# (1) int, unique recorder tag
# (3) string, object type that needs to be recorded
# [4] int, optional argument with leading keyword "every" to indicate the interval of recording,
# for example: "every 10" means the recorder will record the response every ten converged substeps.
```

The `Visualisation` will immediately write the disk with incremental file names.

## Node Recorder

To record nodal response,

```
recorder (1) plain Node (3) [every 4] [5...]
recorder (1) hdf5 GroupNode (3) [every 4] [5...]
# (1) int, unique recorder tag
# (3) string, object type that needs to be recorded
# [4] int, optional argument with leading keyword "every" to indicate the interval of recording,
# for example: "every 10" means the recorder will record the response every ten converged substeps.
# [5...] int, tags of nodes or node groups, etc.
```

If `GroupNode` is used, then the tags of node groups shall be used.

Nodal scalar response can be directly summed up by using the `Sum` recorder.

```text
recorder (1) plain Sum (3) [every 4] [5...]
recorder (1) hdf5 GroupSum (3) [every 4] [5...]
# (1) int, unique recorder tag
# (3) string, object type that needs to be recorded
# [4] int, optional argument with leading keyword "every" to indicate the interval of recording
# [5...] int, tags of nodes or node groups, etc.
```

It is handy to record the summation of nodal response, for example, the summation of nodal reaction force.

## Element Recorder

To record element response,

```
recorder (1) plain Element (3) [every 4] [5...]
recorder (1) hdf5 GroupElement (3) [every 4] [5...]
# (1) int, unique recorder tag
# (3) string, object type that needs to be recorded
# [4] int, optional argument with leading keyword "every" to indicate the interval of recording,
# for example: "every 10" means the recorder will record the response every ten converged substeps.
# [5...] int, tags of elements or element groups, etc.
```

If `GroupElement` is used, then the tags of element groups shall be used.

## Global Recorder

Sometimes, it is necessary to record global quantities.

Currently, it is possible to record energy quantities.

```
recorder (1) plain Global (3) [every 4]
recorder (1) hdf5 Global (3) [every 4]
# (1) int, unique recorder tag
# (3) string, object type that needs to be recorded
# [4] int, optional argument with leading keyword "every" to indicate the interval of recording,
# for example: "every 10" means the recorder will record the response every ten converged substeps.
```

The `(3)` can be:

1. `KE`: kinetic energy
2. `SE`: strain energy (potential energy)
3. `VE`: energy dissipated via viscosity
4. `NVE`: energy dissipated via non-viscosity
5. `MM`: momentum
6. `K`: global stiffness matrix, vectorised
7. `M`: global mass matrix, vectorised

For energy terms, the recorder records two quantities computed from different sources: the first column is the summation
of all corresponding energy terms collected from all valid elements; the second column is the global energy term.

The reason to have two different columns is to mainly account for the fact that some models/theories may impose global
level energy dissipation.

A very direct example is the global damping models used in seismic engineering. Take the `Rayleigh` model as an example.
Since it can be implemented in two ways, either apply linear combination of stiffness and mass at element level after
computing elemental stiffness and mass (see Rayleigh [`Modifier`](../Element/Modifier/Modifier.md)), or globally after
assembling global stiffness and mass (see [`RayleighNewmark`](../Integrator/Implicit/Newmark/RayleighNewmark.md)). If the former
is selected, each element can record its own energy dissipation term. If the latter is selected, the dissipated energy
can only be computed from global stored quantities.

Some other models cannot be applied at element level, resulting in missing energy if those energy terms are only
collected from elements.

As a rule of thumb, often two columns are equal to each other, if there is no global energy 'modifier'. Otherwise, there
would be a difference between two columns. Depending on whether the elemental energy or global energy is under
investigation, users can flexibly choose the columns to be compared.
