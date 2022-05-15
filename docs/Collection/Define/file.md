# file

The `file` command is used to load external `suanPan` model files with or without extension `.supan` under the current
working path.

## Syntax

```
file (1)
# (1) string, external file name
```

Please note users can use [`pwd`](../Process/pwd.md) to change current working path.

## Usage

The main file:

```
# main file calling external file
file pre
step static 1
cload 1 0 23 2 2 ! this is an example
step static 2
cload 2 0 17 1 2
analyze
peek node 2
exit
```

The `pre.supan` file:

```
# pre.supan
node 1 0 0
node 2 1.34 0
material Elastic1D 1 132
element EB21 1 1 2 7.213 6.825 1
fix 1 P 1
```
