# version

The `version` command prints version and build information about the running executable.
It reports the copyright notice, the binary version and compile date, the instruction set, and details of the linked linear algebra and optional libraries.

## Syntax

```text title="version"
version
```

## Remarks

The same information is available from the command line with the `-v` flag.
In parallel runs, only rank zero prints the information.
