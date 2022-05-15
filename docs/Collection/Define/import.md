# import

The `import` command is used to load external libraries. Drop the library file `.dll` (or `.so` or `.dylib`) to the same
folder contains the executable, one can use following command to import it.

```
import (1)
# (1) string, external library name
```

There is no need to include file extension.

If the external library has only one function exported and the name of which coincides with the external library name,
there is no need to explicitly import the library. It will be done automatically.

Say for example, the external library `ElementExample.dll` contains the corresponding function to create an
external `ElementExample` object. According to the default naming convention, the function will be named
as `void new_elementexample()`. To define a `ElementExample` element, one can simply use

```
element ElementExample !... element definition goes here
```

The program will look up build-in element library to see if `ElementExample` exists. If not, it tries to find a function
with signature `void new_elementexample()` in the currently loaded external libraries. If still not found, the program
tries to load `ElementExample.dll`.

If the external library contains more than one function, to use other functions, users need to **explicitly** import the
library.

For CPP implementation, a smart pointer, for example `unique_ptr<Element>`, is passed from DLL to main executable. It is
crucial to ensure both `.dll` and `.exe` are compiled with the same configuration. Otherwise, unexpected errors may
occur. If possible, always try a C type interface implementation.
