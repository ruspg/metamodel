# Research Brief: Enterprise Knowledge Graph & Ontology-Driven Architecture

> Задание на рисерч рыночных практик. Фокус: кто строит графы знаний в enterprise, как формальные метамодели меняют архитектуру, какие роли и команды для этого нужны, и почему это критично для AI-first организаций.

---

## 1. Scope

### 1A. Enterprise Ontology & Knowledge Graph в финансовом секторе

**Вопросы:**
- Какие банки / финтехи / страховые строят внутренние графы знаний? Масштаб, технологии, результаты.
- Как устроен граф: какие слои (бизнес, IT, данные, оргструктура)? Какие связи между ними считаются must-have?
- Какой путь от «CMDB + wiki» до «queryable knowledge graph»? Типичные этапы, сроки, ловушки.
- Palantir Foundry Ontology, Goldman Sachs Legend/PURE, JPMorgan internal KG, ING enterprise ontology — что известно публично? Whitepapers, конференции, патенты.
- Не-банки с сильными кейсами: Siemens (industrial KG), Airbus (engineering ontology), NHS (healthcare), Walmart (supply chain graph).

**Артефакты для поиска:**
- Публикации на KGC (Knowledge Graph Conference), ISWC, ESWC, VOILA workshops
- Gartner / Forrester отчёты по enterprise knowledge graphs 2024-2026
- Open-source онтологии для financial services (FIBO, FpML, CDM от ISDA)

### 1B. Metamodel-Driven Architecture

**Вопросы:**
- Кто использует формальные метамодели (не просто Archimate diagrams в EA tool, а machine-readable ontology как source of truth)?
- Как метамодель интегрируется в CI/CD: валидация, генерация артефактов, bundle-подход?
- Связка metamodel → code generation: кто генерирует API contracts, UI schemas, compliance reports из метамодели?
- Стандарты: ArchiMate, TOGAF, OMG MOF, Schema.org — кто реально использует как runtime schema, а не как reference?
- Компании с публичными metamodel repos / ontology repos на GitHub.

**Артефакты для поиска:**
- Доклады на EA Conference, Open Group events, The Architecture Gathering
- Практики ING, ABN AMRO, Deutsche Bank, BNP Paribas по metamodel-driven approach
- Emerging: LLM-powered ontology construction, ontology-as-code движение

### 1C. Роли и команды

**Вопросы:**
- Какие роли существуют вокруг enterprise knowledge graph?
  - Knowledge Architect / Ontology Engineer / Taxonomy Manager / Knowledge Graph Engineer / Semantic Data Engineer
  - Где они сидят в оргструктуре: в архитектуре? в data management? в AI/ML? отдельной командой?
- Как устроены команды:
  - Centralized ontology team vs federated domain ontologists?
  - Сколько людей типично? Какие навыки (OWL, SPARQL, graph DB, NLP, domain expertise)?
- Job postings: какие компании нанимают ontology engineers / knowledge architects прямо сейчас?
- Карьерные треки: откуда приходят (data engineering? architecture? NLP?) и куда растут.

**Артефакты для поиска:**
- LinkedIn job postings: «ontology engineer», «knowledge architect», «knowledge graph engineer» в financial services
- Salary benchmarks (Glassdoor, Levels.fyi)
- Team structure case studies от Palantir, Meta, Google, Amazon (public talks / blog posts)

### 1D. Значение для AI-First организаций

**Вопросы:**
- Почему knowledge graph критичен для enterprise AI (не просто RAG, а structured context)?
  - Graph RAG vs Vector RAG — сравнение подходов, когда что работает
  - Ontology как grounding layer для LLM (снижение галлюцинаций, structured tool use)
  - MCP (Model Context Protocol) и knowledge graph как backend для AI-агентов
- Кто из AI-first компаний инвестирует в knowledge infrastructure?
  - Palantir AIP + Foundry Ontology
  - Microsoft Copilot + Microsoft Graph
  - Google Gemini + Knowledge Graph
  - Amazon (product graph, supply chain ontology)
- Тезис: «Без knowledge graph AI-агенты работают вслепую — с ним они понимают контекст организации»
  - Есть ли данные / кейсы, подтверждающие это количественно?
  - ROI от knowledge graph для AI use-cases (time-to-answer, accuracy, hallucination rate)

**Артефакты для поиска:**
- Публикации Anthropic, OpenAI, Google DeepMind про structured knowledge + LLM
- AI Engineering conferences: доклады про ontology-grounded agents
- Enterprise AI platforms с built-in ontology layer (Palantir, Dataiku, Databricks Unity Catalog)

---

## 2. Формат результата

Для каждого направления:

| Блок | Содержание |
|------|-----------|
| **Обзор** | 1-2 абзаца: что происходит на рынке, ключевой тренд |
| **Лидеры** | Таблица: компания, что сделали, масштаб, публичные источники |
| **Практики** | 3-5 конкретных паттернов с примерами |
| **Роли** | Какие роли нужны, где их берут, типичная команда |
| **Для нас** | Что из этого применимо к нашему контексту (банк, метамодель, Atlas) |
| **Источники** | Ссылки на первоисточники (не блоги-пересказы) |

---

## 3. Приоритеты

| # | Тема | Приоритет | Почему |
|---|------|-----------|--------|
| 1 | AI-first + Knowledge Graph | 🔴 | Главный бизнес-аргумент: без графа AI слепой |
| 2 | Роли и команды | 🔴 | Нужно обосновать найм/формирование команды |
| 3 | Enterprise KG в банках | 🟡 | Индустриальные референсы для стейкхолдеров |
| 4 | Metamodel-driven architecture | 🟡 | Подтверждение подхода (не только мы так делаем) |

---

## 4. Ограничения

- Только публичные источники (конференции, whitepapers, blog posts, job postings)
- Фокус на 2023-2026 (свежие практики, не исторические)
- Финансовый сектор в приоритете, но tech-гиганты и промышленность как референсы допустимы
- Без спекуляций — если данных нет, так и писать
