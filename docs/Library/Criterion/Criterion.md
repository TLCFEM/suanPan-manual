# Criterion

What is a `Criterion`? The `Criterion`, as the name implies, is some sort of criterion that may or may not be satisfied
by some quantities of the model.

The main motivation to have a `Criterion` is to terminate the [`ArcLength`](../Step/ArcLength.md) analysis. In a
typical `ArcLength` analysis, neither the displacement nor the resistance is known in advance. There should be a way to
determine when to stop the analysis.

A `Criterion` provides such a functionality. If the `Criterion` is satisfied, an `exit` flag will be sent out so that
the analysis will stop.

Due to its designed functionality, a `Criterion` can also be used to early-stop the analysis.
