# Architecture Review — OneDocStorage AI (#608351)

**Reviewer role:** Enterprise Architect
**Artifacts reviewed:**
- IT Proposal — *OneDocStorage AI Design* (#608351), rev. 09/10/2026
- Technical Design — *OneDocStorage AI Design* (#608351), Version 2, rev. 09/10/2026
- `Penske_PTL_One_Document_Search_OAzure_AI_Architecture.pdf` (Azure AI Services – One Document Search, Prod)
- `OneDocStorage AI OCP.pdf` (OCP application view)

---

## Summary

The overall solution *shape* is reasonable and follows a recognised pattern: event-driven ingest → Azure AI Document Intelligence → embeddings → Azure AI Search → AI Foundry agents fronted by Python microservices on OCP.

However, the **design documentation is not yet at tollgate quality**. Several decisions that determine security posture, data ownership and operability are either missing, contradictory across the three artifacts, or stated as aspirations rather than designs. The findings below should be resolved or formally risk-accepted before approval.

---

## 1. Blocking inconsistencies between documents

These are not cosmetic — each one changes the build.

| # | Issue | Detail |
|---|-------|--------|
| 1.1 | **Metadata store contradiction** | IT Proposal §5 says catalogued metadata is pushed from Cosmos DB to **MySQL**. The OCP diagram shows **SQL Server** (`GHSQL10`, database `onedocument`) over JDBC. Which is the system of record? |
| 1.2 | **Number of microservices** | IT Proposal states **two** (Q&A Agent, Summary Agent). Technical Design §4 and §7.2.1 state **three** (adds Inquiry Agent). Effort estimate and deployment plan differ accordingly. |
| 1.3 | **Environment mismatch** | Technical Design §7.1.1.3 names Cosmos `cosmos-onedoc-ptl-**sbx**-eus2-1`; the OCP diagram points at `cosmos-onedoc-ptl-**prod**-eus2-1`. A sandbox resource is referenced in a production design. |
| 1.4 | **Apigee** | Listed in §7 Infrastructure Assessment "for secure API exposure and management", but appears in neither diagram. The OCP diagram shows the client hitting the pod directly behind Redhat SSO. Is Apigee in the request path? |
| 1.5 | **Auth to Cosmos** | The Azure diagram labels flows "HTTPS – Managed Identity"; the OCP diagram lists secret `onedocstorage-ai-cosmos-access-key` (account key). Account keys bypass RBAC and cannot be rotated without downtime. |
| 1.6 | **Document hygiene** | Headers read "[Sales B2B authentication Design]"; footers read "Document3" and "combined IBMi and Java doc". Template instruction text remains in §2, §3, §5.2, §6.1, §7.1. Revisions and Technical Issues tables are empty. Product Owner is blank in both role tables. |

---

## 2. Security and identity — the largest gap

### 2.1 No end-user identity reaches the Azure layer
Auth Flow is **Client Credential**. Every call to AI Search, Foundry, Cosmos and Blob is therefore made as the *application*, not the user. Yet Technical Design §7.1.1.3 stores `UserId` and `Role` in Cosmos as `"<passed>"` values, and the search index carries a single `role` field.

If the caller supplies its own role, entitlement is **client-asserted and therefore spoofable**.

### 2.2 Document-level authorization is undefined
"Cosmos DB to store custom metadata for RBAC enforcement" is an aspiration, not a design. For contract data the design must specify a concrete security-trimming mechanism:
- ACL / group claims stamped onto each chunk at index time
- Enforced as an Azure AI Search `$filter` derived from the **user's validated token**, not from a client-passed field
- A defined behaviour for documents with no ACL (fail closed)

### 2.3 Auditability
With app-only identity, logs cannot answer *"which user asked what, about which customer's contract."* This is likely a compliance requirement for contract data and should be confirmed with Legal/Compliance.

### 2.4 The Security Assessment is not a security assessment
§6 states only that endpoints are client-credential enabled, protected by Redhat SSO, and "will also contain 0 Test detectable security violations." Missing:
- Threat model
- Data classification for contract content (PII, commercial terms, counterparty confidentiality)
- SAST / DAST / penetration test plan
- DLP position
- Azure OpenAI abuse-monitoring, data-residency and retention posture

### 2.5 Secrets management
`azureadclientsecrets` implies password-based client credentials. Recommend **workload identity federation** or certificate auth. Secrets currently appear in both Key Vault and OCP secrets with no described sync or rotation process.

### 2.6 Network posture
Private Link and Alkira are shown, but the design should explicitly assert that **public network access is disabled** on Blob, Cosmos, AI Search, Document Intelligence, Foundry and Service Bus, and document the private DNS resolution path from OCP to `*.search.windows.net`, `*.documents.azure.com`, etc.

---

## 3. AI-specific risks — largely unaddressed

### 3.1 Prompt injection via ingested documents
Untrusted PDFs are chunked into an index that grounds agents which, per §7 and §10, call **Azure Function Apps acting as MCP servers exposing tools**. This is a direct injection-to-tool-execution path.

Required mitigations:
- Tool authorization scoping and least-privilege function identities
- No destructive or write-capable tools exposed to agents
- Input and output content filtering
- Treat all retrieved document content as untrusted data, never as instructions

### 3.2 The MCP server is undocumented
No tool inventory, no auth model, no statement of what data each tool can reach, no blast-radius analysis if an agent is manipulated.

### 3.3 No quality bar
Missing entirely:
- Accuracy targets for Document Intelligence extraction and classification
- A golden/labelled evaluation dataset
- Hallucination and groundedness evaluation
- A citation requirement in agent responses
- A human-review path for summaries of legally binding contracts

### 3.4 Model lifecycle
`gpt-5-mini` and `text-embedding-3-large` are named with no version pinning, deprecation plan, or **re-embedding / reindex strategy**. An embedding model change forces a full corpus reindex — a significant cost and availability event that must be planned for.

### 3.5 Custom Document Intelligence models
Custom classification and extraction models require labeling effort, version control, accuracy thresholds, and a fallback path for unclassified or low-confidence documents. None of this appears in scope or in the effort estimate.

### 3.6 Capacity and quota
No TPM/PTU sizing for the LLM, no Document Intelligence throughput limits, no AI Search tier / replica / partition sizing, no Cosmos RU sizing, and **no Cosmos partition key decision**.

---

## 4. Data architecture

### 4.1 Three metadata stores, no system of record
Cosmos DB + SQL Server/MySQL + the AI Search index, with no stated authority and no reconciliation process. Drift between Blob, index and Cosmos is inevitable without one.

### 4.2 XLS as an integration contract
Generating a cataloguing spreadsheet from Cosmos → Blob → parsed by the BFF → loaded to MySQL is brittle and will not scale. An API or Cosmos change-feed-driven sync is the conventional pattern. The team should justify this choice.

### 4.3 Index schema is thin and likely mis-specified
`docs-index` is defined as `id, content, contentVector, role, source` only. Missing: chunk ID, page/offset, document ID, effective dates, customer/entity ID, ACL field.

Also, `contentVector` is typed **STRING**. A vector field must be a single-precision collection with a declared dimension and vector search profile. Likely a documentation error, but it needs correcting.

### 4.4 Document lifecycle is not covered
Updates, supersession, deletion and retention are absent. Deleting a PDF must also purge its chunks, vectors and Cosmos metadata — otherwise deleted contracts remain answerable by the agents.

### 4.5 Idempotency
Event Grid delivers at-least-once. Without a dedupe/idempotency key, duplicate ingestion will duplicate index entries and skew retrieval.

---

## 5. Resilience and operations

- **§12 "No special handling, recovery/notification is designed for phase1"** is a material risk acceptance that should be explicit and signed off. There is no DLQ / poison-message handling for Service Bus or Event Grid, no retry/backoff policy, and no reprocessing runbook.
- **Single region (EUS2), no DR.** No RTO/RPO. No backup strategy for Cosmos or the search index. Note that an AI Search index is not backed up — rebuild time from source must be quantified.
- **Observability.** App Insights and Azure Monitor appear in the diagram, but §13 describes only standard Python logging. No correlation ID propagation across OCP → gateway → Azure, no SLOs, no alerting, and **no token/consumption monitoring or cost alerting**.
- **No IaC or CI/CD described**, despite VMSS build agents appearing in the architecture diagram. The environment promotion path is undefined.

---

## 6. Plan, cost and non-functional requirements

- **§3 "Estimated Cost/Benefits of Solution" contains no costs.** Benefits are qualitative only. For a consumption-priced AI workload a modelled run-rate is required: Document Intelligence pages, embedding tokens, LLM tokens per query × expected query volume, AI Search tier, Cosmos RUs.
- **No non-functional requirements at all**: corpus size, ingestion rate, document size/page limits, concurrent users, target query latency, availability target.
- **§5 "Open Issues, Risks, and Assumptions = N/A"** is not credible for a first-of-kind agentic AI system. It also appears to have been merged into the Catalogued Path Processing paragraph by a formatting error.
- **75 days / 3 months looks optimistic.** Ten days of analysis and design, and no line items for custom model training/labeling, prompt engineering, evaluation, security review, performance testing, or MLOps.
- **Testing approach is one sentence.** No test data strategy (can production contracts be used in Dev/QA?), no accuracy acceptance criteria, no load/soak test, no security test, no regression suite for agent responses.
- **Product Owner is blank** in both role tables — no accountable business owner for AI output quality, and no named data owner.

---

## 7. Conditions for tollgate approval

1. Produce a single authoritative architecture decision set resolving: MySQL vs SQL Server; two vs three services; sbx vs prod resources; Apigee in or out of the request path; managed identity vs account key.
2. Provide an **end-to-end authorization design** showing how a user's entitlements reach an AI Search security filter, and how per-user access to contracts is audited.
3. Provide the **MCP tool inventory and threat model**, including prompt-injection mitigations.
4. Add non-functional requirements, a capacity/quota plan, and a modelled monthly run cost.
5. Add error handling, DLQ, reprocessing and reconciliation design — or formally accept the phase-1 risk with a named owner and a remediation date.
6. Add DR position, RTO/RPO, and quantified index rebuild time.
7. Add an AI evaluation plan with accuracy thresholds, plus a document lifecycle and deletion design.
8. Clean up the documents (headers, footers, template text, empty tables) and populate Risks and Assumptions.

---

*Prepared as an enterprise architecture review of the design-tollgate-09-10 artifact set.*
