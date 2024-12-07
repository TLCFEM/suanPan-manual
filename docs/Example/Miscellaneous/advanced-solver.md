# Advanced Newton Solver

For force-controlled analyses, the Newton-Raphson method is the de facto standard method to find the solution of the system.
It works nicely when the initial guess is sufficiently close to the true solution and quadratic convergence rate is often guaranteed.
However, it can be proved that only the local convergence can be guaranteed.
The global convergence, on the other hand, is not achievable.

In this example, we demonstrate that the Newton solver may fail to converge in very common situations.
We will also show how to use the advanced solver to overcome the convergence issue.

## An Example of Failure

It is possible to click the right bottom corner of the plot to open the plot in a new tab.
You can also drag the initial guess (red dot) to see how the first four iterations go.

<iframe src="https://www.desmos.com/calculator/uvmdtncok7?embed" width="700" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

Such a failure pattern could commonly happen for hardening materials under cyclic loading.

In the following example, we define a bilinear hardening material with $1\%$ hardening.
The complete script can be (downloaded)[advanced-solver.zip].

```text
node 1 0 0
node 2 1 0

material Bilinear1D 1 2E5 200 0.01

element T2D2 1 1 2 1 1
```

With the default Newton solver, the analysis will fail to converge in the first unloading step.

```text
>> Current Analysis Time: 1.02000.
--> Relative Incremental Displacement: 1.00000E+00.
--> Relative Incremental Displacement: 1.01643E+00.
--> Relative Incremental Displacement: 6.18750E+01.
--> Relative Incremental Displacement: 1.01643E+00.
--> Relative Incremental Displacement: 6.18750E+01.
--> Relative Incremental Displacement: 1.01643E+00.
--> Relative Incremental Displacement: 6.18750E+01.
--> Relative Incremental Displacement: 1.01643E+00.
--> Relative Incremental Displacement: 6.18750E+01.
--> Relative Incremental Displacement: 1.01643E+00.
--> Relative Incremental Displacement: 6.18750E+01.
--> Relative Incremental Displacement: 1.01643E+00.
--> Relative Incremental Displacement: 6.18750E+01.
--> Relative Incremental Displacement: 1.01643E+00.
--> Relative Incremental Displacement: 6.18750E+01.
```

It appears that the iteration enters a stable infinite loop, bouncing back and forth between two points.
This is exactly the situation demonstrated in the plot above.

## Advanced Newton Solver

More advanced methods based on the Newton-Raphson method have been developed.
Two main categories are available: damped methods and regularization methods.
The damped methods scale the increment of each iteration to improve the convergence.
The regularization methods add a regularization term to the tangent stiffness matrix.
These two techniques can be further combined.

[arXiv.2211.00140](https://doi.org/10.48550/arXiv.2211.00140) proposed a very interesting method that only requires damping.
