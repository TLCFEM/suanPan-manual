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

<iframe src="https://www.desmos.com/calculator/uvmdtncok7?embed" width="800" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

Such a failure pattern could commonly happen for hardening materials under cyclic loading.

In the following example, we define a bilinear hardening material with $1\%$ hardening.
A cyclic load (loading and unloading) is applied to a truss element.
The complete script can be [downloaded](advanced-solver.zip).

```text hl_lines="4 11 13"
node 1 0 0
node 2 1 0

material Bilinear1D 1 2E5 200 0.01

element T2D2 1 1 2 1 1

fix2 1 1 1
fix2 2 2 1 2

amplitude Tabular 1 cyclic

cload 1 1 50 1 2

step static 1 2
set fixed_step_size 1
set ini_step_size 2E-2
set symm_mat 0

converger RelIncreDisp 1 1E-10 20 1

analyze

exit
```

With the default Newton solver, the analysis will fail to converge in the first unloading step.

```text hl_lines="13-16"
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

### AICN

More advanced methods based on the Newton-Raphson method have been developed.
Two main categories are available: damped methods and regularization methods.
The damped methods scale the increment of each iteration to improve the convergence.
The regularization methods add a regularization term to the tangent stiffness matrix.
These two techniques can be further combined.

[arXiv.2211.00140](https://doi.org/10.48550/arXiv.2211.00140) proposed a very interesting method that only requires damping.
The algorithm has been implemented as the [AICN](../../Library/Solver/AICN.md) solver.
It requires a proper estimation of the Lipschitz constant of the residual function.
Here we choose $$20$$.

```text
solver AICN 1 20
```

Running the analysis again, convergence is achieved in the first unloading step after struggling for a few iterations.
The quadratic convergence rate is recovered when the iteration starts to converge.

```text hl_lines="11-15"
>> Current Analysis Time: 1.02000.
--> Relative Incremental Displacement: 1.00000E+00.
--> Relative Incremental Displacement: 2.93208E-01.
--> Relative Incremental Displacement: 3.37174E-01.
--> Relative Incremental Displacement: 3.94691E-01.
--> Relative Incremental Displacement: 4.71640E-01.
--> Relative Incremental Displacement: 5.75497E-01.
--> Relative Incremental Displacement: 7.08534E-01.
--> Relative Incremental Displacement: 8.27423E-01.
--> Relative Incremental Displacement: 7.31105E-01.
--> Relative Incremental Displacement: 3.01591E-01.
--> Relative Incremental Displacement: 3.44108E-02.
--> Relative Incremental Displacement: 4.23933E-04.
--> Relative Incremental Displacement: 6.42983E-08.
--> Relative Incremental Displacement: 3.90999E-14.
```

One may also notice that, for elastic steps, the AICN algorithm requires more iterations.
This is reasonable because the introduction of damping changes the increment, which happens to be the exact solution in the elastic step.
This is typically not a concern in the context of non-linear analysis.

The AICN algorithm guarantees the global quadratic convergence.

### L-BFGS

Another general-purpose solver that can be utilised is the [L-BFGS](../../Library/Solver/BFGS.md) solver.
It is a quasi-Newton method that does not require exact Hessians.
The trade-off is that it only possesses a super-linear convergence rate.

However, it circumvents the shortcomings of the Newton-Raphson method.

```text
solver LBFGS 1
```

Running the analysis again, the L-BFGS solver converges in the first unloading step.

```text hl_lines="4-6"
>> Current Analysis Time: 1.02000.
--> Relative Incremental Displacement: 1.00000E+00.
--> Relative Incremental Displacement: 6.18750E+01.
--> Relative Incremental Displacement: 1.47614E+00.
--> Relative Incremental Displacement: 3.57688E-01.
--> Relative Incremental Displacement: 3.19744E-14.
```

## Takeaways

1. It is perfectly normal for the Newton solver to fail to converge in some situations.
2. The advanced solvers, such as AICN and L-BFGS, can be used to overcome the convergence issue.

In specific, the Newton-Raphson method should typically converge when the response is "nice", for example, monotonic with non-trivial curvature.
If the quadratic convergence cannot be achieved in this specific case, then the local integration at material point level may be the culprit.

When the response is not "nice", for example, cyclic loading, softening, the Newton solver may fail to converge even when everything is implemented correctly.
In this case, one can either reduce the step size or use the advanced solvers.
