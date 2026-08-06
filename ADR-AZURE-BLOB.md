# ADR-006: Azure Blob Storage as a Permitted Exception
 
| Field | Value |
|---|---|
| **Status** | Proposed |
| **Date** | 2026-08-05 |
| **Deciders** | *[Architecture group / tech leads]* |
| **Consulted** | *[Platform, Security, Data, Finance]* |
| **Informed** | *[Engineering org]* |
| **Exception to** | ADR-005: AWS S3 as the Standard for Object and Document Storage |
 
> **This ADR does not weaken ADR-005.** It defines the narrow, evidenced circumstances under which Azure Blob Storage may be used instead, and the conditions attached to that use. Outside these circumstances the standard applies without exception.
 
---
 
## 1. Context
 
ADR-005 establishes S3 as the standard for object and document storage. A small number of workloads have characteristics that make compliance either impossible or clearly value-destroying:
 
- Workloads whose compute already runs in Azure, where storing objects in S3 imposes cross-cloud egress charges and network latency on every operation, for no offsetting benefit.
- Workloads that consume Azure-native services taking blob storage as their direct input or output, where an intermediate copy step adds cost, latency, and a failure mode with no architectural gain.
- Contractual or regulatory obligations requiring data to be held in a specific provider, region, or sovereign cloud that AWS cannot satisfy for that workload.
- Business units or acquired entities operating substantially on Azure, where forced migration would cost more than the divergence it removes.
Refusing these cases would push teams toward worse designs — copying data between providers, or building bespoke synchronisation — while nominally complying with the standard. Refusing to name a legitimate exception does not eliminate it; it drives it underground.
 
## 2. Decision
 
**Azure Blob Storage may be used for object and document storage where at least one qualifying condition below is met and evidenced in the solution design, and where all attached conditions are satisfied.**
 
### 2.1 Qualifying conditions
 
At least one must apply, and the solution design must evidence it — not merely assert it:
 
| # | Condition | Required evidence |
|---|---|---|
| Q1 | **Compute co-location** — the consuming workload runs substantially in Azure, and cross-cloud transfer volume makes S3 materially more expensive or slower | Estimated transfer volume, egress cost comparison, latency requirement |
| Q2 | **Azure-native service dependency** — a required Azure service consumes or produces blob storage directly, with no reasonable alternative | The service, its storage integration, and why an intermediate copy is not acceptable |
| Q3 | **Contractual or regulatory requirement** — a customer contract, regulator, or data-residency obligation requires Azure or a region AWS cannot serve | The specific clause or regulatory reference |
| Q4 | **Inherited estate** — an acquired or existing business unit operates on Azure, and migration is not economically justified within *[the current planning horizon]* | Migration cost estimate and a documented target state |
 
### 2.2 Explicitly not qualifying
 
The following are **not** grounds for this exception, and a design resting on them is returned at triage:
 
- Team preference, familiarity, or existing Azure skills
- Speculative multi-cloud portability or provider-hedging ambitions with no current requirement
- Availability of provider credits or promotional pricing
- A belief that Azure Blob is technically superior for the workload — absent a qualifying condition, the standard's organisational benefits outweigh per-workload technical preference
- Convenience of an existing Azure subscription
### 2.3 Attached conditions
 
Where the exception is granted, the workload must achieve **posture equivalent to the ADR-005 baseline**. The exception is from the *technology*, not from the controls:
 
1. Encryption at rest with a customer-managed key held in *[Azure Key Vault]*, with key access scoped to the consuming identities.
2. TLS enforced; insecure transfer disabled at the storage account.
3. **Public blob access disabled at the storage account level**, not merely per container.
4. Access via *[Entra ID]* workload identity. **Shared account keys and long-lived SAS tokens are prohibited**; where SAS is required, it is user-delegation SAS with short expiry.
5. Private endpoints for access from within the network; no public network access except where explicitly justified.
6. Soft delete and blob versioning enabled.
7. Immutability policy in locked mode for object classes subject to regulatory retention, matching the retention defined in *[the data classification policy]*.
8. **A lifecycle management policy is mandatory**, declaring tier transitions and expiry, on the same terms as ADR-005.
9. Geo-redundant replication per data classification, aligned to documented RPO.
10. Diagnostic logging to *[the central log platform]*, and identity events forwarded to the same SIEM as AWS activity, so the two estates are observable together rather than separately.
11. Mandatory tagging equivalent to the ADR-005 standard: owner, classification, cost centre, environment, retention class.
12. Provisioned through infrastructure-as-code only.
### 2.4 Registration
 
Every invocation is recorded in the exception register with the qualifying condition claimed, the evidence, a named owner, and a review date not more than *[12 months]* out. An exception that is not re-evidenced at review lapses, and the workload is scheduled for migration.
 
## 3. Alternatives Considered
 
| Option | Why not chosen |
|---|---|
| **Apply ADR-005 with no exceptions** | Maximally simple to govern. Rejected because it forces genuinely disadvantaged designs — cross-cloud copies and bespoke synchronisation — that are worse on every dimension including the security posture the standard exists to protect. |
| **Replicate Azure-resident data to S3 for a single control plane** | Preserves one storage standard. Rejected because it doubles storage cost, introduces synchronisation lag and a new failure mode, and does not remove the Azure copy that necessitated it. |
| **Cloud-agnostic abstraction over both providers** | Would permit either provider transparently. Rejected on the same grounds as in ADR-005: it constrains every consumer to the lowest common denominator, forfeiting the provider-specific controls both this ADR and ADR-005 require. |
| **Case-by-case waivers with no exception ADR** | More flexible. Rejected because undocumented per-project waivers accumulate without visibility, apply inconsistent conditions, and are the mechanism by which standards are repealed without anyone deciding to repeal them. |
 
## 4. Consequences
 
### Positive
 
- Genuinely disadvantaged workloads get an appropriate solution without either violating the standard or building a worse design to comply with it.
- The circumstances are named in advance, so the assessment is against published criteria rather than negotiation, argument quality, or seniority.
- Exceptions become visible and countable, which makes the standard's fit measurable.
- Limited provider concentration relief for the specific data classes where a contractual obligation demands it.
### Negative
 
- **A second operating model.** Two sets of runbooks, controls, IAM models, cost models, and on-call knowledge. This cost is real, recurring, and consistently underestimated at the point of granting the exception.
- **Duplicated assurance.** Every audit, control test, and security review must now cover two platforms.
- **Identity and network complexity** where a workload spans both estates.
- **Skills dilution.** Engineers maintain competence in two storage platforms rather than depth in one.
- **Precedent pressure.** Each granted exception makes the next request easier to justify by analogy. The register and the review trigger in §6 exist specifically to counter this.
- **Migration debt.** Q4 exceptions in particular defer rather than resolve, and the deferral needs to remain visible.
## 5. Compliance and Enforcement
 
- Azure storage accounts outside the registered exception list are flagged by automated inventory reconciliation.
- Policy-as-code enforces the §2.3 conditions at deployment; non-conformant accounts fail the pipeline.
- Detection and alerting on shared-key access and on account-level public access being enabled.
- Exception register reviewed *[quarterly]* by Enterprise Architecture; lapsed entries escalate.
## 6. Review Triggers
 
Revisit this decision if:
 
- Registered exceptions exceed *[N]* or *[10%]* of storage-consuming solutions — the boundary between standard and exception is in the wrong place, and ADR-005 should be reassessed rather than this ADR extended.
- The same qualifying condition recurs across many workloads, indicating a structural rather than exceptional circumstance.
- The cost of maintaining dual assurance exceeds the cost the exceptions avoid.
- The organisation's primary cloud platform strategy changes, which would invert the relationship between this ADR and ADR-005.
