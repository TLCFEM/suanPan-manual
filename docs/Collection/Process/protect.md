# protect

In structural optimization, for example, elements are disabled when necessary.
For some analyses, certain elements must never be disabled.
Use `protect` to prevent those elements from being modified.

## Syntax

```text title="protect"
protect node (1...)
protect element (1...)
# (1...) int, node/element tags
```
