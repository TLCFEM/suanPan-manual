# import

The `import` command loads external libraries.
Place the library file (`.dll`, `.so` or `.dylib`) in the folder containing the executable and use the following command to import it.

```
import (1)
# (1) string, external library name
```

The file extension is optional.

If an external library exports only one function and its name matches the library name, the library does not need to be imported explicitly.
It is imported automatically.

For example, the external library `ElementExample.dll` contains the function that creates an external `ElementExample` object.
By default, the function is named `void new_elementexample()`.
To define an `ElementExample` element, simply use

```
element ElementExample !... element definition goes here
```

The program first looks in the built-in element library for `ElementExample`.
If it is not found, the program looks for a function with the signature `void new_elementexample()` in the currently loaded external libraries.
If it is still not found, the program tries to load `ElementExample.dll`.

If an external library exports more than one function, users must **explicitly** import the library to use the other functions.

In a C++ implementation, a smart pointer such as `unique_ptr<Element>` is passed from the DLL to the main executable.
Both the DLL and the executable must be compiled with the same configuration.
Otherwise, unexpected errors may occur.
If possible, use a C-type interface instead.
