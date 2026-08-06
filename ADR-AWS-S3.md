# ADR-005: AWS S3 as the Standard for Object and Document Storage
 
| Field | Value |
|---|---|
| **Status** | Proposed |
| **Date** | 2026-08-05 |
| **Deciders** | *[Architecture group / tech leads]* |
| **Consulted** | *[Platform, Security, Data, Finance, Infrastructure]* |
| **Informed** | *[Engineering org]* |
| **Exceptions** | ADR-006 (Azure Blob Storage), ADR-007 (PowerScale) |
| **Supersedes** | — |
 
> **Scope.** Unstructured object and document storage: uploaded documents, images, media, generated reports, exports, backups, data-lake objects, and static assets.
> **Out of scope:** structured data belonging in a database; workloads requiring POSIX file semantics (see ADR-007); ephemeral scratch space local to compute; source code (version control); secrets (secret management).
 
---
 
## 1. Context
 
Object and document storage is a requirement in *[most / a majority of]* solution designs the development teams produce. Today each team selects a storage technology independently, and the results diverge in ways that are expensive but individually invisible:
 
- **Proliferation of operating models.** *[N]* distinct storage technologies are in production, each with its own access control model, encryption configuration, backup approach, and failure behaviour. Operational knowledge does not transfer between them.
- **Inconsistent security posture.** Encryption, public-access prevention, access logging, and retention are configured per team, to varying standards. There is no way to answer "is any of our document storage publicly readable?" without inspecting each system separately.
- **Audit and retention gaps.** Regulatory retention for *[regulated document classes]* is implemented differently in each system, and in some cases not at all. Demonstrating compliance requires per-system evidence gathering.
- **Cost is invisible until it is large.** Without a common tagging and lifecycle standard, storage grows monotonically. Nothing expires because nothing was ever configured to.
- **Duplicated engineering.** Each team independently solves upload handling, large-file transfer, access-controlled retrieval, and lifecycle management.
- **Review overhead.** Every solution design re-litigates a decision that has no team-specific answer, consuming architecture review capacity on a settled question.
The organisation's primary cloud platform is AWS, where *[the majority of]* compute already runs.
 
## 2. Decision
 
**AWS S3 is the default and standard technology for all object and document storage. Any solution requiring such storage will use S3 unless a published exception ADR applies and its qualifying conditions are demonstrably met.**
 
The following baseline is mandatory for every bucket. These are not recommendations — they are the terms on which the standard is granted, and a bucket that does not meet them is non-conformant regardless of who created it.
 
### Security
 
1. **Encryption at rest** using SSE-KMS with a customer-managed key. Key policy grants access only to the roles that need it, giving a second, independent control point over the data.
2. **TLS in transit**, enforced by bucket policy denying non-TLS requests.
3. **Block Public Access enabled at the account level** and not overridable per bucket. Public distribution, where genuinely required, is served through *[CDN with origin access control]* rather than by making objects public.
4. **Access via IAM roles only.** No long-lived access keys. Workloads assume roles through *[instance profiles / IRSA / workload identity federation]*.
5. **Client access via presigned URLs** with short expiry, rather than proxying object bytes through application services. Applications should not become file servers.
6. **Least-privilege bucket and key policies**, scoped to prefixes where a bucket serves multiple purposes.
### Data management
 
7. **Versioning enabled** on every bucket, to make accidental deletion and overwrite recoverable.
8. **A lifecycle policy is mandatory.** Every bucket declares storage-class transitions and an expiration or explicit justification for indefinite retention. **A bucket with no lifecycle policy is a defect**, because absent a decision the default is to keep everything forever and pay for it forever.
9. **Object Lock in compliance mode** for object classes subject to regulatory retention, configured to *[the retention period defined in the data classification policy]*.
10. **Replication** per data classification: *[cross-region replication for tier-1 data; same-region or none below that]*, aligned to documented RPO.
### Operations
 
11. **CloudTrail data events enabled** for buckets holding *[regulated or sensitive]* data; server access logging to a central log account.
12. **Mandatory tagging**: owner, data classification, cost centre, environment, retention class.
13. **Naming convention**: `*[org]-[env]-[domain]-[purpose]*`, globally unique and predictable enough to reason about from the name alone.
14. **Provisioned through infrastructure-as-code only.** No console-created buckets in any environment above development.
### Usage constraints
 
15. **S3 is not a database.** No workflow depends on listing a bucket to find data — listing at scale is slow and expensive. Object keys are derived from an authoritative record in a database, or an index is maintained separately.
16. **Key design supports access patterns**: prefix by tenant, date, or domain to permit prefix-scoped IAM policies and efficient enumeration.
17. **Multipart upload** for objects above *[100 MB]*, with abort-incomplete-upload lifecycle rules — orphaned multipart parts are a common and entirely invisible source of cost.
## 3. Alternatives Considered
 
| Option | Why not chosen |
|---|---|
| **Per-team choice (status quo)** | Optimises for individual team autonomy at the cost of every organisational property in §1. The costs are diffuse and the benefits are local, which is precisely why this pattern persists without anyone choosing it. |
| **Self-managed object storage** (e.g. an S3-compatible platform on our own infrastructure) | Avoids provider lock-in and can be cheaper at very large, stable volumes. Rejected because it makes us responsible for durability, capacity, and upgrades of a system whose managed equivalent is a solved problem, and the operational burden is permanent rather than one-off. |
| **Documents in database BLOB columns** | Transactional consistency between metadata and content is a genuine advantage. Rejected as a general pattern because it inflates database size, slows backup and restore, and consumes the most expensive storage tier for the least demanding data. Acceptable only for small objects with strict transactional coupling. |
| **Network file share for everything** | Familiar and simple for legacy applications. Rejected as the default because it does not scale elastically, requires capacity forecasting, and lacks the lifecycle and retention primitives above. **Retained as an exception where file semantics are genuinely required — see ADR-007.** |
| **Cloud-agnostic storage abstraction layer** | Preserves theoretical portability. Rejected because it constrains every consumer to the lowest common denominator across providers, forfeiting the specific features this ADR mandates, in exchange for a portability option that is rarely exercised. Abstraction is paid for continuously and redeemed almost never. |
| **Multi-cloud by default** | Doubles the operating model, the security surface, and the required skills, to hedge a risk that is better managed contractually. Specific, justified exceptions are handled by ADR-006. |
 
## 4. Consequences
 
### Positive
 
- One operating model: one set of runbooks, one security baseline, one cost model, one skill set to hire for and maintain.
- The security baseline is designed once and enforced automatically, rather than reasoned about per project.
- Retention and audit posture becomes answerable organisation-wide from a single control plane.
- Storage cost becomes visible and attributable through consistent tagging, and controllable through mandatory lifecycle policy.
- Solution designs stop re-deciding this, freeing architecture review capacity for decisions that are actually project-specific.
- Data co-locates with the compute that already runs in AWS, avoiding cross-provider egress and latency.
### Negative
 
- **Provider concentration.** Commercial leverage decreases and provider-specific dependency increases. Mitigated commercially rather than architecturally; the exception ADRs are not a hedging strategy and should not be treated as one.
- **Egress cost for consumers outside AWS.** On-premise or other-cloud consumers pay per-gigabyte egress. Where this dominates the economics, an exception may be warranted.
- **Request costs at high operation volume.** Workloads performing very large numbers of small operations can find request charges exceeding storage charges. Access-pattern design matters more than object size.
- **No POSIX semantics.** No atomic rename, no directory operations, no partial in-place update, no file locking. Applications assuming a filesystem cannot use S3 unmodified — the most common source of exception requests.
- **Latency for on-premise consumers** is higher than local storage and variable in a way local storage is not.
- **The baseline adds friction** to creating a bucket. Some teams will experience this as bureaucracy, particularly for low-value internal data.
### Neutral
 
- Exceptions are legitimate and expected, and are governed by ADR-006 and ADR-007 rather than by informal negotiation.
## 5. Exception Process
 
An exception is not a waiver granted per project. It is a **claim that a published exception ADR's qualifying conditions are met**, and it is assessed on that basis.
 
1. The solution design identifies which exception ADR it invokes and evidences each qualifying condition.
2. The domain architect verifies the conditions. **Preference, familiarity, prior experience, and speculative future portability are explicitly not qualifying conditions** under any exception ADR.
3. The exception is recorded in the exception register with a named owner and a review date.
4. A requirement not covered by an existing exception ADR is not granted ad hoc — it is a proposal for a **new** exception ADR, reviewed at enterprise tier. This is deliberately a higher bar than a project-level waiver, because a per-project waiver path is how a standard is quietly repealed.
Recurring exception requests are a signal about the standard, not about the requesting teams. Where the same condition recurs across *[three or more]* solutions, this ADR is reassessed rather than the exceptions being renewed.
 
## 6. Compliance and Enforcement
 
- Service control policies prevent disabling account-level Block Public Access and prevent bucket creation outside approved regions.
- Infrastructure-as-code policy checks fail the pipeline on: missing encryption configuration, missing lifecycle policy, missing required tags, or a bucket policy permitting anonymous access.
- Automated detection of console-created buckets, reported to the owning team.
- Periodic audit of buckets against the baseline, with drift reported to the owning team and to Enterprise Architecture.
- Solution designs proposing non-S3 storage without invoking a published exception ADR are returned at triage.
## 7. Review Triggers
 
Revisit this decision if:
 
- Exception requests exceed *[20%]* of solution designs requiring storage — the standard no longer fits the workload profile.
- Egress or request costs materially exceed forecast, changing the economics against on-premise or alternative storage.
- The organisation's primary cloud platform changes, or a significant business unit is acquired with a different platform.
- A contractual or regulatory obligation makes single-provider concentration untenable for a class of data.
