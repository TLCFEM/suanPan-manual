# domain

The `domain` command can be used to create new problem domains or switch from one to another.

## Syntax

```
domain (1)
# (1) int, domain tag
```

## Example

The program adopts a domain concept so that it could hold multiple domains (problems) at the same time. The program
starts with a default domain labelled with tag 1. Following output can be seen if a debug version is executed.
Irrelevant information has been removed for simplicity.

```
+--------------------------------------------------+
|   __        __        suanPan is an open source  |
|  /  \      |  \          FEM framework (64-bit)  |
|  \__       |__/  __   __          Acrux (0.1.0)  |
|     \ |  | |    /  | |  |                        |
|  \__/ |__| |    |__X |  |     maintained by tlc  |
|                             all rights reserved  |
+--------------------------------------------------+

debug: Storage of Domain ctor() called.
debug: Domain 1 ctor() called.
suanPan ~<>
```

By using the `domain` command, readers can create/switch to other domains, if necessary.

```
suanPan ~<> domain 2
debug: Domain 2 ctor() called.
create_new_domain() successfully creates Domain 2.
suanPan ~<>
```

Of course, domains can be deleted by using `erase`, `remove` or `delete`.

```
suanPan ~<> domain 2
debug: Domain 2 ctor() called.
create_new_domain() successfully creates Domain 2.
suanPan ~<> domain 3
debug: Domain 3 ctor() called.
create_new_domain() successfully creates Domain 3.
suanPan ~<> domain 4
debug: Domain 4 ctor() called.
create_new_domain() successfully creates Domain 4.
suanPan ~<> domain 5
debug: Domain 5 ctor() called.
create_new_domain() successfully creates Domain 5.
suanPan ~<> remove domain 2
debug: Domain 2 dtor() called.
suanPan ~<> erase domain 5
debug: Domain 5 dtor() called.
erase_domain() switches to Domain 1.
suanPan ~<> domain 4
create_new_domain() switches to Domain 4.
suanPan ~<> delete domain 3
debug: Domain 3 dtor() called.
suanPan ~<> remove domain 4
erase_domain() switches to Domain 1.
suanPan ~<>
```

Five domains are created. When `remove domain 2` is invoked, the current domain is `5`, so `2` is safely removed.
When `erase domain 5` is invoked, the current domain 5 is then deleted, by default, the program switches to the first
domain in the storage, it could be other domains, not necessary `1`. When `domain 4` is invoked, `4` already exists in
the storage so instead of creating a new one, the program switch to the existing one.

Within each domain, independent model can be defined, when `analyze` command is called, all domains will be analyzed.
