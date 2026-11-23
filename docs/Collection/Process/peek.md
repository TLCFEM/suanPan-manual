# peek

The `peek` command prints predefined information.
It has no effect if global screen output is switched off.

## Syntax

```text title="peek"
peek node (1)
peek element (1)
peek material (1)
peek constraint (1)
peek recorder (1)
peek solver (1)
peek integrator (1)
peek group (1)
peek nodegroup (1)
peek amplitude (1)
peek expression (1)
# (1) int, object tag

peek eigenvalue
peek output_folder
peek num_threads
peek num_nodes
peek statistics
peek stats
```

`peek nodegroup` prints every node contained in the given group.

`peek output_folder` prints the current output folder.

`peek num_threads` and `peek num_nodes` print the current thread and node counts.

`peek statistics` (or `peek stats`) prints accumulated timings for the major analysis phases.
