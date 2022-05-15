# Linear Analysis of A Single Element

In this example, we show a very basic analysis using isogeometric analysis and compare the result with the traditional
finite element analysis.

The model can be downloaded here [linear-analysis-of-a-single-element.zip](linear-analysis-of-a-single-element.zip).

## Geometry

We analyze a single quadrilateral element with arbitrary lengths of edges. For traditional finite element analysis that
uses isoparametric mapping, it is required to define four nodes that represent the vertexes of the quadrilateral. For
example,

```
# FEA
node 1 0 0
node 2 .5 0
node 3 .75 1
node 4 0 1
```

For isogeometric analysis, the geometry is controlled by the control nodes, which form control polygon in higher
dimensions. Since NURBS is used, for each control node, a weight shall be assigned. This means for an $$n$$ dimensional
problem, the control nodes shall have size of $$n+1$$. In this 2D example, we use the same `node` command to define
control nodes, the size shall be handled properly.

```
# IGA
node 1 0 0 1
node 2 .5 0 1
node 3 .75 1 1
node 4 0 1 1
```

Here we use unity for all four nodes. For the geometry (linear) considered, NURBS falls back to B-Spline, which is
sufficient.

## Element

In FEA, each element is defined by the nodes ordered anticlockwise. So to define a `CP4` element with unit thickness and
material model with tag $$1$$, the following command can be used.

```
# FEA
element CP4 1 1 2 3 4 1 1
```

In IGA, a different strategy is used. Each patch that consists of a number of elements is considered as a giant element,
hence the number of control nodes is not known in advance. Meanwhile, the knot vectors may have various lengths.
In `suanPan`, a key-value style definition is used. Please refer to the corresponding page for more details
of `PatchQuad` element. In this example, the following command is used. Please note the order of control nodes is
different from that in FEA.

```
element PatchQuad 1 -node 1 2 4 3 -material 1 -thickness 1 -knotx 0 0 1 1 -knoty 0 0 1 1
```

## Other Parts

The rest of the model is pretty simple, as long as BCs and loads are defined, the model is ready to be analyzed.

```
fix 1 1 1
fix 2 2 1 2
cload 1 0 1 2 3 4
step static 1
analyze
exit
```