# load

The `load` command is used to create loads applied on nodes.

Currently, concentrated node based loads can be applied in terms of force, displacement and acceleration. Given that 
all external forces are eventually converted to concentrated nodal forces, commands for distributed load patterns 
may not be available in the foreseeable future.

All loads are initialised and processed in **parallel** via global mutexes.

## Syntax

All loads share a similar syntax:

```text
load <load_type> <unique_tag> <arguments that define the specific load...>
```

### Nodal Load

To apply loads on nodes,

```text
# to apply nodal concentrated force
cload (1) (2) (3) (4) (5...)
load cload (1) (2) (3) (4) (5...)
# to apply nodal displacement
displacement (1) (2) (3) (4) (5...)
load displacement (1) (2) (3) (4) (5...)
# (1) int, unique tag
# (2) int, amplitude tag, 0 to use a default `Ramp` amplitude
# (3) double, nominal magnitude
# (4) int, dof tag
# (5...) int, node tags

# to apply nodal acceleration
acceleration (1) (2) (3) (4) [5...]
load acceleration (1) (2) (3) (4) [5...]
# (1) int, unique tag
# (2) int, amplitude tag, 0 to use a default `Ramp` amplitude
# (3) double, nominal magnitude
# (4) int, dof tag
# [5...] int, node tags
```

The keyword `cload` is the abbreviation for **c**oncentrated **load**.

### Body Force

Some elements support body force. Indications are given for elements that support body force in the corresponding pages.

```text
bodyforce (1) (2) (3) (4) (5...)
load bodyforce (1) (2) (3) (4) (5...)
# (1) int, unique tag
# (2) int, amplitude tag, 0 to use a default `Ramp` amplitude
# (3) double, nominal magnitude
# (4) int, dof tag
# (5...) int, element tags
```

### Load Applied To Node/Element Groups

To apply loads on groups,

```text
# on node groups
groupcload (1) (2) (3) (4) (5...)
groupdisplacement (1) (2) (3) (4) (5...)
load groupcload (1) (2) (3) (4) (5...)
load groupdisplacement (1) (2) (3) (4) (5...)

# on element groups
groupbodyforce (1) (2) (3) (4) (5...)
load groupbodyforce (1) (2) (3) (4) (5...)

# (1) int, unique tag
# (2) int, amplitude tag, 0 to use a default `Ramp` amplitude
# (3) double, nominal magnitude
# (4) int, dof tag
# (5...) int, group tags
```

### Support Excitation

For response history analysis, sometimes it is necessary to apply excitations on supports. The multi-support excitation
is automatically supported if analysts assign different excitations to different supports.

```text
supportdisplacement (1) (2) (3) (4) (5...)
supportvelocity (1) (2) (3) (4) (5...)
supportacceleration (1) (2) (3) (4) (5...)
load supportdisplacement (1) (2) (3) (4) (5...)
load supportvelocity (1) (2) (3) (4) (5...)
load supportacceleration (1) (2) (3) (4) (5...)
# (1) int, unique tag
# (2) int, amplitude tag, 0 to use a default `Ramp` amplitude
# (3) double, nominal magnitude
# (4) int, dof tag
# (5...) int, node tags
```

Essentially, `supportdisplacement`, `supportvelocity` and `supportacceleration` are all implemented as displacement
loads, thus displacement controlled scheme is automatically enabled.

Although it is designed to be used in response history analysis, it can also be used to apply acceleration/velocity on
any nodes (not only supports).

### Uniformly Distributed Load (UDL)

```text
lineudl2d (1) (2) (3) (4) (5...)
lineudl3d (1) (2) (3) (4) (5...)
load lineudl2d (1) (2) (3) (4) (5...)
load lineudl3d (1) (2) (3) (4) (5...)
# (1) int, unique tag
# (2) int, amplitude tag, 0 to use a default `Ramp` amplitude
# (3) double, nominal magnitude
# (4) int, dof tag
# (5...) int, node tags
```

### Reference Load

For arc-length analysis, reference load can be defined via the `RefForce` command.

```text
refforce (1) (2) (3) (4) (5...)
refload (1) (2) (3) (4) (5...)
load refforce (1) (2) (3) (4) (5...)
load refload (1) (2) (3) (4) (5...)
# (1) int, unique tag
# (2) int, amplitude tag, has no effect in arc-length analysis, just a placeholder, can be set to 0
# (3) double, reference magnitude
# (4) int, dof tag
# (5...) int, node tags
```

## Remarks

1.  The leading `load` keyword can often be omitted for simplicity.
2.  The `acceleration` is by default applied to all active nodes in the model if `[5...]` is not assigned.
3.  The true load magnitude is the product of nominal magnitude and amplitude. This is similar to ABAQUS.
4.  The multipoint displacement control algorithm [`MPDC`](../../Library/Solver/MPDC.md) is automatically enabled if
    a `displacement` or `groupdisplacement` is used.
5.  Optionally, the displacement can be applied by using [`MPC`](../../Library/Constraint/MPC.md) constraint.
6.  The multipoint displacement control algorithm [`MPDC`](../../Library/Solver/MPDC.md) is automatically enabled if
    a `supportdisplacement`, `supportvelocity` and/or `supportacceleration` are used.

**It must be noted that nodal displacement loads are only valid for one single step.** This means, if a displacement 
load is defined within a step, it will be activated for that step only.

All other load types will stay active once they are activated.
