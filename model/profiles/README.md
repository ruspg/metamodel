# model/profiles

Profile projection filters for downstream bundle generation.

Each profile defines which entity kinds and relation kinds are included
in a given projection (e.g. `atlas_mvp`).

> **Current status:** Profile filtering logic lives inside
> `tools/wave1/projection_builder.py`. Extracting it into declarative
> YAML files here is a planned future step.
