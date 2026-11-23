# terminal

The `terminal` command executes external commands.

```
terminal (1)
# (1) string, external command to be executed
```

The `terminal` command can only be used for external non-interactive commands.
It invokes the `std::system` function to execute commands in the host environment's command processor.

Commands such as `chdir` do not work because the spawned process exits when the command is executed.
