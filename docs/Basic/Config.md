# Configuration

## Disable New Version Check

Some distributions are bundled with an updater that checks for new versions of the application on startup and allows you
to download new archives if necessary.
In some fully automated environments, one can disable the check via the `-nu` option.

```shell
suanpan -nu -f <your_input_model.sp>
```

### Disable Color Output

By default, the console output is colored to make it more readable.
If the console output is redirected to a file, the ANSI color codes will be included in the file.
To disable the color output, use the `-nc` option.

```shell
suanpan -nc -f <your_input_model.sp>
```

The ANSI color codes can be properly rendered using, for example, [bat](https://github.com/sharkdp/bat).

### Redirect Console Output

By default, the console output is printed to the standard output.
To redirect the output to a file, use the `-o` option.

```shell
suanpan -f <your_input_model.sp> -o <your_output_file>
```

### Verbose Output

With the release build, only info/warning/error/fatal messages will be printed.
To print debug messages, use the `-vb` option.

```shell
suanpan -vb -f <your_input_model.sp>
```

### Disable Output

If the model has been checked, output can be disabled to speed up the analysis.
To disable the output, use the `-np` option.

```shell
suanpan -np -f <your_input_model.sp>
```
