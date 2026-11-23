# expression

The `expression` command defines mathematical expressions that can later be used to customise relevant material models.

The command parses a block of plain text into mathematical expressions.
The parsing and evaluation functionality is powered by [`exprtk`](https://github.com/ArashPartow/exprtk).

`exprtk` generates an AST from the input text.
The evaluation of the expression has performance on par with native C++ code.

A customisable expression, however, allows more flexibility and makes it easier to experiment with different functions.

## Syntax

### Simple Scalar-valued Expression

```text title="SimpleScalar"
expression SimpleScalar (1) (2) (3)
# (1) int, unique expression tag
# (2) string, input variable list
# (3) string, expression string or name of file containing expression
```

This evaluates a scalar-valued function $$f(x_1,x_2,\cdots,x_n)$$.
The input arguments can be either scalars or vectors.
For example, `"x_1|2|x_2"` represents two variables: 1) $$x_1$$ is a vector of size 2 and 2) $$x_2$$ is a scalar.
The function value is returned as a result.
For example, the expression can be $$x_1^2+x_2^2$$.

This form ***supports*** automatic computation of derivatives.
Thus, it can be used in models that require automatic computation of derivatives.

### Simple Vector-valued Expression

```text title="SimpleVector"
expression SimpleVector (1) (2) (3) (4)
# (1) int, unique expression tag
# (2) string, input variable list
# (3) string, output variable list
# (4) string, expression string or name of file containing expression
```

This evaluates a vector-valued function $$y:=f(x_1,x_2,\cdots,x_n)$$.
An assignment must be used to explicitly assign values to the output variables.
The input arguments can be either scalars or vectors.
The output argument should be a vector; the size shall be given such that `"y|3"` represents a vector of size 3.

This form ***does not support*** automatic computation of derivatives.
Thus, it ***cannot*** be used in models that require automatic computation of derivatives.

## Remarks

1. The variables in the expression must be explicitly given as arguments.
   They can be unquoted or enclosed in double quotes `"`.
2. Multiple variables must be separated by a vertical bar `|`.
3. The expression can be given as a string or as a file name.
   The program tries to load the file first.
   If the file does not exist, the program tries to parse the string as an expression.
4. No whitespace (including `,` and ` `) is allowed in any argument.

`exprtk` provides powerful functionality.
Logical operations and control flow can be used in an expression.

## Example

For example, consider a uniaxial nonlinear elastic model with the following stress-strain relationship:

$$
\sigma=\varepsilon^3+\varepsilon
$$

The expression can then be defined as

```text
expression SimpleScalar 1 x x^3+x
```

Here, `x` is used as the free variable and the corresponding expression is `x^3+x`.

For the uniaxial nonlinear elastic model, the input is strain, which maps to `x`.
The output maps to stress.

Alternatively, the expression can be stored in a file and loaded by the program.

```text title="cubic.txt"
x^3+x
```

The expression can then be defined as

```text
expression SimpleScalar 1 x cubic.txt
```

For complex expressions, using a file is more convenient.

To use the expression, the [`CustomElastic1D`](../../Library/Material/Material1D/Elastic/CustomElastic1D.md) model is used here.

```text
# using expression 1
material CustomElastic1D 1 1

materialTest1D 1 1E-2 200

exit
```

The response can be tested with the [material tester](../Process/materialtest.md).

## Result

![cubic response](expression.svg)
