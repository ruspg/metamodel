# tools

Canonical location for repository tooling.

## Current state
Existing converter tooling is preserved in-place to avoid breaking current workflows:
- `metamodel2owl/` (OWL + Mermaid export CLI)
- `metamodel_to_mermaid/` (focused Mermaid rendering pipeline)

This `tools/` directory is the forward-looking home for future loader/validator/generator/release scripts and wrappers.

## Ontology loader
- `tools/wave1/loader.py` provides `load_ontology(...)` for deterministic structural loading/normalization.
- `tools/wave1/model.py` defines the normalized in-memory dataclasses consumed by follow-up validation/generation tasks.

## Ontology validator
- `tools/wave1/validator.py` provides `validate_ontology(...)` for structural/contract checks over the normalized model.
- `ensure_valid_ontology(...)` raises a readable fatal error while preserving structured result support for tests/review.

## Ontology lint
- `tools/wave1/lint.py` provides `lint_ontology(...)` for semantic quality checks (naming/alias/glossary/relation consistency) after structural validation.

## Relation catalog validator
- `tools/wave1/relation_catalog_validator.py` provides `validate_relation_catalog(...)` and `ensure_valid_relation_catalog(...)` for dedicated relation-catalog gates prior to generation tasks.

## Validation harness
- `tools/wave1/harness.py` provides `run_wave1_validation_harness(...)` to run load + ontology validation + lint + relation catalog validation in one deterministic flow.
- Local CLI usage: `python -m tools.wave1.harness model/metamodel.yaml --relation-catalog-path model/relation_catalog.yaml`

## Projection builder
- `tools/wave1/projection_builder.py` provides `build_projection_model(...)` for deterministic, profile-aware shaping of validated ontology data into a generator-ready projection model.
- `tools/wave1/projection_model.py` defines the projection dataclasses intended as shared inputs for downstream bundle generators.

## Atlas bundle generator
- `tools/wave1/atlas_bundle_generator.py` provides `generate_atlas_bundle(...)` as the canonical atlas bundle orchestration entrypoint over the projection model.
- `tools/wave1/atlas_bundle_model.py` defines bundle manifest/result dataclasses and deterministic artifact planning structures for future concrete artifact generators.
- `tools/wave1/metamodel_snapshot_generator.py` implements the concrete `metamodel_snapshot.json` artifact as a compact, deterministic runtime-facing metamodel surface for the active profile.
- `tools/wave1/type_catalog_generator.py` implements the concrete `type_catalog.json` artifact as a compact, deterministic runtime-facing kind/attribute catalog for the active profile.

- `tools/wave1/relation_catalog_generator.py` implements the concrete `relation_catalog.json` artifact as a compact, deterministic runtime-facing relation catalog for the active profile.
- `tools/wave1/search_aliases_generator.py` implements the concrete `search_aliases.json` artifact as a compact, deterministic runtime-facing alias/disambiguation projection for the active profile.
- `tools/wave1/compatibility_report_generator.py` implements the concrete `compatibility_report.md` artifact as a deterministic release/import compatibility summary over generated bundle artifacts.
- `tools/wave1/bundle_determinism.py` provides `verify_bundle_determinism(...)` to run repeated bundle generation and compare file paths, bytes, manifest ordering, and artifact ordering checks with concise drift diagnostics.
