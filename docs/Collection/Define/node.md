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

There is no limitation on the dimension of the node defined. A dummy node (without location) can be defined as follows.
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

The dimension of node 1 will be automatically expanded to 2 with zero filling so node 1 represents node $$(3.0,0.0)$$ in
the 2D space. If, on the other hand, an 1D analysis is performed, then the second coordinate will be ignored.

It is still recommended defining nodes with proper coordinates. Generating a node list from ABAQUS input file is an easy
task.
