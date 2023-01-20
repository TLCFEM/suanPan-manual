# Analyze

This page aims to show an overview of how a model looks like by establishing a simple model, which is a simple elastic
cantilever beam subjected to an end load.

A native CPP parser is used by `suanPan`. The default syntax resembles the one of `OpenSees`. Model files are written in
plain text. Although there is no restriction, the suffix `.supan` is reserved by default.

The line starts with the hash symbol (`#`) or the exclamation symbol (`!`) is a comment line. To write one command spans
a few lines, please use backslash (`\`) to concatenate multiple lines. Please refer to [Syntax](Syntax.md) for details.

```
# defines two nodes at (0,0) and (1.34,0)
node 1 0 0
node 2 1.34 0

# define an elastic material with the elastic modulus of 132
material Elastic1D 1 132

# define an (E)lastic (B)eam element 1 connecting node 1 and node 2 with A=7.213 and I=6.825 using material 1
element EB21 1 1 2 7.213 6.825 1

# fix all DoFs (P) of node 1
fix 1 P 1

# apply a load of magnitude 23 at DoF 2 of node 2
cload 1 0 23 2 2
# apply another load of magnitude 17 at DoF 1 of node 2
cload 2 0 17 1 2

# create a static step
step static 1

analyze

# print the state of node 2
peek node 2

exit
```

Since each command is commented, there is not much to explain. This model is similar to the one created by the `example`
command, both are simple one element models. The output is directly printed on screen by default. For this model, it is

```
+--------------------------------------------------+
|   __        __         suanPan is an open source |
|  /  \      |  \           FEM framework (64-bit) |
|  \__       |__/  __   __           Acrux (1.0.0) |
|     \ |  | |    |  \ |  |      maintained by tlc |
|  \__/ |__| |    |__X |  |    all rights reserved |
|                           10.5281/zenodo.1285221 |
+--------------------------------------------------+
|  https://github.com/TLCFEM/suanPan               |
|  https://github.com/TLCFEM/suanPan-manual        |
+--------------------------------------------------+
|  https://gitter.im/suanPan-dev/community         |
+--------------------------------------------------+

current analysis time: 1.00000.
Node 2:
   1.3400        0
Displacement:
   0.0239   0.0205   0.0229
Resistance:
   1.7000E+01   2.3000E+01  -3.0820E-07

Finished in 0.015 seconds.
```

The analytical solution of horizontal tip displacement is

$$
u=\dfrac{PL}{EA}=\dfrac{17\times1.34}{132\times7.213}=0.023926.
$$

The analytical solution of vertical tip displacement is

$$
u=\dfrac{PL^3}{3EI}=\dfrac{23\times1.34^3}{3\times132\times6.835}=0.020476.
$$
