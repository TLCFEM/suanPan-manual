# file

The `file` command loads external `suanPan` model files, with or without the `.supan` extension, from the current working directory.

## Syntax

```text title="file"
file (1)
# (1) string, external file name
```

Use [`pwd`](../Process/pwd.md) to change the current working directory.

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
fix 1 E 1
```
