# enable/disable/remove

## Enable/Disable/Remove Objects

In `suanPan`, defining an object does not necessarily mean it will be considered in the analysis.
Each object has an 'active' flag, and only active objects are considered.
Thus, it is possible to define a set of candidate objects (for example, a number of loads) and test different cases with different objects.

Furthermore, wrongly defined objects can be removed before performing the analysis.

```
enable (1) [2...]
disable (1) [2...]
remove (1) [2...]
# (1) string, object type
# [2...] int, tags
```

For object types, possible values are: `domain`, `step`, `converger`, `constraint`, `load`, `element`, `node`, `recorder`, `modifier` and `expression`.

## Enable/Disable Print Output

Output can also be enabled or disabled.
Printing to the screen buffer takes time.
Once the model is confirmed to be correct, output can be disabled to improve speed.
Third-party libraries are not controlled by this command and may still print.

```
enable print
disable print
```
