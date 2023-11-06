# node

Nodes are basic components in FE models. The `node` command is used to construct nodes.

## Syntax

```
node (1) [2...]
# (1) int, unique tag
# [2...] double, coordinates
```

## Usage

A unique tag is required to identify different nodes. The tag shall be an unsigned integer, negative values are not
allowed. Although zero is a valid tag, it is suggested to label nodes starting with one. It is not recommended to use
arbitrarily large tag for any nodes, although the maximum tag is about four billion (`unsigned int`). Any unnecessarily
large node tag may lead to memory leakage as some functions create matrix depending on the largest node tag to ensure
all nodes could be stored.

There is no limitation on the dimension of the node defined.
A trivial node (without a location) can be defined as follows.
Such a node will not be used to define elements in general cases.

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

In fact, during initialisation, the dimension of each node will be double-checked to ensure the connected elements could
work properly. Meanwhile, excessive dimensions would be ignored (but not discarded) during analysis. If for example one
is performing a 2D analysis and the model contains the following snippet.

```
node 1 3.
node 2 2. 1.
# later define a 2D element connecting node 1 and node 2
```

The dimension of node 1 will be automatically expanded to two with zero filling,
so node 1 represents node $$(3.0,0.0)$$ in the 2D space.
If, on the other hand, an 1D analysis is performed, then the second coordinate will be ignored.

It is still recommended defining nodes with proper coordinates. Generating a node list from ABAQUS input file is an easy
task.

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

1. For static analysis, normally only displacement `U` and resistance `RF` are activated. Thus, recording other 
   quantities returns trivial results.
2. If the required quantity is not active, the output will be empty.
3. The damping and inertial forces are collected from all the elements in the model. It **must** be noted that the 
   recorded values do **not** include any contributions that do not stem from elements. For example, the damping 
   force given by global damping models cannot be split to individual elements; thus it is not reflected in the 
   nodal damping force. This design is necessary as one may wish to separate contributions from various sources apart.
4. To record **global** damping and inertial forces that account for the total force, use `GDF`, `GDF1`, `GDF2`, 
   `GDF3`, `GDF4`, `GDF5`, `GDF6`, `GIF`, `GIF1`, `GIF2`, `GIF3`, `GIF4`, `GIF5`, `GIF6`, which stand for global 
   damping force and global inertial force.
