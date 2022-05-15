# Triple Pendulum

The model can be downloaded [here](triple-pendulum.supan).

## Model

First to define the nodes and the corresponding truss elements and point masses. The first node is pinned so that it
does not move.

```
node 1 0 0
node 2 0 -2
node 3 0 -3
node 4 0 -5

material Elastic1D 1 1E7

element T2D2 1 1 2 1 1 true
element T2D2 2 2 3 1 1 true
element T2D2 3 3 4 1 1 true

element Mass 4 2 20 1 2
element Mass 5 3 10 1 2
element Mass 6 4 20 1 2

fix2 1 P 1
```

An initial velocity is assigned to the third node (the second mass).

```
initial velocity 25 1 3
```

The gravity load is assigned in form of constant force.

```
amplitude Constant 1
cload 1 1 -200 2 2
cload 2 1 -100 2 3
cload 3 1 -200 2 4
```

The analysis is performed with the Newmark integration method.

```
step dynamic 1 100
set ini_step_size 1E-3
set fixed_step_size 1
set symm_mat 0

integrator Newmark 1

converger AbsIncreDisp 1 1E-10 10 1

analyze
```

## Results

The animation is presented as follows.

![animation](triple-pendulum.gif)