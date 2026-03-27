# Business Layer Semantic Alignment

> Каноническое определение и разграничение ключевых бизнес-концепций онтологии.

---

## 1. Назначение

Этот документ фиксирует каноническое значение и границы ключевых бизнес-концепций, используемых в онтологии и runtime-графе. Его задача — исключить семантический дрейф при моделировании связей, маппинге BPMN и построении bundle.

The concepts covered here are:
- `value_stream`
- `value_stream_stage`
- `business_capability`
- `business_process`
- `business_operation`
- `business_function`
- `business_entity`
- `information_flow`

This document is normative for:
- ontology definitions in `metamodel`
- business-layer relation matrix
- BPMN mapping decisions
- registry/card/search wording
- source-to-type mapping and ingestability review

---

## 2. Core modeling principle

The business layer must separate:
- **why value is created**
- **what the organization is able to do**
- **how work is organized end-to-end**
- **what executable steps happen inside that work**
- **what stable functional responsibilities exist**
- **what business objects are manipulated**
- **what information moves between actors/systems/steps**

The canonical chain is:

`value_stream -> value_stream_stage -> business_process -> business_operation`

Cross-cutting and linked concepts:
- `business_capability` = what the organization is able to do
- `business_function` = stable functional responsibility / responsibility area
- `business_entity` = business object manipulated by work
- `information_flow` = information movement between actors, processes, operations, systems, or domains

---

## 3. Canonical definitions

### 3.1 `value_stream`

**Definition**  
An end-to-end value creation chain from trigger to outcome, expressed from the viewpoint of stakeholder/customer/business value delivered.

**Answers the question**  
“How is value created end-to-end?”

**Characteristics**
- cross-functional
- outcome-oriented
- spans multiple processes, teams, and systems
- relatively stable at an architectural level
- not a workflow diagram and not a functional org chart

**Good examples**
- Retail customer onboarding
- Consumer loan issuance
- Merchant payment acceptance lifecycle

**Not this**
- a single department’s activity list
- a BPMN diagram
- a system landscape
- a capability map item

---

### 3.2 `value_stream_stage`

**Definition**  
A major phase of a value stream representing a meaningful segment in the end-to-end value journey.

**Answers the question**  
“What major phase of value delivery are we in?”

**Characteristics**
- belongs to exactly one `value_stream`
- coarse-grained
- groups processes and, in future, metrics/KPIs
- useful for decomposition and navigation, not for execution logic

**Good examples**
- Lead capture
- Verification
- Fulfillment
- Servicing

**Not this**
- a low-level activity
- a function
- a team
- a system state machine step

---

### 3.3 `business_capability`

**Definition**  
A stable statement of business ability: what the organization is able to do, independent of a specific implementation, workflow, or system.

**Answers the question**  
“What must the organization be able to do?”

**Characteristics**
- relatively implementation-agnostic
- stable over time
- does not prescribe sequence
- not tied to a single team or system
- useful for target architecture and heatmapping

**Good examples**
- Identity verification
- Payment orchestration
- Credit decisioning
- Case management

**Not this**
- a single executable step
- a concrete workflow
- a screen or microservice
- a value stream stage

---

### 3.4 `business_process`

**Definition**  
A governed sequence of business work that transforms an input trigger into a business outcome according to rules, roles, and expected handoffs.

**Answers the question**  
“How is this business outcome operationally achieved?”

**Characteristics**
- sequence/flow-aware
- can have entry/exit conditions
- can have owner, SLA, criticality, and variants
- commonly represented in BPMN or similar notation
- usually spans multiple operations and may touch multiple functions/systems

**Good examples**
- Open current account
- Resolve disputed transaction
- Approve corporate credit line

**Not this**
- an entire value stream
- a capability statement
- a single atomic action
- a static org responsibility

---

### 3.5 `business_operation`

**Definition**  
A concrete executable business step performed within a business process, meaningful enough to be mapped to actors, systems, data changes, controls, and BPMN activities/tasks.

**Answers the question**  
“What business step is actually executed here?”

**Characteristics**
- finer-grained than `business_process`
- execution-facing
- can be linked to systems, components, data, controls, and BPMN activities
- may be repeated across processes
- is the preferred semantic target for process-step / activity mapping

**Good examples**
- Capture onboarding application
- Validate identity documents
- Enrich customer risk profile
- Create account in core banking
- Notify customer of approval

**Not this**
- a whole process
- an abstract capability
- a permanent function owned by a department
- a UI click or technical API call without business meaning

---

### 3.6 `business_function`

**Definition**  
A stable area of business responsibility or functional work domain that groups related business responsibilities independent of a specific process instance or sequence.

**Answers the question**  
“What area of functional business responsibility does this belong to?”

**Characteristics**
- more stable than process decomposition
- often aligns with enduring operating model responsibilities
- does not imply an ordered flow
- useful for mapping processes/operations to responsibility domains

**Good examples**
- Customer due diligence
- Account servicing
- Treasury operations
- Claims handling

**Not this**
- a process instance
- a BPMN task
- a capability statement without responsibility semantics
- a team/org unit itself

---

### 3.7 `business_entity`

**Definition**  
A core business object/concept that business work creates, updates, evaluates, moves, or references.

**Answers the question**  
“What business object is the work about?”

**Characteristics**
- domain object, not necessarily a physical database object
- stable semantic anchor across business, data, and IT layers
- can be lifecycle-bearing
- often mapped to data products/tables/topics in downstream layers

**Good examples**
- Customer
- Application
- Account
- Payment order
- Merchant agreement
- Credit case

**Not this**
- a row in a specific table
- a PDF attachment
- a process or capability
- a topic name as infrastructure artifact

---

### 3.8 `information_flow`

**Definition**  
A semantically meaningful movement or exchange of information between business actors, processes, operations, systems, or domains.

**Answers the question**  
“What information moves from where to where, and for what business purpose?”

**Characteristics**
- about information movement, not physical transport only
- can carry qualifiers such as channel, frequency, trigger, contract, direction, sensitivity
- bridges business and data architecture
- may later map to data contracts, events, interfaces, or documents

**Good examples**
- Customer profile passed from onboarding to risk screening
- Payment instruction sent from channel to payment processing
- Decision outcome returned to front office

**Not this**
- a system integration object only
- a Kafka topic by itself
- a team handoff without information semantics

---

## 4. Semantic boundaries and distinctions

### 4.1 `value_stream` vs `business_process`

- `value_stream` is end-to-end value creation across the organization.
- `business_process` is an operational flow that realizes part of that value.
- One value stream usually contains multiple processes.
- A process should not be used as a surrogate for the whole value journey.

### 4.2 `business_capability` vs `business_function`

- `business_capability` = ability the enterprise must have.
- `business_function` = stable responsibility domain where related work is grouped.
- A capability is about **ability**.
- A function is about **responsibility area / work domain**.
- They often relate, but are not interchangeable.

### 4.3 `business_process` vs `business_function`

- A process is sequence-oriented and execution-aware.
- A function is sequence-independent and more stable.
- A process can involve multiple functions.
- A function can support many processes.

### 4.4 `business_process` vs `business_operation`

- A process is a governed flow composed of steps.
- An operation is one meaningful executable step inside that flow.
- If something can be mapped to an activity/task with clear business meaning, it is often an operation.

### 4.5 `business_operation` vs BPMN activity

- BPMN activity is a modeling artifact element in a BPMN diagram.
- `business_operation` is a domain concept in the ontology.
- One BPMN activity may map 1:1 to one operation.
- In more complex cases, one operation may map to multiple BPMN activities or vice versa, but the ontology target remains `business_operation`, not raw BPMN syntax.

### 4.6 `business_entity` vs `data_table`

- `business_entity` is a business-domain concept.
- `data_table` is a physical/logical data asset in the data layer.
- Multiple tables may represent one business entity.
- One table may contain attributes of several business entities.

### 4.7 `information_flow` vs system integration

- `information_flow` captures business-semantic information movement.
- A system integration is a technical implementation route.
- One information flow may be implemented by multiple integrations/topics/APIs.

---

## 5. Recommended modeling chain

### 5.1 Canonical cross-layer chain

Recommended default modeling path:

`value_stream -> value_stream_stage -> business_process -> business_operation`

Then connect:
- `business_operation -> business_function`
- `business_operation -> business_entity`
- `business_operation -> information_flow`
- `business_operation -> it_system/component`
- `business_process -> business_function` where there is a coarse-grained stable relationship
- `business_capability` cross-cuts process/function/value stream as a statement of ability

### 5.2 Capability placement

Capabilities should usually sit as an **orthogonal lens**, not as the main execution chain.

Recommended interpretation:
- value stream = end-to-end value lens
- capability = ability lens
- process = operational flow lens
- function = stable responsibility lens
- operation = execution step lens

---

## 6. Overlap zones and how to resolve them

### 6.1 Capability vs function

**Problem**: both are often named similarly.  
**Resolution**: if the phrase sounds like “the enterprise must be able to …”, model as capability; if it sounds like “the area of business work/responsibility that handles …”, model as function.

### 6.2 Function vs operation

**Problem**: teams often call steps “functions”.  
**Resolution**: if it is a step in a sequence and can be mapped to BPMN activity/context, it is an operation; if it is a stable responsibility area, it is a function.

### 6.3 Process vs value stream

**Problem**: end-to-end processes are often mislabeled as value streams.  
**Resolution**: if the object is modeled as stakeholder value journey crossing organizational boundaries, it is a value stream; if it is governed operational work with flow logic and ownership, it is a process.

### 6.4 Business entity vs information flow

**Problem**: people model “application package” both as object and movement.  
**Resolution**: the object itself is `business_entity`; its transfer/handoff/exchange is `information_flow`.

---

## 7. Anti-patterns

### Anti-pattern 1 — using `business_function` as a bucket for process steps

Wrong:
- “Validate client documents” modeled as a function

Right:
- operation: “Validate client documents”
- function: “Customer due diligence”

### Anti-pattern 2 — mapping BPMN activity directly to `business_function`

Wrong because:
- activity is execution-level
- function is stable responsibility-level

Right:
- activity -> `business_operation`
- operation -> `business_function`

### Anti-pattern 3 — modeling every team handoff as `information_flow`

Wrong because:
- some handoffs are responsibility/workflow transitions, not information exchanges

Right:
- use `information_flow` only where information content and movement matter

### Anti-pattern 4 — using `business_entity` for technical artifacts

Wrong:
- Kafka topic, database schema, PDF file modeled as business entity by default

Right:
- keep technical artifacts in data/IT layers unless the object itself is a genuine business-domain concept

### Anti-pattern 5 — collapsing `value_stream`, `process`, and `capability` into one registry

Wrong because:
- these concepts answer different questions and support different UX journeys

Right:
- keep them separate and explicitly linked

---

## 8. Canonical examples

### Example A — retail onboarding

- `value_stream`: Retail customer onboarding
- `value_stream_stage`: Verification
- `business_capability`: Identity verification
- `business_process`: Open current account
- `business_operation`: Validate identity documents
- `business_function`: Customer due diligence
- `business_entity`: Customer application
- `information_flow`: Identity verification result sent to onboarding decision step

### Example B — payment processing

- `value_stream`: Merchant payment acceptance lifecycle
- `value_stream_stage`: Authorization
- `business_capability`: Payment authorization
- `business_process`: Process card payment
- `business_operation`: Route authorization request
- `business_function`: Payment operations
- `business_entity`: Payment order
- `information_flow`: Authorization response returned to acquiring channel

### Example C — loan issuance

- `value_stream`: Consumer loan issuance
- `value_stream_stage`: Decisioning
- `business_capability`: Credit decisioning
- `business_process`: Approve consumer loan
- `business_operation`: Enrich borrower risk profile
- `business_function`: Risk assessment
- `business_entity`: Credit application
- `information_flow`: Decision outcome transferred to front-office servicing

---

## 9. Decision rules for modeling

When deciding what something is, ask in order:

1. Is this an end-to-end value journey?  
   -> `value_stream`
2. Is this a major phase inside that journey?  
   -> `value_stream_stage`
3. Is this an enterprise ability statement?  
   -> `business_capability`
4. Is this a governed flow of work toward an outcome?  
   -> `business_process`
5. Is this an executable business step inside that flow?  
   -> `business_operation`
6. Is this a stable responsibility/work domain?  
   -> `business_function`
7. Is this a business-domain object manipulated by work?  
   -> `business_entity`
8. Is this semantically meaningful information movement?  
   -> `information_flow`

If an object seems to match several categories, prefer:
- keep the execution chain explicit
- keep stable responsibility separate from execution
- keep business object separate from data asset
- keep semantic information movement separate from technical implementation

---

## 10. Normative consequences for the ontology

### 10.1 Must remain separate kinds

The following must remain distinct first-class concepts in the ontology:
- `value_stream`
- `value_stream_stage`
- `business_capability`
- `business_process`
- `business_operation`
- `business_function`
- `business_entity`
- `information_flow`

### 10.2 BPMN implication

BPMN activity/task mapping must target `business_operation` as the primary business semantic anchor.

### 10.3 Runtime/UI implication

- Registries and cards must not blur process/function/capability terminology.
- Search aliases may help users find the right object, but aliases must not collapse ontology identities.
- Path/impact use cases should prefer paths passing through semantically explicit operations where available.

### 10.4 Ingestability implication

If a proposed kind cannot be populated distinctly from sources and produces no demo/query value, it may be demoted in MVP priority. But semantic distinctness is defined here first; ingestability review comes later.

---

## 11. Summary decisions

1. `business_operation` is treated as a first-class business-layer concept.
2. BPMN activity/task should map primarily to `business_operation`, not `business_function`.
3. `business_function` remains a stable responsibility/work-domain concept.
4. `business_capability` remains an orthogonal ability lens, not the execution chain.
5. `value_stream` and `business_process` stay separate because they answer different architectural questions.
6. `business_entity` is semantic business object, not technical storage artifact.
7. `information_flow` is semantic information movement, not merely technical integration plumbing.

---

## 12. Связанные контракты

- [Business Layer Relation Matrix](business_layer_relation_matrix.md)
- [Entity Kind Contract](entity_kind_contract_v2.md)
- [Решение: business_operation](../decisions/formal_decision_business_operation.md)

