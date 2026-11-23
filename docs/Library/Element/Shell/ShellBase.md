# ShellBase

The `ShellBase` class is a base class for all shell elements.
It provides basic methods to convert displacement from global to local, or convert resistance and stiffness from local to global.

## Background

Each shell node has six DoFs: three membrane components and three plate components.
`ShellBase` derives the local direction cosines from the element geometry and assembles the membrane and plate contributions into the full element resistance and stiffness.
In a nonlinear geometry analysis the transformation is recomputed from the trial displaced shape.

## Remarks

`ShellBase` is not a user-instantiable element and has no `element ShellBase` command.
Use one of its derived elements instead: [`DKTS3`](DKTS3.md), [`S4`](S4.md) or [`SGCMS`](SGCMS.md).
