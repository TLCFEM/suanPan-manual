# modifier

The `modifier` objects are used to modify element response that does not considered in element itself. Typical examples
include element damping matrix, lumped mass matrix, etc.

It shall be noted that if several modifiers are defined, they are applied on the system in a sequential manner based on
their tags. No parallel execution can be implemented as different orders may lead to different results.

Users shall pay extra attention to the order of definition of modifiers.

Please refer to [`Modifier`](../../Library/Element/Modifier/Modifier.md) for available modifiers.
