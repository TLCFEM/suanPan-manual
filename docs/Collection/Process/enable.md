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

For object types, possible values are: `amplitude`, `constraint`, `converger`, `criterion`, `domain`, `element`, `expression`, `group`, `integrator`, `load`, `material`, `modifier`, `node`, `orientation`, `recorder`, `section`, `solver` and `step`.

The `mute` command is an alias of `disable`.

The `erase` and `delete` commands are aliases of `remove`.

The special object type `all` is accepted by `enable` only and activates every object in the current domain.

## Enable/Disable Print Output

Output can also be enabled or disabled.
Printing to the screen buffer takes time.
Once the model is confirmed to be correct, output can be disabled to improve speed.
Third-party libraries are not controlled by this command and may still print.

```
enable print
disable print
```
