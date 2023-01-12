# expression

The `expression` command can be used to define mathematical expressions that can be later used to customise relevant
material models.

The `expression` command essentially parses a block of plain text into mathematical expressions.
The parsing and evaluation functionalities are powered by [`exprtk`](https://github.com/ArashPartow/exprtk).

The `exprtk` generates an AST from the input text. The evaluation of the expression is for sure slower than built-in
expressions.

But a customisable expression allows for more flexibility and it is easier to experiment different functions.

## Syntax

```text
expression (1) (2) (3)
# (1) int, unique expression tag
# (2) string, variable list
# (3) string, expression string or name of file containing expression
```

## Remarks

1. The variables in the expression need to be explicitly given as the second argument. It can be either unquoted or
   quoted by `"`.
2. Multiple variables must be separated by vertical bar `|`.
3. The expression can be given as a string or as a file name. The program tries to load the file first. If the file
   does not exist, the program tries to parse the string as an expression.
4. No whitespace (',', ' ', etc.) is allowed in the variable list `(2)`, and
   in expression string `(3)`, if it is not the file name.

`exprtk` provides very powerful functionalities. It is possible to apply logics and control flows in the expression.

## Example

Say, for example, one is going to define a uniaxial nonlinear elastic model that uses the following stress-strain
relationship:

$$
\sigma=\varepsilon^3+\varepsilon
$$

Then the expression can be defined as

```text
expression 1 x x^3+x
```

Here, we use `x` as the free variable and the corresponding expression is `x^3+x`.

For the unixial nonlienar elastic model, the input is strain, which maps to `x`, the output maps to stress.

Alternatively, the expression can be stored in a file and loaded by the program.

```text
# file cubic.txt
x^3+x
```

Then the expression can be defined as

```text
expression 1 x cubic.txt
```

For complex expressions, it is convenient to use the file format.

To use the expression, here, [`CustomElastic1D`](../../Library/Material/Material1D/Elastic/CustomElastic1D.md) is used.

```text
# using expression 1
material CustomElastic1D 1 1

materialTest1D 1 1E-2 200

exit
```

The response can be tested by [material tester](../Process/materialtest.md).

## Result

![cubic response](expression.svg)
