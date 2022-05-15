# Constraint

In this article, the formulation and implementation of constraints, both single-point and multipoint types, are briefly
discussed.

## Penalty Method

### Theory

### Implementation

The easiest approach to implement the constraint with penalty method is to treat the constraint as a special element.

## Lagrange Multiplier Method

### Theory

In the most general form, a minimisation problem of function $$f(x)$$ subjected to equality constraint $$g(x)$$ can be
expressed as

$$
\text{minimise}~f(x)~\text{subjected to}~g(x)=0.
$$

It can be converted to the Lagrangian function so that the target is to find the stationary points of

$$
L(x,\lambda)=f(x)+\lambda^\mathrm{T}g(x).
$$

Either linear or nonlinear constraints can be applied.

For finite element analysis, $$f(x)$$ is normally the strain energy $$W(u)$$ so that

$$
\dfrac{\partial{}W(u)}{\partial{}u}=R(u),
$$

which would be resistance.

Thus, the stationary condition leads to the following nonlinear system.

$$
R(u)+\lambda^\mathrm{T}\dfrac{\mathrm{d}g}{\mathrm{d}u}=0,\qquad g=0.
$$

Linearisation gives the Jacobian to be

$$
J=\begin{bmatrix} K&\dfrac{\mathrm{d}g}{\mathrm{d}u}^\mathrm{T}\\ \dfrac{\mathrm{d}g}{\mathrm{d}u}&0 \end{bmatrix}+
\begin{bmatrix} \displaystyle\sum_{i=1}^{n}\lambda_i\dfrac{\mathrm{d}^2g_i}{\mathrm{d}u^2}&0\\0&0 \end{bmatrix},
$$

where $$K$$ is the tangent stiffness of the unconstrained system.

### Implementation

From the formulation, it is clear that the general implementation of Lagrange multiplier method requires two main parts,
namely the Hessian matrix and the gradient of constraints $$g_i$$.

For the Hessian matrix, it can be treated as the corresponding stiffness matrix of the element that connects the nodes
on which the constraint is applied. It can be computed locally and assembled into global stiffness matrix with other
conventional elements.

For the gradient, it is normally stored separately in the so-called border matrix. In a system with multiple constraints
defined, the number of active constraints may differ from step to step, especially with the presence of inequality
constraints. Thus, the border matrix, and the corresponding constraint residual (for nonlinear constraints), shall be
stored locally and later be used to formulate the corresponding global variables in each iteration.

To consider linear constraints only, the implementation can be greatly simplified. But its applicability would be
confined.