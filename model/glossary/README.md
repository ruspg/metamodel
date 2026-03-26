# model/glossary

Глоссарий терминов метамодели живёт непосредственно в `model/metamodel.yaml` в секции `entity_kinds`.

Каждый `entity_kind` содержит глоссарные поля:
- `description` — формальное определение
- `scope_notes` — границы, ограничения, правила именования экземпляров
- `aliases[]` — управляемые синонимы `{value, lang, alias_type, status}`
- `examples[]` — конкретные примеры экземпляров
- `usage_purpose` — зачем сущность нужна
- `status` — `active` / `draft` / `deprecated`
- `introduced_in` — версия глоссария

Источник: **Глоссарий 1.0** (SSCAR-615105454)

Структура записей: см. [glossary_alias_naming_policy.md](../../docs/architecture/glossary_alias_naming_policy.md)
