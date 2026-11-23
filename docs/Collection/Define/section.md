# section

The `section` command defines a section that can be attached to beam elements.
Please refer to the specific section types for the available syntax.

## Syntax

```text title="section"
section (1) (2) ...
# (1) string, section type
# (2) int, unique section tag
```

For code-based sections, a designation string is required between the section type and the tag, for example, `section US2D W21X68 1 1`.
