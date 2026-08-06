# ADR-007: PowerScale Storage as a Permitted Exception
 
| Field | Value |
|---|---|
| **Status** | Proposed |
| **Date** | 2026-08-05 |
| **Deciders** | *[Architecture group / tech leads]* |
| **Consulted** | *[Infrastructure, Security, Data, Finance, Capacity Management]* |
| **Informed** | *[Engineering org]* |
| **Exception to** | ADR-005: AWS S3 as the Standard for Object and Document Storage |
 
> **This ADR does not weaken ADR-005.** It defines the narrow, evidenced circumstances under which on-premise PowerScale storage may be used instead, and the conditions attached to that use.
 
---
 
## 1. Context
 
ADR-005 establishes S3 as the standard. A distinct class of workload cannot use object storage at all — not for cost or preference reasons, but because the access semantics are wrong:
 
- **Applications that require file semantics.** Commercial or legacy applications that expect a mounted filesystem — POSIX paths, atomic rename, in-place partial writes, file locking, directory operations. Object storage does not provide these, and the application cannot be modified.
- **On-premise compute adjacency.** Processing that runs on-premise against very large datasets, where moving the data to cloud storage imposes transfer cost and latency exceeding any benefit.
- **Data custody obligations.** Regulatory or contractual requirements for physical custody, air-gapped operation, or a jurisdiction cloud regions cannot serve.
- **Economics at sustained very large volume.** Datasets in the *[hundreds of terabytes to petabytes]* with high read throughput and long retention, where owned capacity is materially cheaper over the asset life than metered cloud storage plus egress.
The organisation operates PowerScale as its scale-out file platform, with existing capacity, operational capability, and support arrangements. These conditions are structural rather than transitional — unlike the Azure exception, most will not resolve with time.
 
## 2. Decision
 
**PowerScale storage may be used for document and file storage where at least one qualifying condition below is met and evidenced in the solution design, and where all attached conditions are satisfied.**
 
### 2.1 Qualifying conditions
 
At least one must apply, with evidence:
 
| # | Condition | Required evidence |
|---|---|---|
| Q1 | **File semantics required** — the application requires POSIX, NFS, or SMB access and cannot be modified to use object storage | The specific semantics required, and why modification is not viable (vendor product, source unavailable, cost) |
| Q2 | **On-premise compute adjacency** — processing runs on-premise against the dataset, and transfer volume or latency makes cloud storage impractical | Dataset size, access pattern, throughput requirement, transfer cost estimate |
| Q3 | **Data custody or sovereignty** — regulation, contract, or security classification requires on-premise custody or air-gapped operation | The specific obligation |
| Q4 | **Sustained large-volume economics** — total cost of ownership over *[5 years]* is materially lower on owned capacity | TCO comparison including capacity, refresh, power, floor space, and operational staffing — not media cost alone |
 
### 2.2 Explicitly not qualifying
 
- Familiarity with file shares, or an application that *could* be adapted but has not been prioritised for adaptation
- Existing spare capacity on the platform — available capacity is not an architectural justification, though it is a frequent one
- Avoidance of cloud onboarding or procurement effort
- A general preference for on-premise infrastructure
- Small datasets, however convenient a share may be
### 2.3 Attached conditions
 
1. **Prefer the S3-compatible protocol where the application supports object semantics.** Where PowerScale is chosen for adjacency or economics (Q2, Q4) rather than file semantics (Q1), the S3 protocol should be used in preference to NFS or SMB. This keeps the application portable to ADR-005 storage should the qualifying condition lapse — and it frequently does.
2. **WORM retention** via *[SmartLock]* for object classes subject to regulatory retention, matching the periods in *[the data classification policy]*.
3. **Snapshots** on a defined schedule with a defined retention, sized into the capacity plan.
4. **Replication to a secondary site** via *[SyncIQ]* for tier-1 data, aligned to documented RPO and RTO. **Replication is not backup** — an independent backup with a separate failure domain is required, and this distinction is the one most often lost when file storage is treated as inherently durable.
5. **Access zones and directory integration** for authentication; access granted through groups, never to individual accounts.
6. **Quotas** enforced per share. Unquotaed shares consume the cluster and are discovered only when it fills.
7. **Encryption at rest** via *[self-encrypting drives / cluster-level encryption]*; encrypted protocols in transit where supported.
8. **Protocol audit logging** forwarded to *[the central SIEM]*, so on-premise access is observable alongside cloud access rather than in a separate silo.
9. **No direct internet exposure.** Access only from within the network or through *[the approved access path]*.
10. **Capacity forecast** included in the solution design: initial size, growth rate, and the horizon at which additional capacity must be procured. **Unlike cloud storage, capacity here is finite and has a procurement lead time of *[N weeks]*** — a workload that grows faster than forecast becomes an infrastructure emergency rather than a line-item increase.
11. **Lifecycle definition**: tiering policy and deletion or archival criteria, on equivalent terms to ADR-005's lifecycle requirement.
12. Mandatory tagging or share metadata equivalent to ADR-005: owner, classification, cost centre, environment, retention class.
### 2.4 Registration
 
Recorded in the exception register with the qualifying condition, evidence, owner, capacity forecast, and review date not more than *[12 months]* out. Review reconfirms the qualifying condition and reconciles actual against forecast growth.
 
## 3. Alternatives Considered
 
| Option | Why not chosen |
|---|---|
| **Apply ADR-005 with no exceptions** | Rejected as impossible rather than merely undesirable for Q1 workloads: object storage does not provide file semantics, and no configuration makes it do so. |
| **Gateway translating file protocols to S3** | Presents a filesystem over object storage and would preserve a single standard. Rejected as a general answer because the semantics remain approximate — locking, atomic rename, and partial-write behaviour differ under load in ways that surface as data corruption rather than as errors. May be reconsidered per workload where the application's actual requirements are known to be within a gateway's guarantees. |
| **Modify applications to use object storage** | The correct long-term answer where feasible, and preferred wherever the application is ours. Not viable for vendor products or where modification cost exceeds the divergence cost — but this should be reassessed at each exception review rather than treated as settled. |
| **Cloud file services** (managed NFS or SMB in AWS) | Would provide file semantics within the standard cloud platform. **This is the strongest alternative and should be evaluated before invoking this ADR**, particularly for Q1 workloads whose compute could move to cloud. It does not address Q2 adjacency or Q3 custody. |
| **Case-by-case waivers with no exception ADR** | Rejected for the same reason as in ADR-006: invisible, inconsistent, and cumulatively corrosive to the standard. |
 
## 4. Consequences
 
### Positive
 
- Workloads that genuinely cannot use object storage have a supported, governed option rather than an improvised one.
- Existing platform investment, operational capability, and support arrangements are used.
- Low, predictable latency for on-premise compute, with no per-gigabyte transfer charge.
- Physical custody satisfied where obligations require it.
### Negative
 
- **Capacity is finite and must be forecast.** The elasticity assumption that holds for cloud storage does not hold here. Under-forecasting produces an urgent procurement; over-forecasting produces stranded capital.
- **Procurement and refresh lead times** measured in *[weeks to months]*, and a hardware lifecycle requiring planned replacement every *[N years]*.
- **Site dependency.** Availability is bounded by the data centre. Multi-site resilience must be engineered and paid for, rather than assumed.
- **Backup and DR are the organisation's responsibility**, engineered and tested explicitly. Cloud storage durability guarantees do not transfer.
- **A separate operating model** from the S3 standard: different controls, different tooling, different skills, different audit evidence.
- **Portability is limited.** File-semantics workloads are the hardest to migrate later, so Q1 exceptions in particular tend to be permanent. Condition 2.3.1 exists to keep the non-Q1 cases from becoming equally stuck.
- **Cost is less visible.** Capital and shared-platform costs are harder to attribute to a consuming workload than metered cloud charges, which makes it easy for a workload to appear cheaper than it is.
## 5. Compliance and Enforcement
 
- Shares created outside the registered exception list are flagged by automated reconciliation against the register.
- Quota enforcement is verified at provisioning; unquotaed shares are reported.
- Snapshot, replication, and backup configuration verified against the registered classification.
- Capacity utilisation and growth reported *[monthly]* against registered forecasts, with variance escalated before it becomes urgent.
- Exception register reviewed *[quarterly]* by Enterprise Architecture.
## 6. Review Triggers
 
Revisit this decision if:
 
- Registered exceptions exceed *[N]* or a materially increasing share of storage-consuming solutions.
- A cloud file service or protocol gateway matures sufficiently to satisfy Q1 workloads within the standard platform.
- Platform refresh or capacity expansion requires investment whose business case depends on exception volume that is not materialising.
- The TCO position underpinning Q4 changes materially in either direction.
- Vendor applications currently requiring file semantics gain object-storage support.
