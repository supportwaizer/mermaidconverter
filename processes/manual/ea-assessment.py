#!/usr/bin/env python3

"""
Interactive Enterprise Architecture Conformance Assessment

Expected repository layout:

architecture-patterns/
    catalog.yaml
    application/
    integration/
    data/
    security/
    ...

Run:

    python architecture_assessment.py

Optional:

    python architecture_assessment.py --catalog architecture-patterns
    python architecture_assessment.py --phase 1

Outputs:

    architecture-assessment-<timestamp>.json
    architecture-assessment-<timestamp>.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


# =====================================================================
# CONFIGURATION
# =====================================================================

DEFAULT_CATALOG = Path("architecture-patterns")

# Scoring weights.
#
# Required controls carry substantially more weight because they
# represent architecture guardrails.
#
WEIGHTS = {
    "required": 3,
    "recommended": 1,
    "prohibited": 3,
}

# Score thresholds. These affect the score-based recommendation.
# Risk triggers and exceptions can elevate the final assurance level.
SCORE_GREEN = 90
SCORE_AMBER = 70


# =====================================================================
# DESIGN INTAKE QUESTIONS
#
# "patterns" contains fragments matched against pattern IDs.
#
# This provides a first-generation applicability engine.
#
# In a later version these rules should move into catalog.yaml.
# =====================================================================

INTAKE_QUESTIONS = [
    {
        "id": "rest_api",
        "question": "Does the solution expose or consume REST/HTTP APIs?",
        "patterns": [
            "rest-api",
            "api-gateway",
            "oauth2",
            "openid-connect",
            "token-validation",
            "encryption-in-transit",
            "correlation-id",
            "structured-logging",
            "timeout",
            "retry-with-backoff",
            "rate-limiting",
        ],
    },
    {
        "id": "internet_facing",
        "question": "Will the solution expose an API or application to the public Internet?",
        "patterns": [
            "api-gateway",
            "api-gateway-security",
            "oauth2",
            "openid-connect",
            "token-validation",
            "encryption-in-transit",
            "rate-limiting",
            "secrets-management",
        ],
        "risk": "RED",
    },
    {
        "id": "event_driven",
        "question": "Does the solution publish or consume asynchronous events/messages?",
        "patterns": [
            "event-driven-architecture",
            "publish-subscribe",
            "point-to-point-messaging",
            "idempotent-consumer",
            "dead-letter-queue",
            "retry-with-backoff",
            "poison-message-handling",
            "correlation-id",
            "structured-logging",
            "managed-messaging",
        ],
    },
    {
        "id": "transactional_events",
        "question": (
            "Must a database transaction and event publication remain "
            "consistent?"
        ),
        "patterns": [
            "transactional-outbox",
            "inbox-deduplication",
            "idempotent-consumer",
        ],
    },
    {
        "id": "batch_file",
        "question": "Does the design use batch processing or file-based integration?",
        "patterns": [
            "managed-file-transfer",
            "batch-interface",
            "bulk-data-transfer",
            "scheduled-data-exchange",
        ],
    },
    {
        "id": "database",
        "question": "Does the solution persist transactional application data?",
        "patterns": [
            "managed-database",
            "database-per-service",
            "data-classification",
            "data-retention",
            "encryption-at-rest",
        ],
    },
    {
        "id": "shared_database",
        "question": "Will multiple independently deployed services share the same database/schema?",
        "patterns": [
            "shared-database",
        ],
        "risk": "AMBER",
    },
    {
        "id": "sensitive_data",
        "question": (
            "Will the solution store, process, or transmit sensitive, "
            "confidential, or regulated data?"
        ),
        "patterns": [
            "data-classification",
            "data-retention",
            "encryption-in-transit",
            "encryption-at-rest",
            "data-masking",
            "sensitive-data-minimization",
            "least-privilege",
            "audit-logging",
            "secrets-management",
        ],
        "risk": "AMBER",
    },
    {
        "id": "authentication",
        "question": "Does the solution authenticate users or service identities?",
        "patterns": [
            "oauth2",
            "openid-connect",
            "single-sign-on",
            "service-identity",
            "least-privilege",
            "secrets-management",
        ],
    },
    {
        "id": "containers",
        "question": "Will the application run in containers?",
        "patterns": [
            "containerized-application",
            "externalized-configuration",
            "health-check",
            "structured-logging",
            "metrics-monitoring",
            "secrets-management",
        ],
    },
    {
        "id": "kubernetes",
        "question": "Will the solution be deployed to Kubernetes?",
        "patterns": [
            "kubernetes-deployment",
            "containerized-application",
            "health-check",
            "externalized-configuration",
            "secrets-management",
            "metrics-monitoring",
        ],
    },
    {
        "id": "cloud",
        "question": "Will the solution be deployed to a public/private cloud platform?",
        "patterns": [
            "landing-zone",
            "infrastructure-as-code",
            "externalized-configuration",
            "managed-database",
            "managed-messaging",
        ],
    },
    {
        "id": "high_availability",
        "question": "Does the solution have high-availability or critical resilience requirements?",
        "patterns": [
            "health-check",
            "failover",
            "disaster-recovery",
            "timeout",
            "retry-with-backoff",
            "circuit-breaker",
            "graceful-degradation",
            "multi-availability-zone",
        ],
    },
    {
        "id": "multi_region",
        "question": "Does the proposed architecture require active use of multiple regions?",
        "patterns": [
            "multi-region",
            "disaster-recovery",
            "failover",
        ],
        "risk": "RED",
    },
    {
        "id": "active_active",
        "question": "Does the design use an active/active architecture?",
        "patterns": [
            "active-active",
        ],
        "risk": "RED",
    },
    {
        "id": "microservices",
        "question": "Is the proposed application using a microservices architecture?",
        "patterns": [
            "microservices-architecture",
            "stateless-service",
            "service-identity",
            "health-check",
            "correlation-id",
            "distributed-tracing",
        ],
        "risk": "AMBER",
    },
    {
        "id": "observability",
        "question": "Will this solution operate as a production service/application?",
        "patterns": [
            "centralized-logging",
            "structured-logging",
            "correlation-id",
            "metrics-monitoring",
            "health-monitoring",
            "alerting",
        ],
    },
    {
        "id": "cicd",
        "question": "Will application changes be delivered through an automated CI/CD pipeline?",
        "patterns": [
            "ci-cd-pipeline",
            "artifact-promotion",
            "automated-rollback",
        ],
    },
    {
        "id": "new_technology",
        "question": (
            "Does the solution introduce a technology, product, platform, "
            "database, framework, or SaaS product that is not currently approved?"
        ),
        "patterns": [],
        "risk": "RED",
    },
    {
        "id": "architecture_exception",
        "question": (
            "Is the team intentionally requesting an exception from an "
            "approved architecture standard or pattern?"
        ),
        "patterns": [
            "architecture-exception",
        ],
        "risk": "AMBER",
    },
]


# =====================================================================
# MODELS
# =====================================================================

@dataclass
class CriterionResult:
    category: str
    criterion: str
    answer: str
    compliant: Optional[bool]
    weight: int
    note: str = ""


@dataclass
class PatternAssessment:
    pattern_id: str
    title: str
    path: str
    phase: int
    catalog_assurance: str
    applicable: bool = True
    criteria: list[CriterionResult] = field(default_factory=list)
    score: Optional[float] = None
    required_failures: int = 0
    prohibited_violations: int = 0


# =====================================================================
# INPUT HELPERS
# =====================================================================

def heading(text: str):
    print()
    print("=" * 78)
    print(text)
    print("=" * 78)


def ask_text(prompt: str, required: bool = False) -> str:
    while True:
        value = input(f"{prompt}: ").strip()
        if value or not required:
            return value
        print("A value is required.")


def ask_yes_no(prompt: str, default: Optional[bool] = None) -> bool:
    if default is True:
        suffix = " [Y/n]"
    elif default is False:
        suffix = " [y/N]"
    else:
        suffix = " [y/n]"

    while True:
        value = input(prompt + suffix + ": ").strip().lower()

        if value == "" and default is not None:
            return default

        if value in {"y", "yes"}:
            return True

        if value in {"n", "no"}:
            return False

        print("Please enter y or n.")


def ask_control(
    prompt: str,
    prohibited: bool = False,
) -> tuple[str, Optional[bool], str]:

    print()
    print(prompt)

    if prohibited:
        print(
            "  y = design DOES violate this prohibition\n"
            "  n = design does NOT violate it\n"
            "  a = not applicable\n"
            "  u = unknown / evidence unavailable"
        )
    else:
        print(
            "  y = compliant\n"
            "  n = not compliant\n"
            "  a = not applicable\n"
            "  u = unknown / evidence unavailable"
        )

    while True:
        answer = input("Response [y/n/a/u]: ").strip().lower()

        if answer not in {"y", "n", "a", "u"}:
            print("Enter y, n, a, or u.")
            continue

        note = ""

        if answer in {"n", "u"} or (prohibited and answer == "y"):
            note = input("Optional note / evidence / rationale: ").strip()

        if answer == "a":
            return "N/A", None, note

        if answer == "u":
            return "UNKNOWN", False, note

        if prohibited:
            # "yes" means prohibited condition exists => nonconformant
            return ("VIOLATION" if answer == "y" else "COMPLIANT",
                    answer == "n",
                    note)

        return ("COMPLIANT" if answer == "y" else "NONCOMPLIANT",
                answer == "y",
                note)


# =====================================================================
# CATALOG
# =====================================================================

def load_catalog(root: Path) -> dict:
    manifest = root / "catalog.yaml"

    if not manifest.exists():
        raise FileNotFoundError(
            f"Could not find catalog manifest: {manifest}"
        )

    with manifest.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "patterns" not in data:
        raise ValueError(
            "catalog.yaml does not contain a 'patterns' collection."
        )

    return data


def normalize_pattern(raw: dict) -> dict:
    return {
        "id": str(raw.get("id", "")).strip(),
        "title": str(raw.get("title", "")).strip(),
        "path": str(raw.get("path", "")).strip(),
        "domain": str(raw.get("domain", "")).strip(),
        "category": str(raw.get("category", "")).strip(),
        "type": str(raw.get("type", "")).strip(),
        "phase": int(raw.get("phase", 0) or 0),
        "status": str(raw.get("status", "")).strip(),
        "assurance-impact": str(
            raw.get("assurance-impact", "GREEN")
        ).upper(),
    }


# =====================================================================
# COMPLIANCE CRITERIA PARSER
# =====================================================================

SECTION_RE = re.compile(
    r"^##\s+Compliance Criteria\s*$",
    re.IGNORECASE,
)

SUBSECTION_RE = re.compile(
    r"^###\s+(Required|Recommended|Prohibited)\s*$",
    re.IGNORECASE,
)

CHECKBOX_RE = re.compile(
    r"^\s*-\s*\[[ xX]\]\s+(.+?)\s*$"
)


def read_compliance_criteria(pattern_file: Path) -> dict[str, list[str]]:
    """
    Extract:

      ## Compliance Criteria

      ### Required
      - [ ] ...

      ### Recommended
      - [ ] ...

      ### Prohibited
      - [ ] ...

    Multi-line checkbox criteria are also supported.
    """

    result = {
        "required": [],
        "recommended": [],
        "prohibited": [],
    }

    if not pattern_file.exists():
        return result

    lines = pattern_file.read_text(
        encoding="utf-8"
    ).splitlines()

    in_compliance = False
    current_category = None
    current_item = None

    def flush():
        nonlocal current_item

        if current_category and current_item:
            criterion = " ".join(current_item.split())

            # Ignore generated placeholders
            if criterion.upper() not in {"TODO", "..."}:
                result[current_category].append(criterion)

        current_item = None

    for line in lines:

        if SECTION_RE.match(line):
            flush()
            in_compliance = True
            current_category = None
            continue

        if not in_compliance:
            continue

        # Another level-2 section ends Compliance Criteria
        if line.startswith("## ") and not SECTION_RE.match(line):
            flush()
            break

        subsection = SUBSECTION_RE.match(line)

        if subsection:
            flush()
            current_category = subsection.group(1).lower()
            continue

        if not current_category:
            continue

        checkbox = CHECKBOX_RE.match(line)

        if checkbox:
            flush()
            current_item = checkbox.group(1)
            continue

        # Continuation of a wrapped checkbox line
        if current_item and line.strip() and not line.lstrip().startswith("#"):
            current_item += " " + line.strip()

    flush()

    return result


# =====================================================================
# APPLICABILITY ENGINE
# =====================================================================

def find_matching_patterns(
    all_patterns: list[dict],
    fragments: list[str],
) -> set[str]:

    matches = set()

    for fragment in fragments:
        fragment = fragment.lower()

        for pattern in all_patterns:
            pid = pattern["id"].lower()
            path = pattern["path"].lower()

            if fragment in pid or fragment in path:
                matches.add(pattern["id"])

    return matches


def intake_assessment(
    patterns: list[dict],
) -> tuple[set[str], list[dict], str]:

    candidate_ids: set[str] = set()
    answers = []
    intake_risk = "GREEN"

    risk_rank = {
        "GREEN": 1,
        "AMBER": 2,
        "RED": 3,
    }

    heading("DESIGN CHARACTERISTICS")

    print(
        "\nAnswer the following questions about the proposed design.\n"
        "These answers identify potentially applicable architecture patterns.\n"
    )

    for item in INTAKE_QUESTIONS:

        answer = ask_yes_no(item["question"])

        result = {
            "id": item["id"],
            "question": item["question"],
            "answer": answer,
        }

        answers.append(result)

        if answer:

            candidate_ids.update(
                find_matching_patterns(
                    patterns,
                    item.get("patterns", []),
                )
            )

            risk = item.get("risk")

            if risk and risk_rank[risk] > risk_rank[intake_risk]:
                intake_risk = risk

    return candidate_ids, answers, intake_risk


# =====================================================================
# MANUAL PATTERN SELECTION
# =====================================================================

def manual_pattern_selection(
    patterns: list[dict],
    candidate_ids: set[str],
    phase_limit: int,
) -> set[str]:

    heading("APPLICABLE PATTERNS")

    candidates = [
        p for p in patterns
        if p["id"] in candidate_ids
        and (phase_limit == 0 or p["phase"] <= phase_limit)
    ]

    if candidates:
        print("\nPatterns inferred from the design intake:\n")

        for p in sorted(
            candidates,
            key=lambda x: (
                x["domain"],
                x["category"],
                x["title"],
            ),
        ):
            print(
                f"  [{p['assurance-impact']:5}] "
                f"P{p['phase']}  "
                f"{p['id']}"
            )
    else:
        print(
            "\nNo patterns were automatically inferred from the "
            "intake questions."
        )

    print(
        "\nYou can now confirm the automatically selected patterns."
    )

    confirmed = set()

    for p in candidates:

        if ask_yes_no(
            f"Is '{p['title']}' applicable to this design?",
            default=True,
        ):
            confirmed.add(p["id"])

    if ask_yes_no(
        "\nWould you like to manually add additional patterns?",
        default=False,
    ):
        selectable = [
            p for p in patterns
            if p["id"] not in confirmed
            and (phase_limit == 0 or p["phase"] <= phase_limit)
        ]

        while True:

            print("\nAvailable additional patterns:\n")

            for index, p in enumerate(selectable, start=1):
                print(
                    f"{index:3}. "
                    f"[{p['assurance-impact']:5}] "
                    f"P{p['phase']} "
                    f"{p['id']}"
                )

            value = input(
                "\nEnter pattern number to add "
                "(or press Enter when finished): "
            ).strip()

            if not value:
                break

            if not value.isdigit():
                print("Enter a numeric pattern number.")
                continue

            index = int(value)

            if index < 1 or index > len(selectable):
                print("Invalid pattern number.")
                continue

            selected = selectable[index - 1]
            confirmed.add(selected["id"])

            print(f"Added: {selected['title']}")

    return confirmed


# =====================================================================
# PATTERN ASSESSMENT
# =====================================================================

def evaluate_pattern(
    root: Path,
    pattern: dict,
) -> PatternAssessment:

    heading(f"PATTERN: {pattern['title']}")

    print(f"ID:             {pattern['id']}")
    print(f"Phase:          {pattern['phase']}")
    print(f"Catalog impact: {pattern['assurance-impact']}")
    print(f"File:           {pattern['path']}")

    path = root / pattern["path"]

    criteria = read_compliance_criteria(path)

    total_criteria = sum(
        len(values)
        for values in criteria.values()
    )

    assessment = PatternAssessment(
        pattern_id=pattern["id"],
        title=pattern["title"],
        path=pattern["path"],
        phase=pattern["phase"],
        catalog_assurance=pattern["assurance-impact"],
    )

    if total_criteria == 0:

        print(
            "\nWARNING: No authored Compliance Criteria were found "
            "for this pattern."
        )

        print(
            "This pattern will be recorded as applicable but will "
            "not affect the numerical conformance score."
        )

        return assessment

    weighted_possible = 0
    weighted_earned = 0

    for category in [
        "required",
        "recommended",
        "prohibited",
    ]:

        items = criteria[category]

        if not items:
            continue

        print()
        print("-" * 78)
        print(category.upper())
        print("-" * 78)

        for number, criterion in enumerate(items, start=1):

            prohibited = category == "prohibited"

            if prohibited:
                question = (
                    f"{number}. Prohibition:\n"
                    f"   {criterion}\n\n"
                    f"Does the proposed design violate this prohibition?"
                )
            else:
                question = (
                    f"{number}. {criterion}\n\n"
                    f"Does the proposed design conform to this criterion?"
                )

            answer, compliant, note = ask_control(
                question,
                prohibited=prohibited,
            )

            weight = WEIGHTS[category]

            assessment.criteria.append(
                CriterionResult(
                    category=category,
                    criterion=criterion,
                    answer=answer,
                    compliant=compliant,
                    weight=weight,
                    note=note,
                )
            )

            # N/A does not count against possible score
            if compliant is None:
                continue

            weighted_possible += weight

            if compliant:
                weighted_earned += weight

            elif category == "required":
                assessment.required_failures += 1

            elif category == "prohibited":
                assessment.prohibited_violations += 1

    if weighted_possible > 0:
        assessment.score = round(
            weighted_earned / weighted_possible * 100,
            1,
        )

    return assessment


# =====================================================================
# RESULT CALCULATION
# =====================================================================

def assurance_rank(level: str) -> int:
    return {
        "GREEN": 1,
        "AMBER": 2,
        "RED": 3,
    }.get(level.upper(), 1)


def maximum_assurance(*levels: str) -> str:
    return max(
        levels,
        key=assurance_rank,
    )


def calculate_result(
    assessments: list[PatternAssessment],
    intake_risk: str,
) -> dict:

    weighted_possible = 0
    weighted_earned = 0

    required_failures = 0
    prohibited_violations = 0
    unknown_controls = 0

    pattern_scores = []

    highest_catalog_assurance = "GREEN"

    for assessment in assessments:

        highest_catalog_assurance = maximum_assurance(
            highest_catalog_assurance,
            assessment.catalog_assurance,
        )

        required_failures += assessment.required_failures
        prohibited_violations += assessment.prohibited_violations

        if assessment.score is not None:
            pattern_scores.append(
                {
                    "pattern": assessment.pattern_id,
                    "score": assessment.score,
                }
            )

        for criterion in assessment.criteria:

            if criterion.compliant is None:
                continue

            weighted_possible += criterion.weight

            if criterion.compliant:
                weighted_earned += criterion.weight

            if criterion.answer == "UNKNOWN":
                unknown_controls += 1

    if weighted_possible:
        score = round(
            weighted_earned / weighted_possible * 100,
            1,
        )
    else:
        score = None

    if score is None:
        score_level = "AMBER"

    elif score >= SCORE_GREEN:
        score_level = "GREEN"

    elif score >= SCORE_AMBER:
        score_level = "AMBER"

    else:
        score_level = "RED"

    # Mandatory control violations cannot result in Green.
    if required_failures > 0:
        score_level = maximum_assurance(
            score_level,
            "AMBER",
        )

    # Violating a prohibited architecture guardrail is treated
    # more seriously.
    if prohibited_violations > 0:
        score_level = maximum_assurance(
            score_level,
            "RED",
        )

    final_level = maximum_assurance(
        score_level,
        intake_risk,
        highest_catalog_assurance,
    )

    return {
        "conformance_score": score,
        "score_based_level": score_level,
        "intake_risk": intake_risk,
        "highest_pattern_assurance": highest_catalog_assurance,
        "recommended_assurance_path": final_level,
        "required_failures": required_failures,
        "prohibited_violations": prohibited_violations,
        "unknown_controls": unknown_controls,
        "pattern_scores": pattern_scores,
    }


# =====================================================================
# REPORTING
# =====================================================================

def write_reports(
    design: dict,
    intake_answers: list[dict],
    assessments: list[PatternAssessment],
    result: dict,
):

    timestamp = datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )

    json_path = Path(
        f"architecture-assessment-{timestamp}.json"
    )

    markdown_path = Path(
        f"architecture-assessment-{timestamp}.md"
    )

    json_data = {
        "assessment_timestamp": datetime.now().isoformat(),
        "design": design,
        "intake": intake_answers,
        "patterns": [
            asdict(a)
            for a in assessments
        ],
        "result": result,
    }

    json_path.write_text(
        json.dumps(
            json_data,
            indent=2,
        ),
        encoding="utf-8",
    )

    md = []

    md.append("# Architecture Conformance Assessment")
    md.append("")

    md.append("## Design")
    md.append("")
    md.append(f"- **Name:** {design['name']}")
    md.append(f"- **Team:** {design['team']}")
    md.append(f"- **Owner:** {design['owner']}")
    md.append(f"- **Description:** {design['description']}")
    md.append("")

    md.append("## Result")
    md.append("")

    score = result["conformance_score"]

    if score is None:
        md.append("- **Conformance Score:** Not enough authored criteria")
    else:
        md.append(f"- **Conformance Score:** {score}%")

    md.append(
        "- **Recommended Architecture Assurance Path:** "
        f"**{result['recommended_assurance_path']}**"
    )

    md.append(
        f"- **Required Control Failures:** "
        f"{result['required_failures']}"
    )

    md.append(
        f"- **Prohibited Control Violations:** "
        f"{result['prohibited_violations']}"
    )

    md.append(
        f"- **Unknown Controls:** "
        f"{result['unknown_controls']}"
    )

    md.append("")
    md.append("## Pattern Assessment")
    md.append("")

    for assessment in assessments:

        md.append(f"### {assessment.title}")
        md.append("")
        md.append(f"- Pattern ID: `{assessment.pattern_id}`")
        md.append(
            f"- Catalog Assurance: "
            f"{assessment.catalog_assurance}"
        )

        if assessment.score is None:
            md.append("- Score: Not scored")
        else:
            md.append(f"- Score: {assessment.score}%")

        md.append("")

        if assessment.criteria:

            md.append(
                "| Type | Criterion | Result | Note |"
            )
            md.append(
                "|---|---|---|---|"
            )

            for c in assessment.criteria:

                criterion = c.criterion.replace("|", "\\|")
                note = c.note.replace("|", "\\|")

                md.append(
                    f"| {c.category.title()} "
                    f"| {criterion} "
                    f"| {c.answer} "
                    f"| {note} |"
                )

            md.append("")

        else:
            md.append(
                "_No authored Compliance Criteria available._"
            )
            md.append("")

    markdown_path.write_text(
        "\n".join(md),
        encoding="utf-8",
    )

    return json_path, markdown_path


# =====================================================================
# MAIN
# =====================================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Interactive architecture conformance assessment "
            "against the Enterprise Architecture Pattern Catalog."
        )
    )

    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_CATALOG,
        help="Path to architecture-patterns repository",
    )

    parser.add_argument(
        "--phase",
        type=int,
        choices=[0, 1, 2, 3],
        default=1,
        help=(
            "Maximum delivery phase to evaluate. "
            "Default is Phase 1. Use 0 for all phases."
        ),
    )

    args = parser.parse_args()

    try:
        catalog = load_catalog(args.catalog)

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    patterns = [
        normalize_pattern(p)
        for p in catalog["patterns"]
    ]

    if args.phase:
        patterns = [
            p for p in patterns
            if p["phase"] <= args.phase
        ]

    heading("FEDERATED ARCHITECTURE ASSURANCE")

    print(
        "\nThis assessment will:\n"
        "  1. Capture basic design information\n"
        "  2. Identify potentially applicable architecture patterns\n"
        "  3. Evaluate authored Compliance Criteria\n"
        "  4. Calculate a conformance score\n"
        "  5. Recommend a Green / Amber / Red assurance path\n"
    )

    # ---------------------------------------------------------
    # Design metadata
    # ---------------------------------------------------------

    heading("DESIGN INFORMATION")

    design = {
        "name": ask_text(
            "Solution / design name",
            required=True,
        ),
        "team": ask_text(
            "Delivery team",
            required=True,
        ),
        "owner": ask_text(
            "Solution owner",
        ),
        "description": ask_text(
            "Short design description",
            required=True,
        ),
    }

    # ---------------------------------------------------------
    # Intake
    # ---------------------------------------------------------

    candidate_ids, intake_answers, intake_risk = (
        intake_assessment(patterns)
    )

    # ---------------------------------------------------------
    # Confirm patterns
    # ---------------------------------------------------------

    selected_ids = manual_pattern_selection(
        patterns,
        candidate_ids,
        args.phase,
    )

    selected_patterns = [
        p for p in patterns
        if p["id"] in selected_ids
    ]

    # ---------------------------------------------------------
    # Evaluate patterns
    # ---------------------------------------------------------

    assessments = []

    for pattern in sorted(
        selected_patterns,
        key=lambda x: (
            x["domain"],
            x["category"],
            x["title"],
        ),
    ):
        assessments.append(
            evaluate_pattern(
                args.catalog,
                pattern,
            )
        )

    # ---------------------------------------------------------
    # Calculate final result
    # ---------------------------------------------------------

    result = calculate_result(
        assessments,
        intake_risk,
    )

    # ---------------------------------------------------------
    # Display result
    # ---------------------------------------------------------

    heading("ARCHITECTURE CONFORMANCE RESULT")

    score = result["conformance_score"]

    if score is None:
        print(
            "\nConformance Score : NOT AVAILABLE"
        )
        print(
            "Reason            : No authored compliance criteria "
            "were available for the applicable patterns."
        )

    else:
        print(
            f"\nConformance Score : {score}%"
        )

    print(
        f"Assurance Path    : "
        f"{result['recommended_assurance_path']}"
    )

    print(
        f"Required failures : "
        f"{result['required_failures']}"
    )

    print(
        f"Prohibited issues : "
        f"{result['prohibited_violations']}"
    )

    print(
        f"Unknown controls  : "
        f"{result['unknown_controls']}"
    )

    print()

    final_level = result[
        "recommended_assurance_path"
    ]

    if final_level == "GREEN":

        print(
            "Recommendation:"
        )
        print(
            "Design is eligible for self-attestation under "
            "the federated Architecture Assurance process."
        )

    elif final_level == "AMBER":

        print(
            "Recommendation:"
        )
        print(
            "Targeted Architecture review is recommended. "
            "Review identified exceptions, unknown controls, "
            "or moderate-risk architecture decisions."
        )

    else:

        print(
            "Recommendation:"
        )
        print(
            "Formal Architecture review is recommended before "
            "the design proceeds."
        )

    # ---------------------------------------------------------
    # Reports
    # ---------------------------------------------------------

    json_path, md_path = write_reports(
        design,
        intake_answers,
        assessments,
        result,
    )

    print()
    print(f"JSON report     : {json_path}")
    print(f"Markdown report : {md_path}")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
