# Constraint

There are a number of different approaches to implement constraints in a FEM context. Interested readers can check
out the relevant documentations of ABAQUS,
or [this](https://mashayekhi.iut.ac.ir/sites/mashayekhi.iut.ac.ir/files//files_course/lesson_16.pdf)
slides for a brief introductory summary on linear constraints.

## Overview

Not all approaches are suitable for general applications. Accounting for efficacy and universality, the [penalty
function method](https://en.wikipedia.org/wiki/Penalty_method) and
the [Lagrange multiplier method](https://en.wikipedia.org/wiki/Lagrange_multiplier)
are implemented for most constraints.

Both methods do not alter the size of the system, or, in other words, they retain/reuse the unconstrained system.
Consequently, there is no need to reallocate memory for the constrained system.

Generally speaking, the penalty function method directly modifies the unconstrained system by introducing penalty
factors into the system. The larger the penalty factor, the more strictly the constraint is enforced. However, the
system tends to become ill-conditioned with large penalty factors.

The Lagrange multiplier method uses the border matrices to exactly enforce the constraint. The solving cost is
higher than the penalty function method, as it is not known in advance if the specific constraint (especially the
inequality constraints) should be active or not before the unconstrained system is solved.

## Difference Between Two Methods With Examples

Here we show a very simple example to illustrate the difference between the two methods. The homogeneous Dirichlet
type boundary condition (`fix` and `fix2`) is used.

The following model defines a simple elastic cantilever beam subjected to end load. The size of the system shall be
$$6$$ (three DoFs per node with two nodes). The fixed end is constrained so three DoFs are constrained, one DoF is
loaded and the other two are free.

```text
node 1 0 0
node 2 1 0
material Elastic1D 1 10
element EB21 1 1 2 12 1 1

# use penalty function method
fix 1 P 1

# to change penalty factor
# set constraint_multiplier 1E12

# to use Lagrange multiplier method
# fix2 1 P 1

cload 1 0 10 2 2
step static 1 1
set ini_step_size 1
set fixed_step_size true
converger RelIncreDisp 1 1E-11 5 1
analyze
exit
```

### Penalty Function Method

The `fix` command implements the penalty function method, the default penalty factor is $$10^8$$. The analysis
results can be shown as follows.

```text
current analysis time: 1.00000.
relative incremental displacement error: 1.00000E+00.
relative incremental displacement error: 3.10087E-09.
relative incremental displacement error: 2.27111E-16.
```

Although it is an elastic model, it still requires three iterations to converge. Since the default penalty factor is
$$10^8$$, each iteration will have an inherent error around $$10^{-8}$$. Thus the second iteration gives a relative 
error of $$3.10087\times10^{-9}$$.

#### Control the Penalty Factor

To enforce stronger/weaker constraints, it is possible to use a larger penalty factor via the `set` command. For
example,

```text
set constraint_multiplier 1E3
```

```text
current analysis time: 1.00000.
relative incremental displacement error: 1.00000E+00.
relative incremental displacement error: 3.10428E-04.
relative incremental displacement error: 3.44025E-07.
relative incremental displacement error: 4.33029E-10.
relative incremental displacement error: 5.48739E-13.
```

Or stronger such as,

```text
set constraint_multiplier 1E12
```

```text
current analysis time: 1.00000.
relative incremental displacement error: 1.00000E+00.
relative incremental displacement error: 3.09916E-13.
```

This is the inherent behaviour of the penalty function method. For nonlinear analysis, it is not a concern. For 
linear elastic analysis, additional iterations are required to converge.

### Lagrange Multiplier Method

The `fix2` command implements the Lagrange multiplier method. With which,

```text
fix2 1 P 1
```

The corresponding iteration results are shown as follows.

```text
current analysis time: 1.00000.
relative incremental displacement error: 1.00000E+00.
relative incremental displacement error: 4.92673E-17.
```

It can be seen that the constraint is exactly satisfied as the relative error is smaller than the machine error 
(`DBL_EPSILON` is typically around $$2\times10^{-16}$$).
