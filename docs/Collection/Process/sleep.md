# sleep

The `sleep` command pauses execution for a given duration in milliseconds.
The argument is an integer number of milliseconds.

## Syntax

```
sleep (1)
# (1) integer, duration in milliseconds
```

## Remarks

If no argument is given, the command pauses for the default 1000 milliseconds.
If the argument cannot be parsed as an integer, an error message is printed and no pause occurs.
