# enable/disable/remove

## Enable/Disable/Remove Objects

In `suanPan`, defining some objects does not necessarily mean those will be considered in analysis. Instead, each object
has an 'active' flag, only active objects will be considered. Thus, it is possible to define a set of candidate
objects (for example, a number of loads), and test different cases with different objects.

Furthermore, it is possible to remove some wrongly defined objects before performing the analysis.

```
enable (1) [2...]
disable (1) [2...]
remove (1) [2...]
# (1) string, object type
# [2...] int, tags
```

For object types, possible values are: `domain`, `step`, `converger`, `constraint`, `load`, `element`, `node`
, `recorder`, `modifier`, `expression`.

## Enable/Disable Print Output

Additionally, it is possible to enable or disable output. Printing to screen buffer takes time. Once the model is
confirmed to be correctly established, users can disable print to improve speed. Third-party libraries are not
controlled by this command thus may print.

```
enable print
disable print
```
