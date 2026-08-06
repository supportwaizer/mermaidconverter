---
title: "Event-Driven Architecture"
status: "active"
date: "2026-08-05"
version: "1.0"
owners:
  - "{team-or-person}"
tags:
  - "architecture-style"
  - "integration"
  - "asynchronous-messaging"
related-patterns:
  - "Service-Based Architecture"
  - "Publish-Subscribe"
  - "Transactional Outbox"
  - "Saga"
---
 
# Event-Driven Architecture
 
## Problem
 
Components that communicate through synchronous request/response calls are coupled in time: a caller cannot complete its work unless the callee is available and responsive, so availability becomes the product of every component in the call path and latency accumulates along it.
 
They are also coupled in knowledge. When a business fact needs to reach a new consumer, the producing component must be modified, retested, and redeployed. The producer accumulates awareness of every consumer, and the cost of adding the *n*th consumer grows with *n*.
 
The recurring problem is: **how to let one component's business facts reach an arbitrary and changing set of consumers, without the producer knowing who they are and without its availability depending on theirs.**
 
## Context
 
Describe the environment in which this pattern applies.
 
- **Business context:** Processes that are naturally reactive — "when X happens, do Y and Z" — where the set of things to do on X grows over time, and where consumers can tolerate acting shortly after the fact rather than within the originating transaction.
- **Technical context:** Multiple components, distinct deployment units, and workloads with significant peak-to-average variation. Downstream views such as search indexes, caches, and reporting stores that must be refreshed faster than batch allows.
- **Regulatory/compliance context:** Environments benefiting from a durable, replayable record of business facts for audit — but also environments where eventual consistency must be explicitly assessed against obligations that assume immediate consistency.
- **Organisational context:** Teams able to own consumers independently, with the operational capability to run messaging infrastructure and to diagnose asynchronous failures.
- **Assumptions:** Business facts can be expressed as immutable statements about the past. Consumers can be made idempotent. The organisation can invest in tracing before, not after, adoption.
- **Constraints:** No distributed transactions across components. At-least-once delivery must be assumed. Ordering can be guaranteed only within a partition key.
## Forces
 
- **Decoupling pulls against comprehensibility.** The less producers know about consumers, the harder it is for anyone to determine what actually happens when an event occurs.
- **Availability pulls against consistency.** Removing temporal coupling means accepting that consumers act after the fact, not within it.
- **Extensibility pulls against traceability.** Adding a consumer without touching the producer is the benefit; it also means no artefact records that the consumer exists.
- **Peak load pulls against provisioning cost.** Synchronous designs must be sized for peak; asynchronous designs can absorb bursts and drain them.
- **Delivery guarantees are bounded by physics.** Exactly-once delivery cannot be assumed, so duplicate and out-of-order handling is unavoidable work in every consumer.
- **Autonomy pulls against schema stability.** Producers cannot know who depends on which field, so contract evolution requires governance that synchronous interfaces obtain implicitly.
## Solution
 
Components communicate by publishing **immutable events describing facts that have already occurred**, named in the past tense. An event is not a command and not a request; it carries no expectation of a response, and the producer neither knows nor cares who consumes it.
 
Events are published to named topics using **publish/subscribe**: any number of consumers subscribe independently, and adding a consumer requires no change to the producer. This is the primary property being purchased.
 
Simple reactive flows are **choreographed** — components react to events and publish their own. Processes requiring multi-step coordination, compensation, or an explicit state machine use a **mediator** that owns the process definition. Choreography is the default; a mediator must be justified by genuine workflow complexity.
 
Because delivery is at-least-once, **every consumer must be idempotent**, tolerating duplicate and out-of-order arrival. Because a state change and its event announcement cannot be committed atomically to two systems, the state change and the outgoing event are written in the same local transaction and published from there by a relay — the transactional outbox. Dual writes lose events.
 
## Structure
 
| Component | Responsibility |
|---|---|
| **Producer** | Executes a business operation and publishes the resulting fact. Knows the topic and the contract; knows nothing of consumers. |
| **Event** | Immutable record of something that happened, carrying an envelope: event identifier, type, schema version, timestamp, source, correlation identifier, causation identifier. |
| **Topic** | Named channel for one event type, to which any number of consumers subscribe. |
| **Broker** | Durably stores and delivers events, absorbing bursts and decoupling producer and consumer availability. |
| **Consumer** | Subscribes and acts. Idempotent, independently deployable and scalable, owns its own failure handling. |
| **Mediator** *(optional)* | Owns a multi-step process definition, issuing commands and handling compensation. Used only where coordination is genuinely required. |
| **Outbox and relay** | Guarantees that a state change and its event are committed atomically and published reliably. |
| **Dead-letter destination** | Receives events a consumer cannot process, with a named owner, an alert, and a redrive procedure. |
 
## Implementation
 
- **Choose the payload style per topic and state it in the contract.** *Notification* events carry an identifier only and require consumers to call back for detail. *Event-carried state transfer* carries the data consumers need, removing read-time coupling at the cost of larger payloads and duplicated state. Mixing styles within one topic causes consumers to be written against assumptions that do not hold.
- **Fix topic naming before the first event is published** — for example `domain.entity.event-past-tense.v1`. Renaming later is a breaking change for every consumer.
- **Permit only backward-compatible schema changes** within a major version: add optional fields, never remove, rename, or retype. Breaking changes publish a new major version in parallel and retire the old only after consumer migration is confirmed.
- **Implement idempotency explicitly**, recording processed event identifiers for a defined window, or documenting why the operation is naturally idempotent.
- **Key events by aggregate identifier** where ordering matters; never assume global ordering across topics.
- **Build observability before the first consumer.** Correlation identifiers propagated through every hop, distributed tracing, and dashboards for consumer lag and dead-letter depth. Consumer lag is the primary health signal.
- **Retain events long enough to replay** and rebuild a consumer from history — another reason idempotency is mandatory rather than advisory.
- **Maintain an event catalogue** listing each event type, its schema, its producer, and its known consumers. It will be imperfect; its absence guarantees nobody can answer what happens when a given fact occurs.
- **Convert one flow first** — one with clear fan-out and tolerant consistency requirements, such as notifications or analytics, never payments.
## Usage Guidelines
 
**When to use this pattern**
 
- Multiple consumers need the same business facts, and the set of consumers changes over time.
- Producer availability should not depend on consumer availability.
- Workload has significant bursts that can be absorbed and drained rather than provisioned for.
- Business processes are naturally reactive, and reacting shortly after the fact is acceptable.
- A durable record of what happened has independent value for audit, replay, or analytics.
**When not to use this pattern**
 
- The caller needs an answer before it can proceed — that is a query, and it should stay synchronous.
- The operation requires immediate consistency that the business genuinely cannot relax.
- There is exactly one consumer and no prospect of another; the coupling being removed does not exist.
- The team cannot invest in tracing, idempotency, and dead-letter handling up front. Adopting the pattern without them produces a system whose failures are undiagnosable.
- The domain is genuinely orchestration-shaped — long, explicit, heavily-conditional workflows — where a workflow engine expresses the intent more honestly than choreography.
## Consequences
 
### Benefits
 
- New consumers are added with no producer change, no producer redeployment, and no producer regression testing.
- Temporal decoupling: a consumer being down delays processing rather than failing the producer's operation.
- Bursts are absorbed by the broker, so components are sized for average rather than peak load.
- Consumers scale independently, and slow consumers do not slow producers.
- The event stream becomes a durable record of business facts, usable for audit, debugging, replay, and analytics.
- Failure is isolated: a failing consumer affects its own processing, not its siblings' or the producer's.
### Trade-offs
 
- Eventual consistency becomes a business-visible property requiring a designed product answer, not a technical detail.
- No end-to-end transaction: multi-component processes need compensating actions, which can themselves fail.
- Debugging is materially harder — there is no stack trace across an asynchronous boundary.
- The overall business process exists nowhere explicitly; behaviour is emergent across subscribers and documentation drifts from reality.
- Every consumer must handle duplicates, out-of-order arrival, and poison messages — real, recurring work that is easy to omit until it causes an incident.
- Schema evolution requires governance, because a producer cannot know who depends on a field.
- Error handling has no caller to return to; failures surface as dead-letter accumulation requiring monitoring and triage ownership.
- The broker becomes critical infrastructure with its own availability, capacity, and upgrade concerns.
## Variants
 
- **Broker topology (choreography)** — components react and publish; no central coordinator. Maximum decoupling, minimum visibility of the overall process.
- **Mediator topology (orchestration)** — a coordinator owns the process definition. Explicit and inspectable, at the cost of re-coupling the coordinator to every participant.
- **Notification events** — thin payloads, consumers call back for detail. Lowest coupling, highest read amplification.
- **Event-carried state transfer** — payloads carry the data consumers need. Eliminates callbacks at the cost of duplicated state.
- **Event sourcing** — events become the system of record, with current state derived by replay. A materially larger commitment than publishing events, and a separate decision; conflating the two is a common and expensive mistake.
- **CQRS with event-maintained read models** — read stores updated by events, decoupling read shape from write shape.
- **Request/reply over messaging** — asynchronous transport with a correlated response. Useful, but it reintroduces temporal coupling and should be recognised as such.
## Example
 
An order platform publishes `OrderPlaced` when an order is accepted.
 
Initially two consumers subscribe: stock reservation and customer notification. Later the business adds demand forecasting, then a fraud screening process, then a partner data feed. **None of these required any change to the order service**, which remains unaware that any of them exist.
 
The order service writes the order and the `OrderPlaced` event in one local transaction via its outbox, so the event cannot be lost if the process fails after commit. Each consumer processes independently: when the notification provider is unavailable for twenty minutes, notifications queue and drain afterwards while order placement continues unaffected.
 
The accepted cost is visible in the product. A customer who places an order and immediately opens their order history may briefly not see it, so the interface shows a pending state rather than pretending the write was synchronous — a design decision, not a defect.
 
## Known Uses
 
- {system or project 1}
- {system or project 2}
## Related Decisions / ADRs
 
- ADR-003: Adopt Event-Driven Architecture
- {link or reference 2}
## References
 
- Hohpe, G. & Woolf, B. — *Enterprise Integration Patterns*
- Richards, M. & Ford, N. — *Fundamentals of Software Architecture*, chapter on event-driven architecture
- Fowler, M. — *What do you mean by "Event-Driven"?* (notification, event-carried state transfer, event sourcing)
## Revision History
 
| Date | Version | Notes |
|------|---------|-------|
| 2026-08-05 | 1.0 | Initial version |
