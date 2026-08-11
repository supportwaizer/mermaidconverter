# Portfolio Reviewer Responsibilities

## 1. Role Purpose

The **Portfolio Reviewer** serves as the first line of architecture assurance within the Federated Architecture Review Process.

The Portfolio Reviewer performs a structured review of proposed solutions against published enterprise architecture standards, patterns, principles, and Architecture Decision Records (ADRs).

The objective is to allow solutions that clearly conform to established architecture guidance to proceed without requiring a detailed Solution Architecture review, while ensuring that exceptions, significant risks, and architectural decisions requiring additional judgment are escalated appropriately.

A Portfolio Reviewer is responsible for **evaluating and demonstrating conformance to established architecture guidance**. The role does not replace Solution Architecture's responsibility for enterprise architecture policy, architectural exceptions, or decisions requiring broader architectural judgment.

---

## 2. Portfolio Reviewer Responsibilities

| Responsibility | Portfolio Reviewer Responsibility | Required Enablers |
|---|---|---|
| Own the review | Take responsibility for completing the Portfolio Review and ensuring the review reaches an appropriate disposition. | Review workflow, ownership model, defined review states |
| Validate review applicability | Confirm that the request requires architecture review and determine which review requirements apply. | Review applicability criteria and examples |
| Validate architecture documentation | Ensure sufficient solution documentation exists to perform the review. | Required-artifact checklist, solution-design template |
| Perform architecture review | Evaluate the proposed solution against applicable enterprise architecture guidance. | Self-review framework and published architecture guidance |
| Identify applicable standards | Determine which principles, standards, patterns and ADRs apply to the solution. | Searchable architecture knowledge repository |
| Evaluate pattern compliance | Determine whether the solution conforms to applicable approved architecture patterns. | Pattern applicability and compliance criteria |
| Evaluate standards compliance | Verify compliance with mandatory enterprise architecture standards. | Explicit, testable architecture standards |
| Validate ADR alignment | Determine whether existing enterprise/domain architecture decisions apply and whether the solution conforms to them. | Published ADR catalog with applicability/scope |
| Identify deviations and exceptions | Explicitly document deviations from established architecture guidance. | Exception taxonomy and exception template |
| Assess architecture risk | Evaluate architectural risk associated with the solution and identified deviations. | Risk-assessment criteria |
| Classify the review | Determine the appropriate review classification based on established criteria. | Green/Amber/Red classification rules |
| Collect review evidence | Ensure compliance conclusions are supported by appropriate evidence. | Evidence requirements and artifact repository |
| Validate architecture decisions | Ensure significant solution-specific architecture decisions are documented. | ADR template and ADR guidance |
| Resolve routine findings | Work with the solution team to resolve documentation gaps and straightforward compliance issues. | Remediation guidance and published examples |
| Determine escalation | Determine whether the solution falls within delegated Portfolio Review authority or requires Solution Architecture involvement. | Explicit escalation criteria |
| Prepare escalation package | Clearly identify the reason for escalation and the specific architectural question requiring SA attention. | Standard escalation template |
| Coordinate specialist advice | Ensure required ODT or specialist concerns are identified and routed appropriately through the process. | ODT engagement criteria |
| Incorporate feedback | Ensure SA/ODT feedback and requested changes are reflected in the solution and review record. | Findings/action tracking |
| Approve within delegated authority | Approve reviews that satisfy published requirements and fall within Portfolio Reviewer authority. | Defined delegated approval authority |
| Maintain traceability | Preserve the review decision, evidence, exceptions, reviewers and supporting artifacts. | Architecture review system of record |
| Support tollgate approval | Provide evidence that the required architecture review has been completed. | Standard review outcome/attestation |

---

## 3. Portfolio Reviewer Self-Review Responsibility

The Portfolio Review should not be based simply on the reviewer's opinion that the architecture is acceptable.

The Portfolio Reviewer should establish:

> **Which architecture requirements apply to the proposed solution, whether the solution conforms to those requirements, what evidence demonstrates conformance, and what deviations or exceptions exist.**

Example:

```text
Applicable Pattern: REST API Pattern
Applicability: Yes — solution exposes synchronous APIs to internal consumers.
Compliance: COMPLIANT

Evidence:
- API defined using OpenAPI 3.x
- Approved authentication mechanism used
- Standard HTTP response codes followed
- Enterprise error-response structure used
- Published API versioning convention followed
- API registered with approved API platform

Architecture Artifacts:
- Solution Design §4.3
- payments-api.yaml

Exceptions: None
```

The Portfolio Review therefore becomes an **evidence-based architecture conformance assessment**.

---

## 4. Architecture Guidance Required by Portfolio Reviewers

Portfolio Reviewers need clear and consumable architecture guidance.

### 4.1 Architecture Principles

Examples include API-first design, reuse before build, loose coupling, security by design, observability by default, platform alignment, data ownership, and authoritative data-source principles.

### 4.2 Architecture Standards

Standards should define:
- Requirement
- Applicability
- Mandatory vs. recommended status
- Compliance criteria
- Evidence required
- Exceptions
- Escalation requirements

---

## 5. Approved Architecture Pattern Catalog

Portfolio Reviewers need access to a published catalog of approved architecture patterns.

```text
Integration
├── REST API
├── Event-Driven Integration
├── Asynchronous Messaging
├── Batch / File Integration
└── External Partner Integration

Application
├── Web Application
├── Microservice
├── Modular Application
└── Scheduled / Batch Application

Data
├── Operational Database
├── Data Replication
├── Event-Based Data Distribution
├── Caching
└── Analytics / Data Platform

Security
├── Service Authentication
├── User Authentication
├── Authorization
├── Secrets Management
└── Encryption

Platform
├── Container Deployment
├── Cloud Application
├── SaaS Integration
└── Legacy Integration
```

Each pattern should define: **Purpose → Applicability → Architecture → Required Elements → Recommended Practices → Prohibited Practices → Compliance Criteria → Evidence → Exceptions → Escalation Triggers**.

---

## 6. Architecture Decision Records

Portfolio Reviewers should determine whether existing ADRs apply, whether the solution complies, whether a new solution-level ADR is required, and whether the solution conflicts with an existing decision.

A conflict with an applicable enterprise architecture decision may trigger escalation.

---

## 7. Portfolio Review Questionnaire

Portfolio Reviewers need a structured questionnaire that applies review criteria conditionally based on the characteristics of the solution.

Examples:
- API used → apply API Architecture criteria.
- Events used → apply Event-Driven Architecture criteria.
- Business data persisted → apply Data Architecture criteria.
- New technology introduced → evaluate SA escalation.

---

## 8. Evidence Requirements

Acceptable evidence may include:
- Solution architecture diagram
- Context/component/integration diagrams
- Sequence and data-flow diagrams
- Deployment diagram
- OpenAPI specification
- Event/schema definition
- Security design
- Technology inventory
- ADR
- Configuration reference
- Pattern compliance assessment
- Exception record

> **Portfolio Reviewers do not simply assert compliance; they demonstrate compliance.**

---

## 9. Review Classification

| Classification | Description | Portfolio Reviewer Action |
|---|---|---|
| Green | Conforms to applicable standards, patterns and ADRs with no material exceptions. | May approve within delegated authority. |
| Amber | Contains uncertainty, architectural risk, or controlled deviation requiring additional advice or judgment. | Obtain advice or escalate according to established criteria. |
| Red | Contains significant exceptions, new architectural direction, significant risk, or conflict with mandatory guidance. | Solution Architecture review required. |

---

## 10. Escalation Responsibility

Potential escalation triggers include:
- New technology or platform
- Exception to a mandatory standard
- Deviation from an approved pattern
- No approved pattern for the proposed approach
- Conflict with an enterprise/domain ADR
- New enterprise or cross-domain decision
- Significant security or data architecture impact
- Creation/change of a system of record
- Significant cross-domain integration
- Material availability/resiliency concerns
- Unsupported/non-standard technology
- Significant external integration
- Unresolved ODT concern
- Risk exceeding delegated Portfolio Review authority

---

## 11. Escalation Package

An escalation should identify the specific architectural issue requiring SA judgment rather than asking SA to repeat the entire review.

```text
Architecture Escalation

Solution: Customer Payment Service
Portfolio Review Status: Completed

Applicable Patterns:
- REST API Pattern: Compliant
- Event Driven Pattern: Compliant
- Data Access Pattern: Exception

Escalation Trigger: Deviation from INT-014

Issue:
The solution requires synchronous access to System X.
The approved event interface does not provide the required information.

Risk:
Creates synchronous runtime dependency on System X.

Proposed Mitigation:
Timeout, circuit breaker and cached fallback.

Specific SA Decision Requested:
Approve the proposed exception to INT-014.

Supporting Evidence:
- Architecture diagram
- Sequence diagram
- ADR-027
- Portfolio Review assessment
```

---

## 12. Portfolio Review Record

Each completed Portfolio Review should produce a standardized record containing:

1. Review Information
2. Solution Overview
3. Applicable Architecture Guidance
4. Review Results and Evidence
5. Exceptions / Deviations
6. Architecture Decisions
7. Risk Classification
8. Escalation Assessment
9. Portfolio Review Decision
10. Supporting Evidence
11. Review Attestation

---

## 13. Portfolio Reviewer vs. Solution Architecture Responsibility

### Portfolio Reviewer

> **Does this solution conform to established architecture guidance, and can we demonstrate that conformance?**

The Portfolio Reviewer operates primarily within existing architectural guardrails.

### Solution Architecture

> **What should the architectural direction be when existing guidance is insufficient, an exception is required, or the decision has broader architectural consequences?**

Solution Architecture handles architectural judgment beyond the delegated authority of the Portfolio Reviewer.

> **Portfolio Reviewers own conformance. Solution Architecture owns architectural judgment and exceptions.**

This distinction allows routine, standards-conforming solutions to proceed through Portfolio Review while Solution Architects focus on exceptions, novel architecture decisions, higher-risk designs, and issues with broader enterprise impact.
