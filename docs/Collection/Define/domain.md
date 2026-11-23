# domain

The `domain` command creates a new problem domain or switches to an existing one.

## Syntax

```text title="domain"
domain (1)
# (1) int, domain tag
```

## Example

The program uses a domain concept so that it can hold multiple domains (problems) at the same time.
It starts with a default domain labelled with tag 1.
The following output is seen when a debug build is executed.
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

Use the `domain` command to create or switch to other domains.

```
suanPan ~<> domain 2
debug: Domain 2 ctor() called.
create_new_domain() successfully creates Domain 2.
suanPan ~<>
```

Domains can be deleted with `erase`, `remove` or `delete`.

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

Five domains are created.
When `remove domain 2` is invoked, the current domain is `5`, so `2` is safely removed.
When `erase domain 5` is invoked, the current domain 5 is deleted.
By default, the program then switches to the first domain in storage, which is not necessarily `1`.
When `domain 4` is invoked, `4` already exists in storage, so the program switches to the existing domain instead of creating a new one.

Within each domain, an independent model can be defined.
When the `analyze` command is called, all domains are analyzed.
