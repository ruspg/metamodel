## Metamodel Change Request

**Type:** <!-- check one -->
- [ ] New entity kind
- [ ] New relation kind
- [ ] Attribute change (add / rename / remove)
- [ ] Qualifier change
- [ ] Glossary / alias update
- [ ] Tooling / CI change
- [ ] Deprecation

**Affected kinds / relations:**
<!-- List entity_kind IDs or relation IDs affected -->

**Breaking change:** <!-- Yes / No -->

**Justification:**
<!-- Why is this change needed? Link to ADR or requirement if applicable -->

---

### Validation results

<!-- Paste output of: python -m tools.wave1.harness model/metamodel.yaml --relation-catalog-path model/relation_catalog.yaml -->

```
<paste here>
```

### Checklist

- [ ] Ran validation harness locally (zero errors)
- [ ] Ran lint check (`python -m tools.wave1.lint ...`)
- [ ] No breaking changes **or** documented migration path
- [ ] Updated `name_ru` for all new/changed entities
- [ ] ADR created in `docs/decisions/` if this is an architectural decision
- [ ] Tests updated or added in `tests/`
