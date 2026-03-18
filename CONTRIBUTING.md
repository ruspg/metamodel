# Contributing to the Metamodel

This repository contains the **canonical ontology definitions** for the RBank Atlas platform.
Changes here affect all downstream systems (API, MCP, UI, ingestion).

## Quick Start

```bash
# Clone and enter
git clone <repo-url> && cd metamodel

# Validate the current model
python -m tools.wave1.harness \
  data/bank_metamodel_horizontal.yaml \
  --relation-catalog-path docs/architecture/relation_catalog_v2_spec.yaml

# Run semantic linter
python -m tools.wave1.lint data/bank_metamodel_horizontal.yaml

# Run tests
python -m pytest tests/ -v
```

## Making Changes

### 1. Create a branch

```bash
git checkout -b feat/add-<kind-name>
```

### 2. Edit the YAML

All entity kinds and relations are defined in `data/bank_metamodel_horizontal.yaml`.

Follow the contracts:
- Entity kinds: see `docs/architecture/entity_kind_contract_v2.md`
- Relations: see `docs/architecture/relation_kind_contract_v2.md`
- Attributes: see `docs/architecture/attribute_def_contract_v2.md`
- Qualifiers: see `docs/architecture/qualifier_def_contract_v2.md`

### 3. Validate locally

```bash
# Must pass with zero errors before creating PR
python -m tools.wave1.harness \
  data/bank_metamodel_horizontal.yaml \
  --relation-catalog-path docs/architecture/relation_catalog_v2_spec.yaml
```

### 4. Create a Pull Request

- Use the PR template (auto-populated)
- Paste validation results
- Tag the metamodel architect for review

### 5. After merge

The CI pipeline will:
1. Re-run validation + lint + tests
2. Verify bundle determinism

Bundle generation and import into rbank-atlas is a separate manual step
(see `generated/atlas_candidates/README.md`).

## Roles

| Role | Responsibility |
|---|---|
| **Metamodel Architect** | Approves all structural changes to kinds/relations |
| **Data Owner** | Confirms attribute definitions for their domain |
| **Platform Team** | Maintains tooling, CI, schema validation |

## Rules

- One change per PR (atomic changes only)
- All entity/relation IDs must use `snake_case`
- Relation IDs must start with a descriptive prefix
- `name_ru` is required for all entities and relations
- Breaking changes require an ADR in `docs/decisions/`
- Generated bundles in `generated/` are immutable — never edit them

## Need Help?

- Full contribution rules: `docs/metamodel_contribution_rules.md`
- Naming policy: `docs/architecture/glossary_alias_naming_policy.md`
- Decision log: `docs/decisions/`
