# Structure

The default parser accepts a **three-part** structure. They are:

1. Model Properties Setup
2. Analysis Properties Setup
3. Post-processing

The previous cantilever beam example is used here to explain the structure. The model is shown as follows.

```
node 1 0 0
node 2 1.34 0
material Elastic1D 1 132
element EB21 1 1 2 7.213 6.825 1
step static 1
fix 1 P 1
cload 1 0 23 2 2
cload 2 0 17 1 2
analyze
peek node 2
exit
```

## Model Properties Setup

Anything before the first `step` command is treated as the setup of model properties. This part may include the
definitions of nodes, elements, material models, loads, recorders, boundary conditions, etc. In this part, the order of
commands **does not** affect the establishment of the model. So that the following reshuffled command flow creates the
same model as the original one does, although, the `EB21` element is created before the creation of its connected nodes.

```
element EB21 1 1 2 7.213 6.825 1
node 2 1.34 0
material Elastic1D 1 132
node 1 0 0
```

When the program parses those commands, the corresponding objects are only created and stored, but not initialized (
viz., no other information is required during the creation of a particular object). So the order does not affect
anything in this part.

## Analysis Properties Setup

The command block between the first `step` command the `analyze` command (or the `precheck` command) is the setup of
analysis properties. A similar analysis flow which resembles the one of ABAQUS is used, that is, multiple steps can be
defined in sequence in this part.

In this example, within step 1, a fixed boundary condition is applied to node 1, two concentrated loads are applied to
node 2 along two directions. For the purpose of illustration, those two loads can be defined in two different steps as
follows.

```
fix 1 P 1
step static 1
cload 1 0 23 2 2
step static 2
cload 2 0 17 1 2
analyze
```

Now the horizontal load is created in step 2 that follows step 1. It shall be noted the BC is created before the first
step. By default, there is a step 0 with no step time, so the BC can be defined in either step 0 or step 1. Similar to
ABAQUS, the sequence of multiple steps will affect analysis results.

## Post-processing

The code block between the `analyze` command and the `exit` command belongs to post-processing. This part is less
concerning and most commands have instant response.
