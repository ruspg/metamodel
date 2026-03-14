# Metamodel bundle landing area

This directory is the canonical landing area for **versioned metamodel bundle artifacts** imported from upstream `metamodel` releases.

## What lives here

- `active_version.json` — explicit metadata for which imported bundle version is currently active for Atlas consumption.
- `versions/` — immutable, versioned bundle snapshots.

Each version directory is expected to contain exactly these upstream bundle artifacts:

- `metamodel_snapshot.json`
- `type_catalog.json`
- `relation_catalog.json`
- `search_aliases.json`
- `compatibility_report.md`

## Active version semantics

- "Active" means the pinned bundle version that downstream Atlas runtime and tests should consume.
- Runtime code should consume pinned artifacts from this landing area, not raw upstream authoring files.
- Switching active versions is a metadata update in `active_version.json`; no dynamic switching logic is defined in this task.

## Population model

This area is populated by importing released/candidate upstream metamodel bundles into `versions/<bundle-version>/` and then setting `active_version.json`.

The `example-v0.0.0` directory is a shape-only placeholder for follow-up tasks.
