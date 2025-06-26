# The Very First Analysis

This page aims to show an overview of how a model looks like by establishing a simple model, which is a simple elastic
cantilever beam subjected to an end load.

A native C++ parser is used by `suanPan`.
The default syntax resembles the one of `OpenSees`.
Model files are written in plain text.
Although there is no restriction, the suffix `.supan` is reserved by default.

The line starts with the hash symbol (`#`) or the exclamation symbol (`!`) is a comment line.
To write one command spans a few lines, please use backslash (`\`) to concatenate multiple lines.
Please refer to [Syntax](Syntax.md) for details.

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

Since each command is commented, there is not much to explain.
This model is similar to the one created by the `example` command, both are simple one element models.
The output is directly printed on screen by default. For this model, it is

```
+--------------------------------------------------------+
|             ____             suanPan is an open source |
|   ___ _   _|  _ \ __ _ _ __     FEM framework (64-bit) |
|  / __| | | | |_) / _` | '_ \           Canopus (3.8.0) |
|  \__ \ |_| |  __/ (_| | | | |        by tlc @ 236da9bc |
|  |___/\__,_|_|   \__,_|_| |_|      all rights reserved |
|                                 10.5281/zenodo.1285221 |
+--------------------------------------------------------+
|  🧮 https://github.com/TLCFEM/suanPan                  |
|  📚 https://tlcfem.github.io/suanPan-manual/latest     |
+--------------------------------------------------------+
|  🎧 https://bit.ly/vsc-sp                              |
+--------------------------------------------------------+

>> Current Analysis Time: 1.00000.

Node 2:
Coordinate:
  1.3400e+00  0.0000e+00
Displacement:
  2.3926e-02  2.0476e-02  2.2921e-02
Resistance:
  1.7000e+01  2.3000e+01 -2.4633e-07


Time Wasted: 0.0029 Seconds.
```

The analytical solution of horizontal tip displacement is

$$
u=\dfrac{PL}{EA}=\dfrac{17\times1.34}{132\times7.213}=0.023926.
$$

The analytical solution of vertical tip displacement is

$$
v=\dfrac{PL^3}{3EI}=\dfrac{23\times1.34^3}{3\times132\times6.835}=0.020476.
$$
