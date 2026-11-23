# node

Nodes are basic components in FE models.
The `node` command constructs nodes.

## Syntax

```text title="node"
node (1) [2...]
# (1) int, unique tag
# [2...] double, coordinates
```

## Usage

A unique tag is required to identify different nodes.
The tag must be an unsigned integer; negative values are not allowed.
Although zero is a valid tag, it is recommended to number nodes starting from one.
It is not recommended to use an arbitrarily large tag, although the maximum tag is about four billion (`unsigned int`).
An unnecessarily large node tag may lead to excessive memory allocation because some functions create matrices sized by the largest node tag to ensure all nodes can be stored.

There is no limit on the dimension of a node.
A trivial node (without a location) can be defined as follows.
Such a node is generally not used to define elements.

```
node 1
```

Nodes with different dimensions can coexist.

```
node 1
node 2 2. 0.
node 3 0.
node 4 9. 8. 7. 1.
```

During initialisation, the dimension of each node is checked to ensure that the connected elements can work properly.
Any excess dimensions are ignored, but not discarded, during analysis.
For example, consider a 2D analysis with the following snippet.

```
node 1 3.
node 2 2. 1.
# later define a 2D element connecting node 1 and node 2
```

The dimension of node 1 is automatically expanded to two with zero filling.
Node 1 then represents $$(3.0,0.0)$$ in the 2D space.
If, on the other hand, a 1D analysis is performed, the second coordinate is ignored.

It is still recommended to define nodes with proper coordinates.
Generating a node list from an ABAQUS input file is straightforward.

## Output Types

The following quantities can be recorded using the commands similar to `plainrecorder 1 Node (output_type) (nodes...)`.


| variable label               | physical meaning              |
|------------------------------|-------------------------------|
| U                            | all displacement components   |
| U1, U2, U3, UR1, UR2, UR3    | displacement along each DoF   |
| V                            | all velocity components       |
| V1, V2, V3, VR1, VR2, VR3    | velocity along each DoF       |
| A                            | all acceleration components   |
| A1, A2, A3, AR1, AR2, AR3    | acceleration along each DoF   |
| RF                           | all resistance components     |
| RF1, RF2, RF3, RM1, RM2, RM3 | resistance along each DoF     |
| DF                           | all damping force components  |
| DF1, DF2, DF3, DM1, DM2, DM3 | damping force along each DoF  |
| IF                           | all inertial force components |
| IF1, IF2, IF3, IM1, IM2, IM3 | inertial force along each DoF |

### Remarks

1. For static analysis, normally only displacement `U` and resistance `RF` are activated.
   Recording other quantities therefore returns trivial results.
2. If the required quantity is not active, the output is empty.
3. The damping and inertial forces are collected from all elements in the model.
   It **must** be noted that the recorded values do **not** include contributions that do not stem from elements.
   For example, the damping force given by global damping models cannot be split among individual elements, so it is not reflected in the nodal damping force.
   This design is necessary because one may wish to separate contributions from various sources.
4. To record **global** damping and inertial forces that account for the total force, use `GDF`, `GDF1`, `GDF2`, `GDF3`, `GDF4`, `GDF5`, `GDF6`, `GIF`, `GIF1`, `GIF2`, `GIF3`, `GIF4`, `GIF5` and `GIF6`.
   These stand for global damping force and global inertial force.
