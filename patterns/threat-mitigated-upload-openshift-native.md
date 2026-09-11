---
title: "Threat-Mitigated File Upload Pipeline (On-Premises OpenShift Native Variant)"
status: "active"
date: "2026-09-10"
version: "1.0"
owners:
  - "{team-or-person}"
tags:
  - "architecture-style"
  - "security-pattern"
  - "openshift-native"
related-patterns:
  - "Gatekeeper Pattern"
  - "Secure File Upload Pipeline"
  - "Zero-Trust Upload Architecture"
---
 
# Threat-Mitigated File Upload Pipeline (On-Premises OpenShift Native Variant)
 
## Problem
 
Allowing users to upload files to an enterprise application presents a massive attack vector. Malicious files can contain malware, executable scripts, or format exploits that can compromise core file storage, corrupt internal networks, or infect other users who later download the files.
 
When an architecture is restricted entirely to an on-premises or private Red Hat OpenShift cluster without public cloud object storage (like AWS S3) to act as a buffer, the platform must absorb raw binary data streams directly. Processing these dense files inline inside core web application pods bloats cluster memory, causes severe CPU context switching, and risks exposing the core cluster to Remote Code Execution (RCE) or Denial of Service (DoS) attacks. Furthermore, writing unvalidated data directly to shared storage disks can pollute internal networks and bypass network isolation controls.
 
The recurring problem is therefore: **how to securely ingest, validate, sanitize, and store user-uploaded files natively inside a Red Hat OpenShift cluster without exposing core application microservices or internal persistent volumes to security threats and resource exhaustion.**
 
## Context
 
Describe the environment in which this pattern applies.
 
- **Business context:** Private cloud, sovereign cloud, or on-premises enterprise environments (e.g., core banking systems, government records, or healthcare systems) where data cannot leave the private corporate network, and public cloud services are unavailable or legally prohibited.
- **Technical context:** A native Red Hat OpenShift cluster hosting application microservices and utilizing software-defined or network-attached cluster storage (e.g., OpenShift Data Foundation / Ceph, NetApp Trident, or enterprise NFS) for long-term persistence.
- **Regulatory/compliance context:** High-compliance landscapes requiring complete air-gapped data isolation, local data sovereignty, and an auditable, isolated processing lifecycle for all untrusted external inputs.
- **Organisational context:** A corporate environment where platform engineering teams manage Red Hat OpenShift cluster operations, ingress policies, and storage classes via GitOps (ArgoCD).
- **Assumptions:** The OpenShift cluster is equipped with an ingress controller or API gateway capable of applying rate limits and basic payload constraints at the cluster perimeter.
- **Constraints:** Files must be fully validated and sanitized before they are permitted to enter production storage namespaces or be made visible to other internal microservices.
## Forces
 
- **Deployment independence pulls against data integrity.** Separating deployables invites separating data, which is what destroys transactional guarantees.
- **Team autonomy pulls against coordination cost.** More independently deployable units means less merge contention but more pipelines, dashboards, and contracts to maintain.
- **Granularity pulls in both directions.** Finer services scale and deploy better; coarser services stay self-contained and avoid inter-service chatter.
- **Change-rate variance.** Domains that change weekly and domains that change annually are penalised by being forced onto a shared release train.
- **Operational capability is finite.** Each additional service consumes a fixed quantum of operational attention that does not scale with team size.
- **Cost and time-to-value.** The strongest architecture is worthless if the migration exceeds the organisation's patience or budget.
## Solution
 
Isolate, inspect, and sanitize file uploads using an internal **segmented, asynchronous, cluster-native processing architecture** within Red Hat OpenShift.
 
The web client never streams files to the core business microservices or production storage volumes. Instead, an edge-facing **Upload Proxy Pod** accepts the incoming file stream and streams it immediately to an ephemeral, highly restricted **Quarantined Staging Volume**.
 
The successful write triggers a lightweight internal event via an in-cluster message broker (e.g., **AMQ Streams / Apache Kafka** or **Red Hat AMQ Broker**). A dedicated pool of **Validation Worker Pods**, isolated within a restricted project namespace and auto-scaled via **KEDA**, picks up the event message. The worker pod scans the file for malware using local scanning engines, verifies file signatures (magic bytes), and sanitizes the content. Only upon passing all checks does the worker pod transfer the clean file to the **Production Persistent Volume**, update the database record to `Active`, and purge the staging volume.
 
## Structure
 
| Component | Responsibility |
|---|---|
| **OpenShift Ingress / Route** | The entry point for cluster traffic, enforcing request rate limits and maximum payload size restrictions. |
| **Upload Proxy Pod** | A low-privilege, single-purpose microservice that accepts the file stream from the ingress and streams it directly into the Quarantine Volume. It emits an event to the message broker. |
| **Quarantine Volume (PV)** | An isolated Kubernetes Persistent Volume (ReadWriteMany or ReadWriteOnce depending on scaling metrics) used strictly as an on-premises data DMZ. |
| **In-Cluster Message Broker** | AMQ Streams (Kafka) or AMQ Broker (ActiveMQ). Acts as the asynchronous buffering mechanism, collecting and dispatching upload processing events. |
| **KEDA Operator (OpenShift)** | Monitors internal broker queue depths and dynamically scales the Validation Worker Pods to match incoming traffic patterns. |
| **OpenShift Validation Pods** | Low-privilege pods running in a locked-down namespace. They pull the file from the Quarantine Volume, execute virus scanning (e.g., ClamAV sidecar), and perform binary sanitization. |
| **Production Storage (PV)** | The secure, primary enterprise storage volume class (e.g., ODF / Ceph or enterprise SAN) containing only verified and sanitized active files. |
 
Interaction: the client targets an upload proxy service via an OpenShift Route. The proxy buffers the stream onto a quarantined Persistent Volume and posts an ingestion event to the broker topic. KEDA spins up worker pods to drain the queue. Workers execute signature verification and local virus checks, shifting authorized binary datasets directly onto production enterprise persistent storage.
 
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
 
- The architecture is strictly hosted within a private cloud, on-premises data center, or an air-gapped Red Hat OpenShift cluster environment.
- Corporate governance, regulatory frameworks, or data sovereignty mandates prohibit the routing or storage of enterprise file assets via public cloud infrastructure.
- High traffic variance requires a decoupled processing architecture to prevent user file uploads from degrading core system memory or API responsiveness.
**When not to use this pattern
 
- The cluster architecture has seamless access to cloud-native public edge buffers (like AWS S3) that can be utilized to offload initial raw binary stream absorption.
- The application handles extremely low file upload volume (<10 files per day) and file sizes are miniature, making the overhead of message brokers and dedicated workers unnecessary.
## Consequences
 
### Benefits
 
- **Absolute Data Sovereignty:** Raw data, processing compute pipelines, and final file architectures remain 100% within the walls of the corporate private cloud infrastructure.
- **Cluster Resource Hardening:** Ingress routes and core application pods are completely protected from memory exhaustion or unexpected binary processing crashes.
- **Blast Radius Reduction:** If a malformed file triggers a zero-day exploit or RCE inside a container tool, the damage is restricted to an isolated, non-root OpenShift namespace with no lateral network connectivity.
- **Predictable Elasticity:** Cluster administrators can limit the max replicas of the Validation Workers to prevent file processing spikes from consuming compute resources required by core transaction pods.
### Trade-offs
 
- **Increased On-Premises Compute Demand:** Antivirus scanning and file transformation (CDR) are CPU-heavy operations that will consume bare-metal or hypervisor compute nodes within your own cluster footprint.
- **Complex Private Storage Orchestration:** Managing sharing and file locks across multiple pods on an internal staging volume requires enterprise storage options capable of supporting efficient `ReadWriteMany (RWX)` volumes (e.g., ODF / CephFS).
- **Asynchronous Front-End Design:** UI development teams must implement cluster-native asynchronous updating patterns, like routing WebSocket connections through an OpenShift route to push status changes to the user browser.
## Variants
 
- **Sandbox Execution Variant:** High-security applications route files through a full execution sandbox machine, mimicking user interactions inside an isolated OS container to screen for behavioral anomalies before promotion.
- **Shared In-Memory Storage Proxy:** In clusters with extreme throughput limits and highly optimized memory pools, the staging storage disk is swapped for a cluster-wide distributed in-memory cache framework (e.g., Red Hat Data Grid / Infinispan).
## Example
 
An on-premises government portal built on Red Hat OpenShift allows citizens to upload tax documentation (PDFs and Excel sheets).
 
Previously, files were posted directly to the core citizen-accounting web pods. An attacker uploaded a maliciously crafted Excel document that contained an embedded binary string targeting an unpatched exploit in the web pod's parsing library, gaining an internal shell inside the application namespace.
 
After partitioning, a user uploads a document. The traffic hits the OpenShift Ingress and is sent to a low-privilege `Upload Proxy Pod`. The proxy writes the file to a temporary, encrypted OpenShift Persistent Volume backed by OpenShift Data Foundation (`odf-quarantine-claim`) and drops a `file-uploaded` event onto a Red Hat AMQ queue. The KEDA operator detects the new message and scales up the `document-validator` pods in a restricted namespace. The validator pod accesses the quarantine disk, passes the file stream to its internal ClamAV sidecar container, strips out macros from the Excel sheet, and moves the verified, sanitized document over to the enterprise core data storage volume (`odf-production-claim`). The staging footprint is wiped, and an internal event changes the state of the citizen’s document record to "Verified."
 
## Known Uses
 
- {Sovereign Government Cloud Citizen Document Portal}
- {Private Banking Infrastructure Secure Invoice Ingestion Engine}
## Related Decisions / ADRs
 
- ADR-033: Deploying KEDA for Private Queue Scale Optimization
- ADR-054: Implementing OpenShift Data Foundation (ODF) for Secure Multi-Pod Storage
- ADR-072: Standardizing Container Security Context Constraints (SCC) across Ingress Zones
## References
 
- Red Hat OpenShift Documentation — *Managing Networking and NetworkPolicies*
- Red Hat Documentation — *AMQ Streams and OpenShift Container Platform Integration*
- OWASP — *File Upload Security Defenses for On-Premises Topologies*
## Revision History
 
| Date | Version | Notes |
|------|---------|-------|
| 2026-09-10 | 1.0 | Initial template adaptation for Private, Native OpenShift-Only Architectures |
