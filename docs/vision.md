# Vision: Why the Bank Needs an Operating Metamodel

> The companies that build a machine-readable map of themselves will operate at a fundamentally different speed than those that don't.

---

## The Problem

A modern bank is a system of thousands of moving parts: products, processes, regulations, IT systems, data pipelines, organizational units — all deeply interconnected. Today, the knowledge about how these parts fit together lives in three places:

1. **People's heads** — the architect who knows which systems support the mortgage pipeline, the analyst who remembers why that reporting field changed last quarter
2. **Scattered documentation** — Confluence pages, spreadsheets, slide decks, Figma diagrams — each telling a partial story in a different format
3. **Siloed systems** — CMDB knows about servers, the process tool knows about workflows, the data catalog knows about tables, but none of them talk to each other

This creates real, measurable problems:

- **Impact analysis takes days, not minutes.** When a system goes down at 2am, who knows what customer journeys are affected? When a regulation changes, which processes, systems, and data products need to adapt? The answer exists — but assembling it requires calling five people and checking three systems.

- **Key-person risk is high.** Critical institutional knowledge walks out the door every time someone changes roles or leaves. Onboarding a new architect takes months because the real architecture isn't written down — it's distributed across conversations and tribal knowledge.

- **Regulatory questions are hard to answer quickly.** Auditors ask "show me every process that handles PII" or "which systems participate in this value chain." These are reasonable questions. The struggle to answer them reveals a structural gap.

- **AI initiatives hit a wall.** Every AI project starts by building its own local data model because there's no shared ontology. LLMs hallucinate about bank processes because there's no authoritative, machine-readable source of truth to ground them.

- **New products are slower than they should be.** Launching a new product means rediscovering which capabilities already exist, which systems can be reused, which data is available — instead of assembling from known building blocks.

---

## The Solution

The Operating Metamodel is a **formal, machine-readable map** of the bank: products, processes, capabilities, systems, data, infrastructure — and all the connections between them.

It is not documentation. It is a **living, validated, queryable graph**.

```
Operating Metamodel       Language & grammar: what types of entities and relationships exist
        │
        ▼
    Ontology              Semantic vocabulary: concrete domain concepts (Customer, Product, Risk)
        │
        ▼
Business Architecture     Business models: processes, capabilities, org structure, KPIs
        │
        ▼
   Knowledge Graph         Populated instance: models + actual data + time + scenarios
```

The metamodel defines the rules. The ontology fills in the vocabulary. The business architecture applies it to the real organization. The knowledge graph makes it queryable and alive.

**Six levels** cover the full stack:

| Level | What it answers | Examples |
|-------|----------------|----------|
| **Strategic View** | Why does this exist? | Goals, value streams, capabilities, products |
| **Business Details** | How does the business work? | Processes, operations, functions, business entities |
| **Data Details** | What data exists and how is it structured? | Data products, contracts, objects, lineage |
| **Solution Details** | What IT solutions support the business? | IT systems, integrations, APIs |
| **Component Details** | What are solutions made of inside? | Components, vendor products, software |
| **Infrastructure** | What does everything run on? | Platforms, resources, environments |

The key insight: **value comes from connections, not just definitions.** Knowing that "Loan Origination" is a process is useful. Knowing that it depends on systems X, Y, Z, produces data products A, B, C, is owned by team T, and is critical for regulatory report R — that's transformative.

---

## Capabilities Unlocked

### Composable Enterprise

When the bank needs a new product, the metamodel shows which capabilities already exist. Instead of building from scratch, teams assemble new value streams from proven building blocks — just as microservices compose into applications.

This is the model Gartner calls "Composable Enterprise" and what leading banks are already implementing: capabilities as reusable, governed, well-understood units that can be recombined for speed.

### Business Activity Monitoring

Map IT components to the business operations and processes they serve. When a system degrades, immediately understand which customer journeys and value streams are affected. Move from "system X is down" to "the mortgage application flow is impaired for the Premium segment."

### AI Agents with Real Context

LLMs and AI agents are only as good as the context they receive. The metamodel provides a structured, authoritative knowledge base that agents can query:

- **Semantic search**: ask "payments" and get the exact business entities, tables, and systems involved
- **Text2SQL**: column-level metadata annotations (types, ranges, examples) enable accurate query generation
- **BPMN generation**: auto-generate process diagrams from structured descriptions
- **"What-if" analysis**: trace the impact of changing a rate, retiring a system, or launching a product

The metamodel becomes the agent's mental model of the bank.

### Impact Analysis in Seconds

Trace any change through the graph: "If we decommission system X, which processes, data products, and value streams are affected?" Today this takes days of investigation. With a connected graph, it's a query.

### Regulatory Readiness by Design

Regulators increasingly ask questions that require connected, cross-cutting views of the organization. When audit readiness is built into the architecture — not bolted on before each audit — compliance shifts from a cost to a capability.

Data certification levels tied to regulatory requirements (reporting, analytics, operational) ensure that data quality is not aspirational but measurable and enforceable.

### Data Contracts and Lineage Enforcement

Formalize the obligations between data producers and consumers. Define what "quality" means with measurable SLI/SLO/SLA frameworks borrowed from service reliability engineering. Automatically propagate requirements through the data lineage: if the final report requires certain standards, every upstream source must meet them too.

---

## Industry Context

This is not a novel idea. The leading technology and financial companies have been building exactly this — and winning because of it.

**Palantir** built their entire business on the insight that connected data is exponentially more valuable than siloed data. Their Foundry Ontology is a semantic layer that maps business concepts onto raw data, enabling anyone in the organization to work with data through business language, not table names. The operating metamodel follows the same philosophy: a shared ontology that makes complexity navigable.

**Microsoft** is investing heavily in knowledge graphs across the enterprise stack: Microsoft Graph connects people, files, and activity; Fabric's semantic model layer is building toward unified enterprise knowledge. Their bet is clear: the future of enterprise software is graph-structured knowledge. The metamodel makes the same bet, purpose-built for banking.

**Goldman Sachs** operates Legend/PURE — a unified metadata and data modeling platform that powers trading, risk, and regulatory reporting from a single source of truth. Proof that formalizing your data model is not academic — it is a competitive weapon at the highest level of finance.

**JPMorgan Chase** maintains an internal knowledge graph connecting systems, data, processes, and organizational structure across 300,000+ employees and thousands of systems. It enables impact analysis, regulatory reporting, and architectural decision-making at scale.

**ING** demonstrated that a European bank can adopt ontology-driven architecture and achieve measurable improvements in time-to-market and operational transparency.

**Zalando, Netflix, Spotify** pioneered data mesh and metadata platforms (DataHub, Backstage), showing that treating metadata as a product — with ownership, contracts, and discoverability — transforms engineering culture. The metamodel brings this thinking to banking with the rigor that financial services demands.

The pattern is consistent: organizations that formalize their self-knowledge into a queryable, machine-readable graph operate at a different level of speed, transparency, and adaptability.

---

## From Metamodel to Knowledge Graph

The metamodel is the **schema** — the types and rules. But the real value emerges when it's populated with actual data from the bank's systems:

| Layer | What it is | What it enables |
|-------|-----------|----------------|
| **Metamodel** | Types and rules (YAML/OWL) | Validation, contracts, governance |
| **Ontology** | Domain vocabulary (concrete concepts) | Shared language across teams |
| **Knowledge Graph** | Populated graph from real systems | Queries, impact analysis, AI context |

The knowledge graph is built not by entering data from scratch, but by **connecting what already exists**: the component catalog knows about systems, the process tool knows about workflows, the data catalog knows about datasets. The metamodel provides the schema that makes these connections meaningful and traversable.

Storage evolves with scale: relational databases for early hundreds of objects, graph databases (like Neo4j) when the graph grows to tens of thousands of interconnected entities.

Access is programmatic: MCP (Model Context Protocol) interfaces allow AI agents to traverse the graph, ask questions about relationships, and use the metamodel as structured context for any task.

---

## The Journey

This is a journey, not a switch. The metamodel delivers value incrementally:

**Immediate** — A shared vocabulary. When business says "process" and IT says "process" and data says "process," they mean the same thing. This alone eliminates entire categories of miscommunication.

**Near-term** — Connected registries. Systems, processes, and data linked through governed relationships. Impact analysis becomes queryable. Onboarding accelerates because the architecture is navigable.

**Medium-term** — AI-augmented operations. Agents use the graph for context-aware assistance: answering architectural questions, generating documentation, suggesting impact of changes, automating compliance checks.

**Long-term** — The knowledge graph becomes the bank's operating system for institutional knowledge. Not replacing existing systems, but connecting them into a coherent, queryable, machine-readable whole. A digital twin of the organization's architecture — always current, always connected, always available.

The companies that figure this out first will not just operate more efficiently. They will operate at a fundamentally different speed — making decisions with full context, launching products from proven components, and answering any question about their own architecture in seconds instead of weeks.

The metamodel is the foundation that makes all of this possible.
