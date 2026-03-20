# Repository structure note

## Purpose
This note defines the canonical authoring/release structure and clarifies what remains legacy during phased migration.

## Canonical directories
- `model/schema/`
- `model/kinds/`
- `model/relations/`
- `model/glossary/`
- `profiles/`
- `tools/`
- `tests/`
- `generated/`

## Legacy-but-preserved areas
To keep the repository coherent and avoid breaking existing workflows, the following are preserved in place in this task:
- `data/` for current monolithic ontology YAML source files.
- `schema/` for current root metamodel schema.
- `metamodel2owl/` and `metamodel_to_mermaid/` for existing conversion/visualization tooling.

## Practical guidance for next tasks
- New loader/validator/generator/release-bundle work should target canonical areas.
- Legacy areas should be treated as compatibility inputs until dedicated migration tasks relocate or split artifacts.
- This task makes no ontology semantic changes.

## Upstream backlog alignment addendum (metamodel-only)

This addendum captures the minimum upstream work needed to keep downstream `rbank-atlas`
Command Center/runtime implementation safe **without** transferring UI/runtime ownership into
`metamodel`.

### Boundary enforcement
- `metamodel` owns ontology semantics, contracts, release bundles, and compatibility declarations.
- `rbank-atlas` owns runtime/API/UI/MCP behavior, instance graph quality, and operational concerns.
- Integration path is fixed: authoring model -> normalized ontology -> versioned atlas-ready bundle -> pinned import in `rbank-atlas` -> active runtime snapshot.

### Backlog items to track upstream

1. **Bundle and release discipline**
   - Ensure versioned atlas-ready bundle generation remains mandatory and deterministic.
   - Enforce release completeness checks for required artifacts in `bundle_manifest.json` and release notes.
   - Keep runtime consumers off raw authoring YAML by treating bundle artifacts as the only downstream import contract.

2. **Artifact closure for pre-implementation readiness**
   - Close and track: `required_preimplementation_artifacts`.
   - Finalize and govern: `ontology_schema_v2`.
   - Finalize and govern: `atlas_projection_bundle_spec`.
   - Finalize and govern: `runtime_normalized_metamodel_contract`.
   - Require compatibility handling/migration notes for any contract-affecting change.

3. **Contract-sensitive metadata completeness**
   - Complete/validate kind and relation metadata required by downstream traversal and labeling.
   - Enforce qualifier metadata discipline where qualifiers participate in runtime contract fields.
   - Ensure evidence-related metadata is present when required by projection/bundle contract.
   - Validate relation direction/inverse/traversal flags and profile applicability metadata.

4. **Change-management guardrails**
   - Block hidden semantic drift via schema and release quality gates.
   - Block untracked bundle shape drift through deterministic artifact checks.
   - Require explicit compatibility classification and migration notes for breaking changes.
   - Disallow upstream shortcuts that bypass the bundle contract.

### Explicitly out of scope for `metamodel`
- UI implementation (canvas, viewers, interaction modes, request UX).
- Runtime behavior implementation in API/MCP services.
- Operational observability/runbook execution concerns.

### Cross-repo dependency map

Downstream maintains a concise dependency map at:
`rbank-atlas/docs/runtime-contracts/cross_repo_dependency_map.md`

It answers: what upstream deliverables unblock downstream UI/runtime work, what can proceed immediately, hard vs parallel dependencies, and ownership boundaries. Upstream should not duplicate this; reference it when coordinating bundle releases and contract changes.
