# Relation Catalog v2 — Rules

Дата: 2026-03-14  
Статус: stub / draft  
Depends on: `relation_kind_contract_v2.md`, `business_layer_relation_matrix.md`, `relation_catalog_v2_spec.yaml`  
Consumed by: bundle generator, relation catalog build, traversal rules

---

## 1. Purpose

Определить правила формирования relation catalog v2:
- allowed/forbidden combinations source_kind → relation_kind → target_kind;
- traversal semantics;
- qualified vs unqualified edges;
- cardinality and direction rules.

---

## 2. TODO

- [ ] Правила allowed relations по слоям (business, data, IT, org)
- [ ] Traversal bounds и recursion limits
- [ ] Qualified edge semantics
- [ ] Cardinality constraints
