from pathlib import Path
from datetime import date

ROOT = Path("architecture-patterns")

# ============================================================
# Pattern catalog
#
# phase:
#   1 = Core guardrails required to enable federated assurance
#   2 = Broader engineering/platform standardization
#   3 = Advanced, specialized, or transformation patterns
#
# assurance:
#   GREEN = normally self-service when pattern is followed
#   AMBER = typically requires targeted architecture review
#   RED   = typically requires formal architecture review
#   TBD   = must be determined when pattern is authored
# ============================================================

CATALOG = {

    # ========================================================
    # 1. APPLICATION ARCHITECTURE
    # ========================================================
    "application": {

        "application-structure": [
            ("layered-architecture.md", 2, "GREEN"),
            ("modular-monolith.md", 2, "GREEN"),
            ("microservices-architecture.md", 1, "AMBER"),
            ("hexagonal-architecture.md", 2, "GREEN"),
            ("clean-architecture.md", 2, "GREEN"),
            ("backend-for-frontend.md", 2, "GREEN"),
        ],

        "domain-service-design": [
            ("domain-driven-design.md", 2, "GREEN"),
            ("bounded-context.md", 2, "GREEN"),
            ("domain-service.md", 2, "GREEN"),
            ("application-service.md", 2, "GREEN"),
            ("anti-corruption-layer.md", 2, "GREEN"),
            ("strangler-fig.md", 3, "AMBER"),
        ],

        "state-session": [
            ("stateless-service.md", 1, "GREEN"),
            ("externalized-session-state.md", 2, "GREEN"),
            ("distributed-cache.md", 2, "AMBER"),
            ("state-machine.md", 3, "AMBER"),
        ],
    },

    # ========================================================
    # 2. INTEGRATION ARCHITECTURE
    # ========================================================
    "integration": {

        "synchronous": [
            ("rest-api.md", 1, "GREEN"),
            ("graphql-api.md", 3, "AMBER"),
            ("grpc.md", 2, "AMBER"),
            ("api-gateway.md", 1, "GREEN"),
            ("api-composition.md", 2, "GREEN"),
            ("backend-for-frontend.md", 2, "GREEN"),
        ],

        "asynchronous": [
            ("event-driven-architecture.md", 1, "GREEN"),
            ("publish-subscribe.md", 1, "GREEN"),
            ("point-to-point-messaging.md", 1, "GREEN"),
            ("competing-consumers.md", 2, "GREEN"),
            ("event-notification.md", 2, "GREEN"),
            ("event-carried-state-transfer.md", 2, "AMBER"),
            ("request-reply-messaging.md", 2, "GREEN"),
        ],

        "reliable-messaging": [
            ("transactional-outbox.md", 1, "GREEN"),
            ("inbox-deduplication.md", 1, "GREEN"),
            ("idempotent-consumer.md", 1, "GREEN"),
            ("dead-letter-queue.md", 1, "GREEN"),
            ("retry-with-backoff.md", 1, "GREEN"),
            ("poison-message-handling.md", 1, "GREEN"),
        ],

        "batch-file": [
            ("managed-file-transfer.md", 1, "GREEN"),
            ("batch-interface.md", 2, "GREEN"),
            ("bulk-data-transfer.md", 2, "GREEN"),
            ("scheduled-data-exchange.md", 2, "GREEN"),
        ],
    },

    # ========================================================
    # 3. DATA ARCHITECTURE
    # ========================================================
    "data": {

        "transactional": [
            ("database-per-service.md", 1, "GREEN"),
            ("shared-database.md", 1, "AMBER"),
            ("repository.md", 3, "GREEN"),
            ("unit-of-work.md", 3, "GREEN"),
            ("optimistic-locking.md", 2, "GREEN"),
        ],

        "distributed-data": [
            ("saga.md", 2, "AMBER"),
            ("cqrs.md", 3, "AMBER"),
            ("event-sourcing.md", 3, "RED"),
            ("materialized-view.md", 2, "GREEN"),
            ("distributed-cache.md", 2, "AMBER"),
        ],

        "analytical": [
            ("data-lake.md", 2, "AMBER"),
            ("data-warehouse.md", 2, "GREEN"),
            ("lakehouse.md", 2, "AMBER"),
            ("data-mart.md", 2, "GREEN"),
            ("medallion-architecture.md", 2, "GREEN"),
            ("data-mesh.md", 3, "RED"),
        ],

        "data-movement": [
            ("etl.md", 2, "GREEN"),
            ("elt.md", 2, "GREEN"),
            ("change-data-capture.md", 2, "AMBER"),
            ("streaming-ingestion.md", 2, "AMBER"),
            ("data-replication.md", 2, "AMBER"),
        ],

        "governance": [
            ("system-of-record.md", 1, "GREEN"),
            ("master-data-management.md", 2, "AMBER"),
            ("data-classification.md", 1, "GREEN"),
            ("data-retention.md", 1, "GREEN"),
            ("data-masking.md", 1, "GREEN"),
            ("tokenization.md", 2, "AMBER"),
        ],
    },

    # ========================================================
    # 4. SECURITY ARCHITECTURE
    # ========================================================
    "security": {

        "identity-access": [
            ("oauth2.md", 1, "GREEN"),
            ("openid-connect.md", 1, "GREEN"),
            ("single-sign-on.md", 1, "GREEN"),
            ("identity-federation.md", 2, "AMBER"),
            ("service-identity.md", 1, "GREEN"),
            ("least-privilege.md", 1, "GREEN"),
        ],

        "api-service-security": [
            ("api-gateway-security.md", 1, "GREEN"),
            ("zero-trust-service-access.md", 2, "AMBER"),
            ("mutual-tls.md", 2, "GREEN"),
            ("token-validation.md", 1, "GREEN"),
        ],

        "secrets-keys": [
            ("secrets-management.md", 1, "GREEN"),
            ("key-management.md", 1, "GREEN"),
            ("certificate-management.md", 1, "GREEN"),
            ("credential-rotation.md", 1, "GREEN"),
        ],

        "data-protection": [
            ("encryption-in-transit.md", 1, "GREEN"),
            ("encryption-at-rest.md", 1, "GREEN"),
            ("data-masking.md", 1, "GREEN"),
            ("tokenization.md", 2, "AMBER"),
            ("sensitive-data-minimization.md", 1, "GREEN"),
        ],
    },

    # ========================================================
    # 5. RESILIENCE & RELIABILITY
    # ========================================================
    "resilience-reliability": {

        "patterns": [
            ("circuit-breaker.md", 1, "GREEN"),
            ("timeout.md", 1, "GREEN"),
            ("retry-with-backoff.md", 1, "GREEN"),
            ("bulkhead.md", 2, "GREEN"),
            ("graceful-degradation.md", 2, "GREEN"),
            ("health-check.md", 1, "GREEN"),
            ("failover.md", 1, "GREEN"),
            ("active-active.md", 3, "RED"),
            ("active-passive.md", 2, "AMBER"),
            ("disaster-recovery.md", 1, "GREEN"),
            ("rate-limiting.md", 1, "GREEN"),
            ("load-shedding.md", 2, "GREEN"),
        ],
    },

    # ========================================================
    # 6. CLOUD & PLATFORM ARCHITECTURE
    # ========================================================
    "cloud-platform": {

        "deployment": [
            ("containerized-application.md", 1, "GREEN"),
            ("kubernetes-deployment.md", 1, "GREEN"),
            ("serverless-function.md", 2, "AMBER"),
            ("platform-as-a-service.md", 2, "GREEN"),
            ("immutable-infrastructure.md", 2, "GREEN"),
        ],

        "cloud-topology": [
            ("single-region.md", 2, "GREEN"),
            ("multi-region.md", 3, "RED"),
            ("multi-availability-zone.md", 1, "GREEN"),
            ("hub-and-spoke-network.md", 2, "AMBER"),
            ("landing-zone.md", 1, "GREEN"),
        ],

        "configuration": [
            ("externalized-configuration.md", 1, "GREEN"),
            ("configuration-as-code.md", 2, "GREEN"),
            ("infrastructure-as-code.md", 1, "GREEN"),
            ("feature-flags.md", 2, "GREEN"),
        ],

        "platform-services": [
            ("service-discovery.md", 2, "GREEN"),
            ("api-gateway.md", 1, "GREEN"),
            ("service-mesh.md", 3, "RED"),
            ("managed-database.md", 1, "GREEN"),
            ("managed-messaging.md", 1, "GREEN"),
        ],
    },

    # ========================================================
    # 7. DEVOPS & DELIVERY
    # ========================================================
    "devops-delivery": {

        "patterns": [
            ("ci-cd-pipeline.md", 1, "GREEN"),
            ("trunk-based-development.md", 2, "GREEN"),
            ("gitops.md", 2, "GREEN"),
            ("blue-green-deployment.md", 2, "GREEN"),
            ("canary-deployment.md", 2, "GREEN"),
            ("rolling-deployment.md", 1, "GREEN"),
            ("feature-toggle.md", 2, "GREEN"),
            ("automated-rollback.md", 2, "GREEN"),
            ("artifact-promotion.md", 1, "GREEN"),
        ],
    },

    # ========================================================
    # 8. OBSERVABILITY & OPERATIONS
    # ========================================================
    "observability-operations": {

        "patterns": [
            ("centralized-logging.md", 1, "GREEN"),
            ("structured-logging.md", 1, "GREEN"),
            ("correlation-id.md", 1, "GREEN"),
            ("distributed-tracing.md", 1, "GREEN"),
            ("metrics-monitoring.md", 1, "GREEN"),
            ("health-monitoring.md", 1, "GREEN"),
            ("audit-logging.md", 1, "GREEN"),
            ("sli-slo.md", 2, "GREEN"),
            ("alerting.md", 1, "GREEN"),
        ],
    },

    # ========================================================
    # 9. UI / DIGITAL EXPERIENCE
    # ========================================================
    "ui-digital-experience": {

        "patterns": [
            ("single-page-application.md", 2, "GREEN"),
            ("server-side-rendering.md", 2, "GREEN"),
            ("micro-frontends.md", 3, "AMBER"),
            ("backend-for-frontend.md", 2, "GREEN"),
            ("responsive-web.md", 2, "GREEN"),
            ("progressive-web-app.md", 3, "AMBER"),
            ("design-system.md", 2, "GREEN"),
        ],
    },

    # ========================================================
    # 10. LEGACY & MODERNIZATION
    # ========================================================
    "legacy-modernization": {

        "patterns": [
            ("strangler-fig.md", 2, "GREEN"),
            ("anti-corruption-layer.md", 2, "GREEN"),
            ("facade-over-legacy.md", 2, "GREEN"),
            ("api-enablement.md", 2, "GREEN"),
            ("replatform.md", 2, "AMBER"),
            ("refactor.md", 2, "GREEN"),
            ("rehost.md", 2, "GREEN"),
            ("replace.md", 3, "RED"),
        ],
    },

    # ========================================================
    # 11. ARCHITECTURE GOVERNANCE
    # ========================================================
    "architecture-governance": {

        "patterns": [
            ("architecture-decision-record.md", 1, "GREEN"),
            ("reference-architecture.md", 1, "GREEN"),
            ("technology-standard.md", 1, "GREEN"),
            ("architecture-exception.md", 1, "AMBER"),
            ("architecture-waiver.md", 1, "AMBER"),
            ("self-attestation.md", 1, "GREEN"),
            ("architecture-fitness-function.md", 2, "GREEN"),
            ("architecture-compliance-check.md", 1, "GREEN"),
        ],
    },
}


# ============================================================
# Helpers
# ============================================================

def pretty_name(value: str) -> str:
    return value.replace("-", " ").title()


def title_from_filename(filename: str) -> str:
    return pretty_name(filename.removesuffix(".md"))


def pattern_id(domain: str, category: str, filename: str) -> str:
    """
    Creates stable unique IDs such as:

        integration.synchronous.rest-api
        security.identity-access.oauth2
    """
    name = filename.removesuffix(".md")
    return f"{domain}.{category}.{name}"


def pattern_type(domain: str, category: str) -> str:
    mapping = {
        "application": "Application Pattern",
        "integration": "Integration Pattern",
        "data": "Data Pattern",
        "security": "Security Pattern",
        "resilience-reliability": "Resilience Pattern",
        "cloud-platform": "Platform Pattern",
        "devops-delivery": "Delivery Pattern",
        "observability-operations": "Operational Pattern",
        "ui-digital-experience": "Experience Pattern",
        "legacy-modernization": "Modernization Pattern",
        "architecture-governance": "Governance Pattern",
    }

    return mapping.get(domain, "Architecture Pattern")


# ============================================================
# Markdown placeholder
# ============================================================

def placeholder_content(
    domain: str,
    category: str,
    filename: str,
    phase: int,
    assurance: str,
) -> str:

    title = title_from_filename(filename)
    pid = pattern_id(domain, category, filename)

    return f"""---
id: "{pid}"
title: "{title}"
status: "Placeholder"
version: "0.1"
phase: {phase}

owners:
  - "Enterprise Architecture"

classification:
  domain: "{pretty_name(domain)}"
  category: "{pretty_name(category)}"
  type: "{pattern_type(domain, category)}"
  assurance-impact: "{assurance}"
  maturity: "Placeholder"

tags: []
related-patterns: []
---

# {title}

## Problem

TODO: Describe the recurring architectural problem this pattern addresses.


## Context

TODO: Describe the situations in which this pattern applies.

- Business context:
- Technical context:
- Regulatory/compliance context:
- Organizational context:
- Assumptions:
- Constraints:


## Forces

- TODO


## Solution

TODO: Describe the recommended architectural solution.


## Structure

TODO: Describe the major components and their relationships.


## Implementation

TODO: Describe implementation guidance without making the pattern
unnecessarily technology-specific.


## Usage Guidelines

### When to use this pattern

- TODO


### When not to use this pattern

- TODO


## Consequences

### Benefits

- TODO


### Trade-offs

- TODO


## Variants

- TODO


## Example

TODO: Provide a concrete example.


## Known Uses

- TODO


## Related Decisions / ADRs

- TODO


## References

- TODO


## Compliance Criteria

### Required

- [ ] TODO


### Recommended

- [ ] TODO


### Prohibited

- [ ] TODO


## Revision History

| Date | Version | Notes |
|------|---------|-------|
| YYYY-MM-DD | 0.1 | Initial placeholder |
"""


# ============================================================
# Pattern template
# ============================================================

PATTERN_TEMPLATE = """---
id: ""
title: "Pattern Name"
status: "Draft"
version: "0.1"
phase: 0

owners:
  - "Enterprise Architecture"

classification:
  domain: ""
  category: ""
  type: ""
  assurance-impact: ""
  maturity: "Draft"

tags: []
related-patterns: []
---

# Pattern Name

## Problem

Describe the recurring architectural problem.


## Context

Describe when the pattern applies.

- Business context:
- Technical context:
- Regulatory/compliance context:
- Organizational context:
- Assumptions:
- Constraints:


## Forces

- ...


## Solution

Describe the recommended architectural solution.


## Structure

Describe the components and relationships.


## Implementation

Provide implementation guidance.


## Usage Guidelines

### When to use this pattern

- ...

### When not to use this pattern

- ...


## Consequences

### Benefits

- ...

### Trade-offs

- ...


## Variants

- ...


## Example

Provide a concrete example.


## Known Uses

- ...


## Related Decisions / ADRs

- ...


## References

- ...


## Compliance Criteria

### Required

- [ ] ...

### Recommended

- [ ] ...

### Prohibited

- [ ] ...


## Revision History

| Date | Version | Notes |
|------|---------|-------|
| YYYY-MM-DD | 0.1 | Initial draft |
"""


# ============================================================
# README
# ============================================================

README_CONTENT = """# Enterprise Architecture Pattern Catalog

This repository contains the enterprise architecture pattern catalog used to
support Federated Architecture Assurance.

The complete target-state taxonomy is represented in the repository even though
patterns are implemented incrementally.

## Delivery Phases

### Phase 1 — Federated Assurance Foundation

Patterns required to move routine architecture decisions from centralized
architecture review to governed team self-assessment.

Focus areas include:

- REST APIs
- Event-driven integration
- Security
- Authentication and authorization
- Messaging reliability
- Data protection
- Resilience
- Observability
- Standard cloud deployment
- Architecture governance
- Self-attestation
- Architecture exceptions

### Phase 2 — Engineering Standardization

Patterns that expand the catalog into broader engineering and platform practices.

Focus areas include:

- Application design
- Domain design
- Advanced messaging
- Data architecture
- Analytics
- DevOps
- Cloud topology
- Modernization
- Digital experience

### Phase 3 — Advanced Architecture

Patterns that tend to require greater architectural maturity or carry
significant complexity.

Examples include:

- Event Sourcing
- CQRS
- Data Mesh
- Service Mesh
- Multi-region architecture
- Active/Active architecture
- Micro Frontends
- Strategic replacement programs

## Assurance Classification

Patterns also indicate their typical Architecture Assurance impact.

### GREEN

The pattern represents an approved architecture guardrail.

A solution conforming to the pattern can normally proceed through
self-assessment and attestation.

### AMBER

Use or deviation normally warrants targeted Architecture review.

### RED

The architecture normally warrants formal Architecture review.

Actual classification may be elevated based on solution context, risk,
regulation, criticality, or exceptions.

## Pattern Lifecycle

Recommended lifecycle:

Placeholder -> Draft -> Review -> Approved -> Deprecated -> Retired

## Catalog Manifest

`catalog.yaml` is the machine-readable index for this repository.

It contains:

- Pattern ID
- Title
- Repository path
- Domain
- Category
- Pattern type
- Delivery phase
- Lifecycle status
- Assurance impact

The manifest should eventually become the primary entry point for automated
Architecture Assurance tooling.
"""


# ============================================================
# YAML helpers
# ============================================================

def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def generate_catalog_yaml() -> str:

    lines = []

    lines.extend([
        'schema-version: "1.0"',
        'catalog-version: "1.0"',
        f'generated-date: "{date.today().isoformat()}"',
        '',
        'name: "Enterprise Architecture Pattern Catalog"',
        '',
        'default-owner:',
        '  - "Enterprise Architecture"',
        '',
        'lifecycle:',
        '  - "Placeholder"',
        '  - "Draft"',
        '  - "Review"',
        '  - "Approved"',
        '  - "Deprecated"',
        '  - "Retired"',
        '',
        'assurance-levels:',
        '  GREEN:',
        '    description: "Normally eligible for self-service architecture assurance."',
        '  AMBER:',
        '    description: "Normally requires targeted architecture review."',
        '  RED:',
        '    description: "Normally requires formal architecture review."',
        '',
        'delivery-phases:',
        '  1:',
        '    name: "Federated Assurance Foundation"',
        '    objective: "Establish core guardrails needed for architecture self-service."',
        '',
        '  2:',
        '    name: "Engineering Standardization"',
        '    objective: "Expand assurance into broader application, data and platform engineering."',
        '',
        '  3:',
        '    name: "Advanced Architecture"',
        '    objective: "Formalize advanced, specialized and transformation-oriented patterns."',
        '',
        'patterns:',
    ])

    for domain, categories in CATALOG.items():

        for category, patterns in categories.items():

            for filename, phase, assurance in patterns:

                pid = pattern_id(domain, category, filename)
                title = title_from_filename(filename)
                path = f"{domain}/{category}/{filename}"

                lines.extend([
                    f'  - id: {yaml_quote(pid)}',
                    f'    title: {yaml_quote(title)}',
                    f'    path: {yaml_quote(path)}',
                    f'    domain: {yaml_quote(pretty_name(domain))}',
                    f'    category: {yaml_quote(pretty_name(category))}',
                    f'    type: {yaml_quote(pattern_type(domain, category))}',
                    f'    phase: {phase}',
                    f'    status: "Placeholder"',
                    f'    assurance-impact: "{assurance}"',
                    f'    owner: "Enterprise Architecture"',
                    '',
                ])

    return "\n".join(lines)


# ============================================================
# File operations
# ============================================================

def create_file(path: Path, content: str):

    if path.exists():
        print(f"SKIP    {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        content,
        encoding="utf-8",
    )

    print(f"CREATE  {path}")


# ============================================================
# Repository creation
# ============================================================

def create_repository():

    ROOT.mkdir(parents=True, exist_ok=True)

    create_file(
        ROOT / "README.md",
        README_CONTENT,
    )

    create_file(
        ROOT / "PATTERN_TEMPLATE.md",
        PATTERN_TEMPLATE,
    )

    total_patterns = 0

    phase_counts = {
        1: 0,
        2: 0,
        3: 0,
    }

    assurance_counts = {
        "GREEN": 0,
        "AMBER": 0,
        "RED": 0,
    }

    for domain, categories in CATALOG.items():

        for category, patterns in categories.items():

            category_dir = ROOT / domain / category
            category_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            for filename, phase, assurance in patterns:

                file_path = category_dir / filename

                create_file(
                    file_path,
                    placeholder_content(
                        domain,
                        category,
                        filename,
                        phase,
                        assurance,
                    ),
                )

                total_patterns += 1
                phase_counts[phase] += 1
                assurance_counts[assurance] += 1

    # Manifest is regenerated each time because it is derived metadata.
    manifest_path = ROOT / "catalog.yaml"

    manifest_path.write_text(
        generate_catalog_yaml(),
        encoding="utf-8",
    )

    print(f"GENERATE {manifest_path}")

    print()
    print("=" * 72)
    print("ENTERPRISE ARCHITECTURE PATTERN CATALOG")
    print("=" * 72)

    print(f"Location: {ROOT.resolve()}")
    print(f"Patterns: {total_patterns}")

    print()
    print("Delivery phases")
    print("----------------")
    print(f"Phase 1: {phase_counts[1]}")
    print(f"Phase 2: {phase_counts[2]}")
    print(f"Phase 3: {phase_counts[3]}")

    print()
    print("Initial assurance classification")
    print("--------------------------------")
    print(f"GREEN : {assurance_counts['GREEN']}")
    print(f"AMBER : {assurance_counts['AMBER']}")
    print(f"RED   : {assurance_counts['RED']}")

    print()
    print("catalog.yaml regenerated successfully.")
    print("=" * 72)


if __name__ == "__main__":
    create_repository()
