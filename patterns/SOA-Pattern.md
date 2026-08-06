---
title: "Service-Based Architecture"
status: "active"
date: "2026-08-05"
version: "1.0"
owners:
  - "{team-or-person}"
tags:
  - "architecture-style"
  - "distributed-systems"
  - "domain-partitioning"
related-patterns:
  - "Modular Monolith"
  - "Microservices"
  - "Event-Driven Architecture"
---
 
# Service-Based Architecture
 
## Problem
 
A monolithic application reaches a size where a change to any module requires releasing and regression-testing the whole system. Release cadence is capped regardless of how small the change is, a defect anywhere can exhaust resources shared by everything, and multiple teams contend for a single deployment pipeline.
 
Microservices resolve these problems but demand that the data model be decomposed into a database per service, eliminating cross-domain joins and ACID transactions, and requiring operational maturity many organisations do not have.
 
The recurring problem is therefore: **how to obtain independent deployability and fault isolation at the domain level without paying the cost of distributed data management.**
 
## Context
 
Describe the environment in which this pattern applies.
 
- **Business context:** A system serving several identifiable business domains with materially different change rates, where release speed and blast radius are constraining delivery, but transactional integrity across the business processes remains a hard requirement.
- **Technical context:** An existing monolith or a greenfield system with a highly relational data model — significant cross-domain foreign keys and joins — and workflows requiring ACID guarantees across what would otherwise become service boundaries.
- **Regulatory/compliance context:** Environments where auditability depends on referential integrity, or where the reconciliation logic that eventual consistency demands would itself be a compliance burden.
- **Organisational context:** Multiple teams, each capable of owning a domain, but without a platform organisation providing per-service infrastructure, service mesh, distributed tracing, and per-service on-call.
- **Assumptions:** Domain boundaries are reasonably well understood. Scaling requirements are satisfied by scaling whole domains. A single database can carry the aggregate load.
- **Constraints:** No appetite for distributed transactions or saga-based compensation. Limited operational maturity for a large service estate. Cost sensitivity relative to a full microservices migration.
## Forces
 
- **Deployment independence pulls against data integrity.** Separating deployables invites separating data, which is what destroys transactional guarantees.
- **Team autonomy pulls against coordination cost.** More independently deployable units means less merge contention but more pipelines, dashboards, and contracts to maintain.
- **Granularity pulls in both directions.** Finer services scale and deploy better; coarser services stay self-contained and avoid inter-service chatter.
- **Change-rate variance.** Domains that change weekly and domains that change annually are penalised by being forced onto a shared release train.
- **Operational capability is finite.** Each additional service consumes a fixed quantum of operational attention that does not scale with team size.
- **Cost and time-to-value.** The strongest architecture is worthless if the migration exceeds the organisation's patience or budget.
## Solution
 
Partition the system into a **small number of coarse-grained, independently deployed domain services** — typically four to twelve, one per business domain. Each service contains the full technical stack for its domain: API, business logic, and persistence access. Services are portions of the application, not single-purpose functions.
 
All services **share a single database**, preserving cross-domain queries and ACID transactions. The database is partitioned into logical schemas per domain, with views exposing one domain's data to another where required, so services are decoupled from each other's table structures.
 
An optional **API layer** in front of the services handles routing, authentication, rate limiting, and observability. It contains no business logic and performs no orchestration — it is not a mediator or an enterprise service bus.
 
Services are designed to be **self-contained**: a service should satisfy a request without calling siblings. Where inter-service calls are unavoidable they are documented in the service contract, and call chains deeper than one hop are prohibited.
 
## Structure
 
| Component | Responsibility |
|---|---|
| **User interface** | Presents the application. Either a single front end or partitioned by domain, calling services through the API layer. |
| **API layer** *(optional)* | Routing, authentication, rate limiting, observability. Stateless, logic-free. |
| **Domain service** | Full stack for one business domain — interface, business rules, data access. Independently deployable, independently testable, owned by one team. |
| **Logical schema** | The domain's tables within the shared database. Written to only by its owning service. |
| **Cross-domain view** | Read-only projection exposing one domain's data to another, decoupling consumers from table structure. |
| **Shared database** | Single physical database providing referential integrity and ACID transactions across the whole system. |
 
Interaction: the UI calls the API layer, which routes to a domain service. The service executes its business logic and reads or writes its own schema, reading other domains through views. Inter-service calls are the exception rather than the mechanism.
 
## Implementation
 
- **Identify domains before services.** Derive boundaries from business capability and change rate, not from the existing module structure or the org chart.
- **Partition the database into schemas first**, while still a monolith. This surfaces cross-domain coupling early and cheaply, and establishes the boundary along which physical separation could later occur.
- **Expose cross-domain reads through views** owned by the producing domain, so that consumers never bind to another domain's tables.
- **Extract the highest-change, lowest-coupling domain first** to validate the pipeline and the boundary approach at minimum risk.
- **Give each service its own build, test, and deployment pipeline** — without this the pattern delivers nothing, since independent deployability is the entire point.
- **Version service contracts** and publish them; require a deprecation window for breaking changes.
- **Distribute cross-cutting concerns as versioned libraries** — authentication, logging, tracing. Never share business logic between services.
- **Establish database change governance** on day one: migrations must be backward-compatible during deployment, because multiple service versions will run against one schema.
## Usage Guidelines
 
**When to use this pattern**
 
- Domain boundaries are identifiable but data is too relationally coupled to decompose economically.
- ACID transactions across the business process are a hard requirement.
- Deployment independence and fault isolation are needed at domain granularity, not per-operation.
- The organisation lacks the operational maturity for a large microservices estate, or is unwilling to fund it.
- A monolith needs decomposing incrementally, with an option to go further later.
**When not to use this pattern**
 
- Individual operations require independent elastic scaling — the pattern scales whole domains.
- The system is small enough that a modular monolith serves the same goals more cheaply.
- Domains genuinely have independent data with no cross-domain transactional requirement — full microservices will serve better.
- The database is already the primary bottleneck; this pattern concentrates load on it rather than relieving it.
- Domain boundaries are unknown. Partitioning on guesses produces chatty services and duplicated logic, and the boundaries are expensive to move afterwards.
## Consequences
 
### Benefits
 
- Domain services deploy on independent cadences; release risk is scoped to one domain.
- Failure in one service does not, by default, take down the others.
- ACID transactions and referential integrity are retained — no sagas, no distributed transaction coordination, no eventual-consistency reconciliation.
- Testing scope shrinks to the changed domain plus its documented contracts.
- Team ownership maps cleanly to services, reducing cross-team coordination.
- Substantially cheaper and faster to reach than microservices, while remaining a viable end state rather than merely a waypoint.
### Trade-offs
 
- The shared database is a single point of failure and the chief constraint on evolution.
- Database schema change becomes a governance problem requiring coordination and a compatibility policy.
- Elasticity is limited — a single hot operation forces scaling of its entire service.
- Operational surface grows with the number of services: pipelines, dashboards, alerts.
- Incorrect domain boundaries produce chatty inter-service calls and duplicated logic, and are costly to correct.
- Distributed debugging requires correlation identifiers and tracing that a monolith did not need.
## Variants
 
- **With and without an API layer.** Small estates may have the UI call services directly; larger ones benefit from a gateway for cross-cutting concerns.
- **Monolithic versus domain-partitioned user interface.** A partitioned UI extends independent deployability to the front end at the cost of a shell and shared design system.
- **Shared schema versus partitioned schemas.** Logical partitioning with views is the stronger form and preserves a migration path; a fully shared schema is simpler but couples services to each other's tables.
- **Partially separated data.** Individual domains with genuinely independent data may take their own database while the rest continue to share, producing a hybrid that shades toward microservices.
- **Event-augmented.** Domain services publish events for cross-domain notification while retaining the shared database for transactional reads. See the Event-Driven Architecture pattern.
## Example
 
An insurance claims platform is partitioned into five services: Policy, Claims, Payments, Documents, and Reporting.
 
Claims changes weekly as products and rules evolve; Payments changes quarterly and is subject to financial controls; Reporting changes constantly but carries no transactional risk. As a monolith all three shared one fortnightly release train, and a Reporting query could exhaust the connection pool used by Claims.
 
After partitioning, each service deploys independently. The claim settlement workflow — which must atomically update a claim, record a payment authorisation, and write an audit entry — remains a single ACID transaction, because all three schemas live in one database. Reporting reads Policy and Claims data through views owned by those domains, so a Claims table restructuring does not break it.
 
Elasticity is the accepted cost: a surge in document uploads requires scaling the entire Documents service rather than only its upload endpoint.
 
## Known Uses
 
- {system or project 1}
- {system or project 2}
## Related Decisions / ADRs
 
- ADR-001: Adopt Service-Based Architecture
- {link or reference 2}
## References
 
- Richards, M. & Ford, N. — *Fundamentals of Software Architecture*, chapter on service-based architecture
- Richards, M. — *Software Architecture Patterns*
- Newman, S. — *Monolith to Microservices* (decomposition techniques, database partitioning)
## Revision History
 
| Date | Version | Notes |
|------|---------|-------|
| 2026-08-05 | 1.0 | Initial version |
 
