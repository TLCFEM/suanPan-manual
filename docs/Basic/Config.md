# Configuration

All available options can be printed via the `--help` flag.

```text
Usage: suanPan [--help] [--version] [--no-color] [--no-print] [--no-update] [--verbose] [--input-file INPUT_FILE_PATH] [--output-file OUTPUT_FILE_PATH]

Optional arguments:
  -h, --help                                    show this help message and exit 
  -v, --version                                 show version information and exit 
  -nc, --no-color                               suppress colors in terminal output 
  -np, --no-print                               suppress (most) terminal output 
  -nu, --no-update                              skip new version check on startup 
  -vb, --verbose                                enable (very) verbose terminal output 
  -f, --input, --input-file INPUT_FILE_PATH     specify path to the file containing input analysis 
  -o, --output, --output-file OUTPUT_FILE_PATH  specify path to the file for terminal output redirection 
```

## Disable New Version Check

Some distributions are bundled with an updater that checks for new versions of the application on startup and allows you
to download new archives if necessary.
In some fully automated environments, one can disable the check via the `-nu` option.

```shell
suanpan -nu -f <your_input_model.sp>
```

## Disable Color Output

By default, the console output is coloured to make it more readable.
If the console output is redirected to a file, the ANSI color codes will be included in the file.
To disable coloured output, use the `-nc` option.

```shell
suanpan -nc -f <your_input_model.sp>
```

The ANSI color codes can be properly rendered using, for example, [bat](https://github.com/sharkdp/bat).

## Redirect Console Output

By default, the console output is printed to the standard output.
To redirect the output to a file, use the `-o` option.

```shell
suanpan -f <your_input_model.sp> -o <your_output_file>
```

## Verbose Output

With the release build, only info/warning/error/fatal messages will be printed.
To print debug messages, use the `-vb` option.

```shell
suanpan -vb -f <your_input_model.sp>
```

## Disable Output

If the model has been checked, output can be disabled to speed up the analysis.
To disable the output, use the `-np` option.

```shell
suanpan -np -f <your_input_model.sp>
```
