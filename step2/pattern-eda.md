---
title: "Event-Driven Architecture Pattern"
status: "Approved"
date: "2026-08-09"
version: "1.0"
owners:
  - "Enterprise Architecture"
tags:
  - "integration"
  - "event-driven"
  - "messaging"
  - "streaming"
  - "asynchronous"
related-patterns:
  - "rest-api-integration-pattern"
  - "enterprise-observability-pattern"
  - "message-broker-pattern"
  - "event-schema-pattern"
  - "dead-letter-queue-pattern"
---

# Event-Driven Architecture Pattern

## Problem
Applications often need to communicate changes in business state, distribute
information to multiple consumers, and process workloads asynchronously without
creating tight runtime dependencies between systems.

Point-to-point synchronous integrations can increase coupling, reduce resilience,
and create cascading failures when downstream services are unavailable.

This pattern establishes the enterprise approach for publishing, consuming, and
processing business events using asynchronous messaging or event-streaming
platforms.

The objective is to enable loosely coupled, scalable, resilient, and observable
integration while maintaining clear ownership of events, schemas, delivery
semantics, and operational responsibilities.


## Context
Use this pattern when systems need to communicate asynchronously through events
representing business facts or changes in state.

- Business context:
  - A business event must notify one or more downstream systems.
  - Multiple consumers may independently react to the same event.
  - Immediate synchronous response from downstream systems is not required.
  - Business processes can tolerate eventual consistency.
  - Systems need to reduce direct runtime coupling.
  - Historical event streams may provide analytical or replay value.

- Technical context:
  - Communication uses an approved message broker or event-streaming platform.
  - Producers publish events without requiring direct knowledge of all consumers.
  - Consumers independently subscribe to events relevant to their business
    capabilities.
  - Events are processed asynchronously.
  - Event schemas are explicitly defined and version controlled.

- Regulatory/compliance context:
  - Events containing sensitive or regulated data must comply with applicable
    enterprise security, privacy, retention, and data-classification standards.
  - Event payloads must contain only the information necessary for intended
    consumers.
  - Access to topics, queues, streams, and event data must follow least-privilege
    principles.

- Organizational context:
  - Event producers own the semantic quality and lifecycle of the events they
    publish.
  - Event consumers own their processing logic, failure handling, and
    idempotency.
  - Teams are expected to use approved enterprise messaging or streaming
    platforms and published event standards.
  - Solutions conforming to this pattern may qualify for the Green Architecture
    Assurance path.

- Assumptions:
  - Eventual consistency is acceptable for the business use case.
  - Consumers can process events independently.
  - The enterprise provides approved event infrastructure.
  - Producers and consumers can tolerate temporary delays or outages.

- Constraints:
  - Approved enterprise messaging or streaming infrastructure must be used.
  - Event schemas must be defined and governed.
  - Events must not contain credentials or secrets.
  - Sensitive information must be protected according to enterprise standards.
  - Delivery semantics and retry behavior must be explicitly defined.


## Forces
- Loose coupling between producers and consumers.
- Scalability.
- Resilience.
- Eventual consistency.
- Message ordering.
- Duplicate delivery.
- Schema evolution.
- Consumer independence.
- Replay capability.
- Failure recovery.
- Observability.
- Data privacy.
- Operational complexity.
- Event ownership and governance.
- Avoidance of event proliferation and uncontrolled topic growth.


## Solution
Publish meaningful business events to an approved enterprise messaging or
event-streaming platform.

A business event represents a fact that has already occurred.

Examples:

    CustomerCreated
    CustomerAddressChanged
    OrderSubmitted
    PaymentReceived
    ShipmentDispatched

Producers publish events without invoking individual downstream consumers.

Consumers subscribe to events and independently determine how to react.

Event-driven solutions must define:

- Event ownership.
- Event schema.
- Event semantics.
- Delivery semantics.
- Ordering requirements.
- Retry behavior.
- Dead-letter handling.
- Idempotency strategy.
- Security requirements.
- Retention requirements.
- Observability requirements.


### Event Design

Events should represent meaningful business facts.

Prefer:

    OrderSubmitted
    PaymentReceived
    CustomerAddressChanged

Avoid events that expose implementation details such as:

    OrderTableUpdated
    DatabaseRowInserted
    CallServiceB

Events should describe what happened, rather than instructing another service
what to do.

Prefer:

    PaymentReceived

over:

    UpdateAccountBalance

unless a command pattern is explicitly required.


### Event Naming

Event names should:

- Use consistent enterprise naming conventions.
- Represent business meaning.
- Use past tense for events representing completed facts.
- Avoid implementation-specific terminology.

Examples:

    CustomerCreated
    OrderCancelled
    InvoiceGenerated
    PaymentFailed


### Event Payload

Event payloads should contain enough information for consumers to understand the
business event without unnecessary coupling to the producer's internal data model.

A typical event envelope may include:

    {
      "eventId": "8fbf0da6-...",
      "eventType": "OrderSubmitted",
      "eventVersion": "1.0",
      "eventTime": "2026-08-09T18:30:00Z",
      "source": "order-service",
      "correlationId": "cb5b...",
      "data": {
        "orderId": "12345",
        "customerId": "C9876"
      }
    }

Recommended metadata includes:

- Unique event identifier.
- Event type.
- Event schema/version.
- Event timestamp.
- Event source.
- Correlation identifier.
- Business payload.


### Event Schema

Every published event must have a documented schema.

The schema should be:

- Version controlled.
- Discoverable.
- Owned by the producing domain.
- Validated where supported by the platform.
- Evolved in a backward-compatible manner where possible.

Approved schema formats may include:

- JSON Schema.
- Avro.
- Protobuf.

The enterprise should define which schema mechanisms are preferred for each
messaging platform.


### Schema Evolution

Changes to event schemas must minimize disruption to existing consumers.

Prefer backward-compatible changes such as:

- Adding optional fields.
- Adding new event types.
- Extending enumerations where consumers tolerate unknown values.

Potentially breaking changes include:

- Removing fields.
- Renaming fields.
- Changing field types.
- Changing event meaning.
- Making optional fields mandatory.

Breaking changes normally require a new schema or event version.


### Producer Responsibilities

Event producers must:

- Publish events only after the corresponding business state change has been
  successfully committed.
- Ensure published events accurately represent business facts.
- Define event ownership.
- Maintain event schemas.
- Publish events to approved topics, queues, or streams.
- Avoid embedding consumer-specific logic into event production.
- Provide appropriate operational monitoring.

Where database state and event publication must remain consistent, an approved
transactional pattern such as the Transactional Outbox Pattern should be used.


### Consumer Responsibilities

Consumers must:

- Assume events may be delivered more than once unless the platform explicitly
  guarantees otherwise.
- Implement idempotent processing where duplicate delivery is possible.
- Handle temporary processing failures.
- Define retry behavior.
- Define poison-message handling.
- Monitor failed processing.
- Avoid making assumptions about other consumers.
- Maintain compatibility with supported event schema versions.


### Idempotency

Consumers should be designed to safely process duplicate events.

A common approach is to use the unique event identifier:

    eventId

Consumers may persist processed event identifiers or use business-level
idempotency keys.

Example:

    eventId = 8fbf0da6-...

If the event has already been processed successfully, the consumer should avoid
performing the business action again.


### Delivery Semantics

The expected delivery behavior must be documented.

Common models include:

- At-most-once.
- At-least-once.
- Effectively-once using application-level controls.

Teams should not assume "exactly once" end-to-end behavior without explicitly
validating platform and application guarantees.

For most enterprise event-driven solutions, consumers should be designed for
at-least-once delivery and therefore tolerate duplicates.


### Ordering

Event ordering requirements must be explicitly defined.

If order matters, the event design should identify the ordering key.

Example:

    customerId

or:

    orderId

Global ordering should be avoided unless absolutely required because it can
significantly reduce scalability.

Prefer ordering within a business entity or partition.


### Retry

Transient failures may be retried.

Retry policies must define:

- Maximum retry count.
- Backoff strategy.
- Maximum retry duration.
- Which errors are considered retryable.

Retries must be bounded.

Example:

    Attempt 1
    Wait 5 seconds

    Attempt 2
    Wait 30 seconds

    Attempt 3
    Wait 2 minutes

    Then route to dead-letter handling.


### Dead-Letter Handling

Events that cannot be processed successfully after the configured retry policy
must be handled through an approved failure mechanism such as a Dead Letter
Queue or Dead Letter Topic.

Dead-letter events should retain:

- Original event.
- Failure reason.
- Consumer identity.
- Failure timestamp.
- Retry information.
- Correlation identifier.

Operational procedures must exist for:

- Monitoring failed messages.
- Investigating failures.
- Correcting the underlying problem.
- Reprocessing events where appropriate.


### Event Replay

If event replay is required, the solution must define:

- Event retention period.
- Replay scope.
- Consumer reset/recovery procedure.
- Idempotency behavior.
- Impact on downstream systems.

Replay should not unintentionally recreate external side effects such as:

- Duplicate payments.
- Duplicate notifications.
- Duplicate orders.


### Security

Event-driven implementations must:

- Use approved authentication for platform access.
- Use authorization based on least privilege.
- Encrypt event traffic using approved transport security.
- Protect sensitive event data.
- Use approved secrets-management capabilities.
- Restrict producer and consumer access to required topics, queues, or streams.
- Comply with applicable data-classification and retention requirements.

Events must not contain:

- Passwords.
- API secrets.
- Authentication tokens.
- Unnecessary sensitive data.


### Data Minimization

Events should contain only data required to describe the business event and
support intended consumers.

Avoid publishing complete database records when only a small subset is needed.

For example, prefer:

    {
      "customerId": "12345",
      "status": "SUSPENDED"
    }

rather than publishing the entire customer profile if consumers only require
the status change.


### Observability

Every event-driven solution must participate in the enterprise observability
model.

At minimum, teams should monitor:

- Events published.
- Events consumed.
- Processing success/failure.
- Consumer lag.
- Retry counts.
- Dead-letter counts.
- Processing latency.
- Broker or platform availability.

Events should contain correlation identifiers where business transactions cross
multiple systems.

Distributed tracing should be used where supported.


### Event Ownership

Every event must have an identifiable owner.

The event owner is responsible for:

- Business meaning.
- Schema.
- Documentation.
- Versioning.
- Deprecation.
- Consumer communication.

The producing application should not necessarily control consumer behavior.


### Topic / Queue Ownership

Topics, queues, and event streams should have:

- Defined owner.
- Defined purpose.
- Naming convention.
- Retention policy.
- Security policy.
- Known producers.
- Known or discoverable consumers.

Unmanaged creation of new topics or queues should be avoided.


## Structure
A typical event-driven implementation is:

    Producer
       |
       | Publish Event
       v
    Enterprise Event Platform
       |
       +-------------------+
       |                   |
       v                   v
    Consumer A          Consumer B
       |                   |
       v                   v
    Business Action     Business Action


A more complete implementation may include:

    Business Service
          |
          v
    Transactional Outbox
          |
          v
    Event Publisher
          |
          v
    Event Broker / Streaming Platform
          |
       ---+----------------------
       |          |            |
       v          v            v
    Consumer A Consumer B   Consumer C
       |          |            |
       v          v            v
    Processing Processing   Processing
       |
       v
    Retry Mechanism
       |
       v
    Dead Letter Queue


Supporting enterprise capabilities may include:

    Schema Registry
    Identity Provider
    Secrets Management
    Central Logging
    Metrics Platform
    Distributed Tracing
    Event Catalog


## Implementation
The pattern is technology independent.

Approved implementations may use technologies such as:

- Apache Kafka.
- Enterprise message brokers.
- Cloud-native event services.
- JMS-compatible messaging platforms.
- Approved managed streaming services.

Applications should use approved enterprise client libraries and platform
standards rather than implementing proprietary messaging infrastructure.

For Java applications, common implementation approaches may include:

- Spring Boot.
- Spring Kafka.
- JMS.
- Spring Cloud Stream.

Technology selection should follow the enterprise technology catalog and
approved platform standards.


## Usage Guidelines

### When to use this pattern

Use this pattern when:

- A producer should not depend on consumer availability.
- Multiple consumers need to independently react to the same business event.
- Eventual consistency is acceptable.
- Processing should occur asynchronously.
- High-volume event distribution is required.
- Business events need to be streamed to multiple systems.
- Systems benefit from loose runtime coupling.
- Event replay provides business or operational value.


### When not to use this pattern

Do not automatically use event-driven architecture when:

- A caller requires an immediate response.
- A simple synchronous request/response interaction is sufficient.
- Strong immediate consistency is required across systems.
- The business operation cannot tolerate asynchronous completion.
- Event infrastructure would introduce unnecessary complexity for a simple
  integration.
- A batch or bulk-transfer pattern better fits the use case.

Consider the REST API Integration Pattern for synchronous interactions.


## Consequences
Event-driven architecture improves decoupling, scalability, and resilience but
introduces additional operational and design complexity.

Teams must explicitly manage eventual consistency, duplicate delivery, message
ordering, schema evolution, replay behavior, and failure recovery.


### Benefits

- Reduced runtime coupling between systems.
- Improved scalability.
- Improved resilience to temporary consumer outages.
- Support for multiple independent consumers.
- Better extensibility.
- Natural support for asynchronous workloads.
- Ability to replay events when using appropriate platforms.
- Improved integration flexibility.
- Reduced proliferation of direct point-to-point integrations.


### Trade-offs

- Eventual consistency may complicate business workflows.
- Debugging distributed asynchronous flows can be more difficult.
- Duplicate processing must be considered.
- Ordering guarantees may be limited.
- Schema evolution requires governance.
- Operational monitoring becomes more important.
- Message brokers and streaming platforms add infrastructure dependencies.
- Replaying events can cause unintended side effects if consumers are not
  designed correctly.


## Variants
Common variants include:

- Publish/Subscribe.
- Event Notification.
- Event-Carried State Transfer.
- Event Streaming.
- Competing Consumers.
- Domain Event.
- Integration Event.
- Transactional Outbox.
- Event Sourcing.

Event Sourcing should be treated as a specialized architectural pattern and
should not be assumed simply because an event broker is being used.


## Example
An Order Management application completes an order submission.

Rather than synchronously calling Inventory, Billing, Notification, and Analytics,
the Order service publishes:

    OrderSubmitted

Example:

    {
      "eventId": "87f73108-6bea-4dc3-a24f-...",
      "eventType": "OrderSubmitted",
      "eventVersion": "1.0",
      "eventTime": "2026-08-09T19:15:00Z",
      "source": "order-service",
      "correlationId": "ORD-12345",
      "data": {
        "orderId": "12345",
        "customerId": "C4567",
        "orderTotal": 425.75,
        "currency": "USD"
      }
    }

Consumers independently react:

    Inventory Service
        -> Reserve inventory

    Notification Service
        -> Send order confirmation

    Analytics Service
        -> Record business event

    Fulfillment Service
        -> Begin fulfillment workflow

The Order service does not need to know how each consumer processes the event.


## Known Uses
Examples of appropriate use include:

- Order lifecycle events.
- Customer lifecycle events.
- Payment processing notifications.
- Shipment and logistics events.
- Inventory changes.
- Fraud detection pipelines.
- Audit event streams.
- Application integration through enterprise messaging.
- Near-real-time analytics ingestion.


## Related Decisions / ADRs
- ADR defining the enterprise event-streaming platform.
- ADR defining the enterprise message broker.
- ADR defining event schema format.
- ADR defining event naming conventions.
- ADR defining event retention requirements.
- ADR defining retry and dead-letter handling.
- ADR defining transactional outbox implementation.
- ADR defining event security and access controls.


## References
- Enterprise Integration Standard.
- Enterprise Event Naming Standard.
- Enterprise Event Schema Standard.
- Enterprise Security Standard.
- Enterprise Observability Pattern.
- Enterprise Data Classification Standard.
- Approved Messaging / Event Streaming Platform Standard.


## Compliance Criteria

### Required

- [ ] An approved enterprise messaging or event-streaming platform is used.
- [ ] The event represents a clearly defined business fact or state change.
- [ ] The event has an identified business/technical owner.
- [ ] The event schema is documented and version controlled.
- [ ] Event schema evolution follows approved compatibility rules.
- [ ] A unique event identifier is included.
- [ ] Event type and event version are included.
- [ ] Event timestamp is included.
- [ ] Event source is identifiable.
- [ ] Correlation identifier is included where the event participates in a
      multi-system business transaction.
- [ ] Delivery semantics are documented.
- [ ] Consumer duplicate-processing behavior is defined.
- [ ] Consumers are idempotent where duplicate delivery is possible.
- [ ] Retry behavior is explicitly defined and bounded.
- [ ] Dead-letter/error handling is defined.
- [ ] Event ordering requirements are explicitly documented where applicable.
- [ ] Producers do not rely on consumer availability.
- [ ] Event payloads follow enterprise data-classification requirements.
- [ ] Credentials, access tokens, and secrets are not included in event payloads.
- [ ] Producer and consumer access follows least-privilege requirements.
- [ ] Event publication and consumption are monitored.
- [ ] Consumer failures and dead-letter events are monitored.
- [ ] Topic/queue/stream ownership is defined.
- [ ] Event retention requirements are documented.
- [ ] Replay behavior is defined if replay is supported or required.

### Recommended

- [ ] Transactional Outbox is used when consistency between database updates and
      event publication is required.
- [ ] A schema registry is used where supported by the platform.
- [ ] Distributed tracing is implemented where supported.
- [ ] Consumer lag is monitored for streaming implementations.
- [ ] Event payloads are minimized to required business information.
- [ ] Ordering is scoped to the smallest appropriate business key or partition.
- [ ] Events and schemas are registered in an enterprise event catalog.
- [ ] Reprocessing procedures are documented for dead-letter events.
- [ ] Consumer teams have automated compatibility tests against event schemas.

### Prohibited

- [ ] No credentials, passwords, secrets, or access tokens in event payloads.
- [ ] No unlimited retry loops.
- [ ] No silent discard of failed events without an approved failure strategy.
- [ ] No unmanaged production topics, queues, or streams.
- [ ] No undocumented breaking schema changes.
- [ ] No direct coupling of producers to specific consumer implementations.
- [ ] No assumption of exactly-once end-to-end processing without explicit
      architectural validation.
- [ ] No global ordering requirement unless justified and approved.
- [ ] No publication of unnecessary sensitive data.
- [ ] No use of database change events as business events unless explicitly
      approved as part of the architecture.


## Revision History

| Date       | Version | Notes           |
|------------|---------|-----------------|
| 2026-08-09 | 1.0     | Initial version |