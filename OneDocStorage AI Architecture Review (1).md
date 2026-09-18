# Architecture Review — OneDocStorage AI (#608351)

**Reviewer role:** Enterprise Architect
**Scope:** design-tollgate-09-10 artifact set
**Source path:** `S:\IT_Qual\PDP_Projects\Sales\Projects\2025\608351_OneDocStorage_AI\design-tollgate-09-10`

---

## Source document key

Findings below are referenced using these short codes.

| Code | Document | Version / date | Author / owner |
|------|----------|----------------|----------------|
| **[ITP]** | IT Proposal — *OneDocStorage AI Design* #608351 (7 pp., footer "Document3") | Modified 11/12/2025, 03/16/2026, 06/26/2026, 09/10/2026 | NagurBasha & Ashwin Balabadrapatruni |
| **[TD]** | Technical Design — *OneDocStorage AI Design* #608351, **Version 2** (6 pp., footer "combined IBMi and Java doc") | Modified 11/11/2025, 03/16/2026, 06/26/2026, 09/10/2026 | Nagur Basha & Ashwin Balabadrapatruni |
| **[AZ]** | `Penske_PTL_One_Document_Search_OAzure_AI_Architecture.pdf` — *Azure AI Services – One Document Search (Prod)* | **Date Updated: 06/25/2026** | Azure Admin: Geoffrey Hartsfield |
| **[OCP]** | `OneDocStorage AI OCP.pdf` — OCP application view | Date Updated: 09/10/2026 | Developer: Srija Adusumilli |

> **Note on [AZ]:** the Azure infrastructure diagram is dated **06/25/2026**, three months older than the rest of the package. Per the [TD] Document Revision Chart, the **09/10 revision added "Cataloguing implementation & Ingestion (Indexing)"** — so [AZ] almost certainly does not reflect the current design. This alone should be corrected before tollgate.

---

## Summary

The solution *shape* is reasonable and follows a recognised pattern: event-driven ingest → Azure AI Document Intelligence → embeddings → Azure AI Search → AI Foundry agents fronted by Python microservices on OCP ([ITP] §4, §10; [TD] §4).

However, the **design documentation is not yet at tollgate quality**. Several decisions that determine security posture, data ownership and operability are contradictory across the four artifacts, missing entirely, or stated as aspirations rather than designs. Findings below should be resolved or formally risk-accepted before approval.

---

## 1. Blocking inconsistencies across the artifact set

Each of these changes the build; none is cosmetic.

| # | Issue | Source references |
|---|-------|-------------------|
| **1.1** | **Metadata store contradiction.** [ITP] §5 *Catalogued Path Processing* and [ITP] §10 both state metadata (UUID, document path, cataloguing fields) is pushed from Cosmos DB to **MySQL** via the OCP API. [OCP] shows the pod connecting over **JDBC** to **SQL Server**, database `onedocument`, host `GHSQL10`, profile `onedoc-aims-user`, secret `database-sqlserver-onedocumentaims`. Which is the system of record? | [ITP] §5, §10; [OCP] "Database Details" panel |
| **1.2** | **Microservice count disagrees.** [ITP] §4 and §10: *"Developed and deployed **two** microservices (Q&A Agent and Summary Agent) on OCP."* [TD] §4: *"Developed and deployed **three** microservices (Q&A Agent, Inquiry Agent and Summary Agent)."* [TD] §7.2.1 then lists **three programs** but names them differently again: *"1. Azure Function App, 2. Q&A Agent, 3. Summary Agent."* Effort and deployment plans differ accordingly. | [ITP] §4, §10; [TD] §4, §7.2.1 |
| **1.3** | **Sandbox resource named in a production design.** [TD] §7.1.1.3 specifies Cosmos `cosmos-onedoc-ptl-**sbx**-eus2-1`. [OCP] repeats the same **sbx** name under *Database Details → Name*, while its own *System(Host)* field on the same panel reads `cosmos-onedoc-ptl-**prod**-eus2-1.documents.azure.com:443`. The [OCP] panel is internally contradictory. | [TD] §7.1.1.3; [OCP] Cosmos "Database Details" panel |
| **1.4** | **Apigee is unplaced.** [ITP] §7 lists *"APIGEE for secure API exposure and management"* as infrastructure. Apigee appears in neither [OCP] nor [AZ]; [OCP] shows the client calling `https://onedocstorage-ai-ms.apps.penske.com` directly behind Redhat SSO. Is Apigee in the request path, and if so where does token validation occur? | [ITP] §7; [OCP] client/ingress path |
| **1.5** | **Managed identity vs. account key.** [AZ] labels the OCP→Azure and Azure-internal flows *"HTTPS – MANAGED IDENTITY"* (and one *"HTTPS – USER DELEGATION"*). [OCP] instead lists secret `onedocstorage-ai-cosmos-access-key` for Cosmos. Account keys bypass RBAC, are non-attributable in logs, and cannot be rotated without downtime. | [AZ] flow labels; [OCP] Cosmos "Secrets" |
| **1.6** | **Search endpoint naming.** [TD] §5.1 gives the index as `https://srch-onedoc-ptl-prod-eus2-1.search.windows.net`; [OCP] "Azure Search Service" repeats it; [AZ] shows only a generic `*.search.windows.net` private endpoint in subnet `sn-pe-ai-shared-prod-ptl-eus2-1`. Confirm private DNS resolution is documented for the exact FQDN. | [TD] §5.1; [OCP]; [AZ] AI subnet |
| **1.7** | **Document hygiene.** Both Word documents carry the wrong project identity and unremoved template content: [ITP] running header *"[Sales B2B authentication Design] – IT Proposal"* and footer *"Document3"*; [TD] running headers *"Technical Design: Sales B2B authentication"* and footer *"combined IBMi and Java doc"*; [ITP] cover *"PDP VERSION: 1/5/2015 / REVIEWED: 1/8/2025"*; [ITP] TOC first line still reads *"COMPARATIVE ANALYTICS SALES TOOL DESIGN"*. | [ITP] cover, TOC, all page headers/footers; [TD] all page headers/footers |
| **1.8** | **[TD] section numbering is broken.** The [TD] Table of Contents lists *"9.2 PROGRAMS (IBMi)"* and *"9.2.1 Program 1"* nested under **7. COMPONENTS / PROGRAMS**, while the body numbers the same content **7.2** and **7.2.1**. | [TD] TOC vs. §7.2 |

---

## 2. Security and identity — the largest gap

### 2.1 No end-user identity reaches the Azure layer
[OCP] states **Auth Flow: Client Credential**, with Azure AD issuing tokens from `https://login.microsoftonline.com/63a58ffd-…/oauth2/v2.0/token` using `azureadclientsecrets`. Every downstream call to AI Search, Foundry, Cosmos, Service Bus and Blob is therefore made **as the application, not the user**.

Yet [TD] §7.1.1.3 defines the Cosmos `OneDocument` collection as:

```
{ "id": "<generated>", "UserId": "<passed>", "Role": "<passed>", "threadIdQandA": "<passed>" }
```

and the `docs-index` schema carries a single `role` column. If `UserId` and `Role` are *passed in* by the caller rather than derived from a validated token, **entitlement is client-asserted and therefore spoofable**.

*References: [OCP] header panel and Azure AD panel; [TD] §7.1.1.3.*

### 2.2 Document-level authorization is asserted, not designed
[ITP] §7 states *"Cosmos DB to store custom metadata for RBAC enforcement."* That is an outcome, not a mechanism. No section of [TD] — including §7.1.1.4 *Business Rules*, which is left as template instruction text, and §9 *Security and Single Sign-on Integration* — describes how a user's entitlements become a retrieval restriction.

Required: ACLs/group claims stamped onto each chunk at index time, enforced as an Azure AI Search `$filter` derived from the **validated user token**, with fail-closed behaviour for unlabelled documents.

*References: [ITP] §7; [TD] §7.1.1.3, §7.1.1.4, §9.*

### 2.3 Auditability
With app-only identity ([OCP] Auth Flow) and logging described only as *"Standard logging using Python for Openshift Microservices / Azure Function Apps"* ([TD] §13), the platform cannot answer *"which user asked what, about which customer's contract."* Confirm with Legal/Compliance whether that is acceptable for contract data.

*References: [OCP]; [TD] §13.*

### 2.4 The Security Assessment is not a security assessment
[ITP] §6 and its verbatim duplicate [TD] §9 state only that Q&A and Summary API endpoints are Client-Credential enabled, the application is protected by Redhat SSO, a JWT is generated, and *"This will also contain 0 Test detectable security violations."*

Absent from both: threat model; data classification for contract content (PII, commercial terms, counterparty confidentiality); SAST/DAST/penetration-test plan; DLP position; Azure OpenAI abuse-monitoring, data-residency and retention posture. Note [ITP] §11 contains **no line item for security testing** in the 75-day estimate.

*References: [ITP] §6, §11; [TD] §9.*

### 2.5 Secrets management
Secrets are enumerated across [OCP] — `azureadclientsecrets`, `onedocstorage-ai-cosmos-access-key`, `onedocstorage-ai-client-credentials`, `onedocstorage-ai-summary-agent-id`, `onedocstorage-ai-tenant-id`, `onedocstorage-ai-search-credentials`, `database-sqlserver-onedocumentaims` — and Key Vault private endpoints appear in [AZ]. No document states where each secret lives, how OCP secrets and Key Vault are kept in sync, or the rotation process. Recommend workload identity federation or certificate auth in place of client secrets.

*References: [OCP] all detail panels; [AZ] "Key Vault EUS2" private endpoint and "Key Vaults".*

### 2.6 Network posture
[AZ] shows Alkira, NSGs, VNet `vnet-data-shared-prod-ptl-eus2-1` (`10.77.176.0/20`), subnets `sn-pe-shared-prod-ptl-eus2-1` and `sn-pe-ai-shared-prod-ptl-eus2-1`, private endpoints for Cosmos, Data Lake, Key Vault, AI Search, Doc Intelligence and AI Foundry, plus DNS private clusters on TCP/UDP 53. What is **not** stated anywhere is that **public network access is disabled** on those PaaS services. Private endpoints coexisting with an open public endpoint is a common and material gap; please assert it explicitly.

*References: [AZ] DTLZ-PTL-Shared-PROD and PLTF panels; [TD] §10 Integration = "NA".*

---

## 3. AI-specific risks — largely unaddressed

### 3.1 Prompt injection into a tool-calling agent
[ITP] §7 and §10 both state *"Azure Function Apps act as MCP Servers and expose tools to AI Foundry Agents,"* and [AZ] shows an **"MCP Server/Entra Auth"** Function App inside `AZLZ-PTL-Shared-PROD`. Untrusted customer PDFs ([ITP] §10 "Data Ingestion & Processing") are chunked into the index that grounds those agents. This is a direct **injection → tool-execution** path.

Mitigations required and currently absent: least-privilege function identities; no destructive/write tools exposed to agents; input and output content filtering; retrieved document content treated as untrusted data, never as instructions.

*References: [ITP] §7, §10; [AZ] MCP Server/Entra Auth + Function Apps; [TD] §5.1 `ptl-onedocstorage-mcp-processor` repo.*

### 3.2 The MCP server is undocumented
[TD] §5.1 gives only the repository URL (`…/_git/ptl-onedocstorage-mcp-processor`). [TD] §7.1.1 *Component 1* is **"N/A"**, §7.1.1.1 *Interface Design* is **"N/A"**, and §7.1.1.2 *Class/Program Design* contains only empty Interface/Method/Class tables. There is therefore **no tool inventory, no auth model, no data-reach statement and no blast-radius analysis** for the most security-sensitive component in the design.

*References: [TD] §5.1, §7.1, §7.1.1, §7.1.1.1, §7.1.1.2.*

### 3.3 No quality bar for AI output
[ITP] §8 *Testing Approach* reads in full: *"Dev/QA Environment will be created for testing."* Nothing in [ITP] or [TD] defines accuracy targets for the custom Document Intelligence classification/extraction models ([ITP] §7, §10), a labelled evaluation set, groundedness/hallucination measurement, a citation requirement, or a human-review path for summaries of legally binding contracts ([ITP] §10 "Customer Contract Summary Agent").

*References: [ITP] §7, §8, §10.*

### 3.4 Model lifecycle and re-embedding
[ITP] §7 pins *"gpt-5-mini – for agentic search and summarization"* and *"text-embedding-3-large for generating document embeddings"* (note [ITP] §10 mis-names the latter *"OpenAI's ext-embedding-3-large"*). No document states model version pinning, deprecation handling, or a **re-embedding/reindex strategy**. An embedding model change forces a full corpus reindex — a significant cost and availability event.

*References: [ITP] §7, §10.*

### 3.5 Custom Document Intelligence models are unscoped
[ITP] §7 and §10 commit to *"custom-trained classification and extraction models trained on Penske's contract formats and terminology."* No labeling effort, model version control, accuracy threshold or low-confidence/unclassified fallback path appears anywhere, and [ITP] §11 contains no corresponding effort line.

*References: [ITP] §7, §10, §11.*

### 3.6 Capacity and quota
No TPM/PTU sizing for the LLM, no Document Intelligence throughput limits, no AI Search tier/replica/partition sizing, no Cosmos RU sizing, and — despite [TD] §7.1.1.3 defining the Cosmos collection — **no partition key decision**.

*References: [TD] §7.1.1.3; [ITP] §3, §7.*

---

## 4. Data architecture

### 4.1 Three metadata stores, no declared system of record
Cosmos DB ([TD] §7.1.1.3), SQL Server/MySQL ([OCP]; [ITP] §5), and the `docs-index` search index ([TD] §7.1.1.3) all hold document metadata. [TD] §6.1 *Physical Data Model, DB Structure, Files and Relations* — the section that should resolve this — contains **only the unmodified template instructions** ("Describe any new files/tables in their entirety, and the relationships between files…"). No reconciliation process is described; drift between Blob, index and Cosmos is inevitable.

*References: [ITP] §5; [TD] §6.1, §7.1.1.3; [OCP].*

### 4.2 XLS as an integration contract
[ITP] §4, §10 and [TD] §4 describe: *"Cataloguing XLS Generation: Generate the cataloguing XLS from Cosmos DB, store it in Blob Storage for FE consumption"* and *"Process the XLS data through the BFF Backend API to extract the catalogued document paths."* A spreadsheet round-trip as a system-to-system interface is brittle and will not scale; an API or Cosmos change-feed sync is the conventional pattern. The team should justify the choice.

*References: [ITP] §4, §10; [TD] §4.*

### 4.3 Index schema is thin and mis-typed
[TD] §7.1.1.3 defines `docs-index` as `id (STRING, PK)`, `content (STRING)`, `contentVector (**STRING**)`, `role (STRING)`, `source (STRING)`.

Two problems:
- **`contentVector` typed as STRING.** An Azure AI Search vector field must be a single-precision collection with a declared dimension and vector search profile. Assumed to be a documentation error, but it must be corrected — it is the core of the retrieval design.
- **Missing fields** for chunk ID, page/offset, document ID, effective dates, customer/entity ID and an ACL/security field. Without the last of these, §2.2 above cannot be implemented at all.

*References: [TD] §7.1.1.3.*

### 4.4 Document lifecycle is absent
[ITP] §10 covers ingestion only. Update, supersession, deletion and retention appear nowhere in [ITP] or [TD]. Deleting a source PDF must also purge its chunks, vectors and Cosmos metadata, or deleted contracts remain answerable by the agents.

*References: [ITP] §10; [TD] §7.1.1.3, §7.1.1.4.*

### 4.5 Idempotency on at-least-once delivery
[ITP] §7 and §10 rely on *"Azure Event Grid to pub-sub blob storage events"* triggering Azure Functions; [AZ] shows Event Grid Subscriptions and a Service Bus queue (`…/onedocumentqueue` per [OCP]). Event Grid and Service Bus both deliver **at-least-once**. No dedupe or idempotency key is defined, so duplicate ingestion will duplicate index entries and skew retrieval.

*References: [ITP] §7, §10; [AZ] Event Grid Subscriptions / Service Bus; [OCP] Azure Service Bus Details.*

---

## 5. Resilience and operations

- **Error handling deferred.** [TD] §12: *"All errors will be logged to logs. No Special handling, recovery/notification is designed for phase1."* This is a material risk acceptance and should be signed off by a named owner. No DLQ/poison-message handling for Service Bus or Event Grid, no retry/backoff policy, no reprocessing runbook.
  *Reference: [TD] §12; [AZ]/[OCP] Service Bus.*
- **Single region, no DR.** All resources in [OCP] and [AZ] are `eus2`. No RTO/RPO, no backup strategy for Cosmos or the search index. Note an AI Search index is not backed up — rebuild time from source must be quantified. [ITP] §9 *Rollout/Implementation Considerations* covers only pre-deployment of agents and the Function App.
  *Reference: [ITP] §9; [AZ]; [OCP].*
- **Observability is thin relative to the diagram.** [AZ] shows Application Insights, Log Analytics Workspaces and an Azure Monitor Private Link Scope, but [TD] §13 describes only standard Python logging. No correlation-ID propagation across OCP → gateway → Azure, no SLOs, no alerting, and **no token-consumption or cost alerting** for a consumption-priced AI workload.
  *References: [AZ] PLTF panel and Application Insights; [TD] §13.*
- **No IaC or CI/CD.** [AZ] shows VMSS Build Agents, and [TD] §5.1 lists Bitbucket and Azure DevOps repositories (`ptl-onedocstorage-data-processor`, `ptl-onedocstorage-mcp-processor`, `onedocstorage-ai-ms`), but no pipeline, environment-promotion path or infrastructure-as-code approach is described anywhere.
  *References: [AZ] VMSS Build Agents; [TD] §5.1.*
- **Irrelevant platform content left in place.** [TD] §5.2 *Directories, Libraries and Programs (IBMi)* and §7.2 *Programs (IBMi)* still carry IBMi template guidance (CORP/GRNHILLS/FLEET libraries, TESTTEST on SUPPORT), and §7.2.1.2 still contains the placeholder *"filename1 = blahblah master file."* This is a Python/Azure workload; these sections should be removed or marked N/A deliberately.
  *References: [TD] §5.2, §7.2, §7.2.1.2.*

---

## 6. Plan, cost and non-functional requirements

- **No costs in the cost section.** [ITP] §3 *Estimated Cost/Benefits of Solution* contains only qualitative benefits (searchability, single structured location, reduced duplication, metadata cataloguing). For a consumption-priced AI workload a modelled run-rate is required: Document Intelligence pages, embedding tokens, LLM tokens per query × expected query volume, AI Search tier, Cosmos RUs, Service Bus and egress.
  *Reference: [ITP] §3.*
- **No non-functional requirements anywhere** in [ITP] or [TD]: corpus size, ingestion rate, document size/page limits, concurrent users, target query latency, availability target.
- **Risks section is empty and corrupted.** [ITP] §5 runs the Catalogued Path Processing paragraph directly into the heading — *"…from Cosmos DB to MySQL Open Issues, Risks, and Assumptions"* — followed by **"N/A"**. Similarly [TD] §15 *Technical Issues* is an empty table and [TD] §4's *Design Issue / Decision and Rationale* table is empty. For a first-of-kind agentic AI system, no recorded risks or design decisions is not credible.
  *References: [ITP] §5; [TD] §4, §15.*
- **Effort looks optimistic.** [ITP] §11: Analysis and Design 10 d, Development 30 d, IT Testing 15 d, QA Testing 15 d, Deployment 5 d — **Total 75 days / 3 months ME**. No line items for custom model training and labeling, prompt engineering, evaluation harness, security review, performance testing or MLOps.
  *Reference: [ITP] §11.*
- **Revision table empty.** [ITP] §12 *Revisions* has no rows, despite [TD]'s Document Revision Chart recording four revisions (11/11, 11/13, 06/26, 09/10) including the 09/10 cataloguing and indexing change.
  *References: [ITP] §12; [TD] Document Revision Chart.*
- **Appendices incomplete.** [ITP] §13 lists *UI/UX Designs: NA* and gives only the folder path for Design Diagrams. The diagrams themselves are not embedded or individually named, so the proposal does not self-evidently reference [AZ] or [OCP].
  *Reference: [ITP] §13.*
- **No accountable business owner.** Product Owner is blank in the Key Stakeholders table and the §2 Project Roles table of [ITP]; the Responsibility column is blank for all three roles. No data owner is named for contract content.
  *Reference: [ITP] Key Stakeholders table, §2.*

---

## 7. Conditions for tollgate approval

1. **Reconcile the artifact set.** Produce one authoritative decision record resolving: MySQL vs SQL Server ([ITP] §5/§10 vs [OCP]); two vs three microservices ([ITP] §4 vs [TD] §4/§7.2.1); `sbx` vs `prod` Cosmos ([TD] §7.1.1.3, [OCP]); Apigee in or out of the request path ([ITP] §7); managed identity vs account key ([AZ] vs [OCP]). **Refresh [AZ]**, dated 06/25/2026, to cover the 09/10 cataloguing/ingestion scope.
2. **Provide an end-to-end authorization design** showing how a validated user identity produces an AI Search security filter, and how per-user contract access is audited. Replace the `<passed>` UserId/Role model in [TD] §7.1.1.3.
3. **Publish the MCP tool inventory and a threat model**, including prompt-injection mitigations, to fill [TD] §7.1.1–§7.1.1.2.
4. **Add NFRs, a capacity/quota plan and a modelled monthly run cost** to [ITP] §3 and a new NFR section.
5. **Design error handling, DLQ, reprocessing and reconciliation**, or formally accept the [TD] §12 phase-1 risk with a named owner and remediation date.
6. **State DR position, RTO/RPO and quantified index rebuild time** in [ITP] §9.
7. **Add an AI evaluation plan** with accuracy thresholds and acceptance criteria to [ITP] §8, plus a document lifecycle/deletion design.
8. **Correct the vector field definition** (`contentVector`) and extend the index schema with chunk, document, date, entity and ACL fields — [TD] §7.1.1.3.
9. **Clean up both documents:** headers/footers, "Sales B2B authentication" identity, [ITP] TOC first line, [TD] TOC numbering (9.2 vs 7.2), residual IBMi template text ([TD] §5.2, §7.2), and populate [ITP] §12, [TD] §4 and [TD] §15.
10. **Name a Product Owner and a data owner** ([ITP] Key Stakeholders, §2).

---

*Prepared as an enterprise architecture review of the design-tollgate-09-10 artifact set. All section numbers refer to the documents as listed in the Source document key above.*
