# terminal

The `terminal` command can be used to execute external commands.

```
terminal (1)
# (1) string, external command to be executed
```

The `terminal` command can only be used to external non-interactive commands. It invokes `std::system` function to
execute commands in the host environment's command processor.

Commands such as `chdir` will not work as the spawned process will quit when the command is executed.
