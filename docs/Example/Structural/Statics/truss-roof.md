# [★☆☆☆☆] Linear Analysis of A Truss Roof

The model can be downloaded. [truss-roof.zip](truss-roof.zip)

## Model

### Node

A 2D truss model is developed. To define nodes, use the [`node`](../../../Collection/Define/node.md) command. As this is
a 2D model, each node is defined by two coordinates, thus the command looks like this: `node <tag> <x> <y>`.

```text
# file: node
node  1 15  0
node  2 15  7
node  3 20  7.5
node  4 25  0
node  5 30  0
node  6 35  0
node  7 35  4
node  8 30  6
node  9 25  7
node  10  10  0
node  11  5 0
node  12  5 4
node  13  10  6
node  14  0 0
node  15  20  0
node  16  40  0
```

Here we define 16 nodes. The truss roof has a span of 40 and an apex height of 7.5.

### Element

To model truss elements, we use the [`T2D2`](../../../Library/Element/Truss/T2D2.md) element. (Yes! The same designation
as in ABAQUS!)

```text
# file: element
element T2D2 1 1 2 1 0.2 ! element 1 connecting nodes 1 and 2 using material 1 with cross-sectional area 0.2
element T2D2 2 3 2 1 0.2
element T2D2 3 4 3 1 0.2
element T2D2 4 5 4 1 0.2
element T2D2 5 6 5 1 0.2
# ...
```

Here the first five elements are shown. The cross sectional area can be directly specified
with [`T2D2`](../../../Library/Element/Truss/T2D2.md). Alternatively, the truss section can be built up manually using
basic shapes, see the [`T2D2S`](../../../Library/Element/Truss/T2D2S.md) element for details.

You may have noticed that the material model used is not defined. Do not worry, for model definitions, the order is not
important, see [Structure](../../../Basic/Structure.md) for explanation.

### Load and BC

Definitions of nodes and elements are stored in files `node` and `element`. We load it first
using [`file`](../../../Collection/Define/file.md) command.

```text
# file: truss-roof.supan
file node
file element
```

For material, we simply define an elastic [`Elastic1D`](../../../Library/Material/Material1D/Elastic/Elastic1D.md)
material with a Young's modulus of $$3E4$$.

```text
# file: truss-roof.supan
material Elastic1D 1 30E3
```

The left-most node `14` is fixed, while the right-most node `16` is roller supported. This means for node `14`, both x
and y displacements are fixed, while for node `16`, only y displacement is fixed. One can use
either [`fix`](../../../Collection/Define/bc.md) (penalty method) or [`fix2`](../../../Collection/Define/bc.md)
(multiplier method) to apply homogeneous boundary conditions. Both shall lead to the same result.

```text
# file: truss-roof.supan
fix2 1 1 14 ! fix x-displacement (dof 1) of node 14
fix2 2 2 14 16 ! fix y-displacement (dof 2) of nodes 14 and 16
```

For load, we apply a vertical [`displacement`](../../../Collection/Define/load.md) load on top of the apex.

```text
# file: truss-roof.supan
displacement 1 0 -1 2 3 ! a displacement load with tag 1 on node 3 dof 2 (vertical) with a magnitude of -1
```

The second parameter `0` is a placeholder for [`amplitude`](../../../Collection/Define/amplitude.md), a `0` means a
default [`Ramp`](../../../Library/Amplitude/Universal/Linear.md) is used.

### Analysis

A simple static step is required to analyse the model.

```text
# file: truss-roof.supan
step static 1
set ini_step_size 1
set fixed_step_size true

analyze ! perform analysis
```

### Probe Result

It is possible to probe the simple results of the analysis, for example, one can check the displacement and resistance
of node `3` by using the [`peek`](../../../Collection/Process/peek.md) command. To record various results, one may want
to use [`recorder`](../../../Collection/Define/recorder.md) command.

```text
peek node 3
```

The following printout shall be expected.

```text
Node 3:
Coordinate:
   20.0000    7.5000
Displacement:
   0.2238  -1.0000
Resistance:
  -1.7053e-13  -7.4093e+01
```

### Bye

Do not forget to quit.

```text
exit
```

## Results

The deformation is shown.

![deformation of truss roof](truss-roof.png)
