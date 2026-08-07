# Federated Architecture Review — Story Inputs
**Stories covered:** EA-320 (Review Workflow), EA-321 (Review Request Process), EA-327 (Portfolio Reviewer Responsibilities)
**Epics:** Federated Architecture Review Process / Portfolio Reviewer Program

---

## 0. Working assumptions — confirm these before you publish anything

These three stories only hang together if the following are true. If any is wrong, tell me and the content below shifts.

| # | Assumption | Why it matters |
|---|---|---|
| A1 | "Application portfolio" is an already-defined grouping of apps with a named owner (e.g. Finance, Logistics, Fleet Maintenance, HR). | The routing rule in EA-321 depends on a portfolio→reviewer map existing. |
| A2 | A Portfolio Reviewer is a senior engineer/architect **inside** the portfolio, exercising authority **delegated** by EA — not a full-time EA headcount. | Drives the time-commitment and decision-rights sections of EA-327. |
| A3 | Solution Architecture (SA) remains the central team for exceptional cases and retains the standards/reference architectures. | Defines the escalation boundary. |
| A4 | Tooling is Jira (EA project) for tracking + Confluence for design artifacts and decision records. | Statuses, forms, and where decisions live. |
| A5 | There is (or will be) a published set of architecture standards, reference architectures, and an approved technology list that reviewers review *against*. | Without this, reviewers are giving opinions, not decisions. This is the single biggest dependency — raise it as a blocker if it doesn't exist. |

---

# EA-320 — Define Architecture Review Workflow

## Suggested description (replaces/extends what's there)

Define and document the new federated architecture review workflow that enables application portfolio reviewers to review application designs within their portfolio, with only exceptional cases brought to the solution architecture team.

**In scope:** the end-to-end steps from an accepted review request through to a recorded, tracked decision — including review tiers, entry/exit criteria per step, roles at each step, target SLAs, Jira statuses, and where decisions are recorded.

**Out of scope:** intake and routing mechanics (EA-321), reviewer role and decision rights (EA-327), escalation triggers and paths (separate story), reviewer onboarding/certification (Portfolio Reviewer Program epic).

## Draft workflow content

### 1. Review tiers — set the depth of review up front

Tiering is the mechanism that makes federation work. Without it, every change gets the same heavyweight treatment and reviewers become a bottleneck.

| Tier | Trigger | Who reviews | Format |
|---|---|---|---|
| **T1 — Self-attest** | Change uses only approved technology and an established pattern; no new integrations; no change to data classification; contained blast radius. | Requesting team completes checklist; Portfolio Reviewer confirms. | Async, no meeting. Target: 2 days. |
| **T2 — Portfolio review** (default) | New or changed integrations, significant change within existing standards, new component within an approved stack, material NFR change. | Portfolio Reviewer, SMEs invited as flagged. | Review session. |
| **T3 — Solution Architecture review** | Net-new technology or pattern, cross-portfolio impact, regulated/restricted data, material cost or risk, standards exception requested. | SA team, Portfolio Reviewer participates. | Escalated — mechanics per escalation story. |

Tiering must be **self-serviceable**: a delivery team should be able to determine its own tier from published criteria without asking EA. The Portfolio Reviewer confirms or corrects the tier at triage.

### 2. Workflow steps

1. **Triage & assign** — request accepted from intake (EA-321). Reviewer assigned, tier confirmed, target dates set.
2. **Design package submitted** — entry criteria met (see artifact list below).
3. **Completeness check** — Reviewer pre-reads and gates: *Ready for review* or *Returned for information* (SLA clock pauses).
4. **Review** — T2: time-boxed session (60 min suggested) with design owner, product owner, and flagged SMEs (security, data, infrastructure, network, integration). T1: async checklist confirmation.
5. **Record findings** — each finding classified and given an owner:
   - **Blocker** — must be resolved before approval
   - **Required** — must be resolved before production, tracked as a condition
   - **Recommended** — strong guidance, team may decline with rationale
   - **Observation** — informational, feeds tech-debt register
6. **Decision** — exactly one of: *Approved* · *Approved with conditions* · *Revise and resubmit* · *Escalate to Solution Architecture* · *Not approved*.
7. **Publish decision record** — short ADR-style record linked to the Jira issue and the portfolio's architecture space. Records are versioned, not edited.
8. **Track conditions** — conditions become tracked items with owner and due date, visible in EA reporting. Approval is not "done" until conditions close.
9. **Post-implementation verification** — sampled or trigger-based check that what shipped matches what was approved. Drift feeds the portfolio backlog / tech-debt register.
10. **Close.**

### 3. Required design package artifacts (entry criteria for step 2)

- Business context and drivers; who the change serves
- Context / system landscape diagram (current and target)
- Logical component view
- Integration inventory — interfaces, protocols, sync/async, volumes
- Data flows, data classification, retention and residency
- Non-functional targets — availability, RTO/RPO, performance, scale
- Security considerations — authN/authZ, secrets, exposure surface
- Hosting, deployment, and environment model
- Alternatives considered and why rejected
- Dependencies and assumptions
- Cost estimate (build and run)
- Known exceptions to standards being requested

Publish a template for each. A package that is missing items goes to *Returned for information* — that gate is what protects reviewer time.

### 4. Suggested Jira statuses

`Draft → Submitted → Triaged → Awaiting Information → In Review → Decision Pending → (Approved | Approved with Conditions | Escalated | Not Approved) → Conditions Open → Closed`

### 5. Draft SLAs (need agreement, not invention)

| Step | Target |
|---|---|
| Triage and reviewer assignment | 2 business days |
| Completeness check after package submitted | 3 business days |
| Review session scheduled | Within 10 business days of *Ready for review* |
| Decision published after session | 3 business days |
| **Clock pauses** in *Awaiting Information* | — |

### 6. RACI (draft)

| Step | Portfolio Reviewer | Delivery team | Solution Architecture | EA lead |
|---|---|---|---|---|
| Tier classification | A | R | C | I |
| Design package | C | R/A | I | I |
| Review & findings | R/A | C | C | I |
| Decision (T1/T2) | A | I | C | I |
| Decision (T3) | C | I | R/A | I |
| Condition closure | A | R | I | I |
| Post-implementation check | R | C | I | A |

## Acceptance criteria

- [ ] Workflow documented in Confluence with a swimlane diagram and a step-by-step table.
- [ ] Review tiers defined with criteria objective enough that a delivery team can self-classify.
- [ ] Entry and exit criteria stated for every step.
- [ ] Required design artifacts listed, each with a linked template.
- [ ] Decision types enumerated, with who is authorised to issue each.
- [ ] Finding severity model defined.
- [ ] Target SLAs stated per step, including pause conditions.
- [ ] Jira statuses and transitions mapped to workflow steps; configuration request raised with the Jira administrator.
- [ ] Decision record format, location, versioning, and retention defined.
- [ ] Handoff point to escalation identified and cross-linked to the escalation story (no duplicate detail).
- [ ] Reviewed and signed off by: EA lead, SA lead, and at least two Portfolio Reviewers.
- [ ] Walkthrough delivered to one pilot portfolio.

## Suggested sub-tasks

1. Draft tier classification criteria
2. Draft workflow diagram
3. Define design package artifact list + templates
4. Define decision types and finding severities
5. Propose SLAs and socialise with delivery leads
6. Map Jira workflow states, raise admin request
7. Define decision record format
8. Review and sign-off session

## Open decisions to raise

- Who breaks a tie if a Portfolio Reviewer and delivery team disagree and neither wants to escalate?
- Is architecture review a **gate** (delivery cannot proceed) or an **advisory checkpoint**? This changes everything downstream — get an explicit answer.
- Does an approval expire? Suggest 6 months, after which material change triggers re-review.
- How are conditions enforced if a team ships without closing them?

---

# EA-321 — Define Architecture Review Request Process

## Suggested description (extends what's there)

Define the process that application portfolio teams must follow to request a review. This should include a request process directly to their portfolio reviewer and the process of escalating a review to solution architecture. Application portfolio teams should also be able to request a review directly from the solution architecture team.

**In scope:** when a review is required, how it is requested, what information the request must contain, how requests route to the right reviewer, acknowledgement timing, and the two non-default paths (direct-to-SA and escalation handoff).

**Out of scope:** what happens once the request is accepted (EA-320), escalation triggers (escalation story), reviewer responsibilities (EA-327).

## Draft content

### 1. When a review is required — mandatory triggers

Publish this as a checklist. If **any** apply, a review request is required:

- New application, or replacement of an existing one
- New vendor/SaaS product, or a material change in how an existing one is used
- New or changed integration between applications or with an external party
- Change in data classification, or new movement of restricted/regulated data
- Introduction of technology not on the approved technology list
- Material change to hosting, platform, or deployment model
- Change materially affecting availability, DR posture, or stated NFRs
- Request for an exception to an architecture standard
- Decommission or consolidation of an application
- Material change to identity, authentication, or authorisation approach

Publish an explicit "you do **not** need a review for…" list as well (bug fixes, config within approved bounds, like-for-like version upgrades, UI changes with no integration or data impact). This is what prevents over-submission — teams default to submitting everything if the "no" list is missing.

### 2. When to request — timing

Requests should be raised **during solution shaping, before build commitment** — when the design is coherent enough to evaluate but changeable enough that findings can still be acted on. State this as a rule, and state the consequence of late submission (findings become tech debt or rework, and the reviewer records it as such).

### 3. Request channels

| Path | When | Route to |
|---|---|---|
| **Standard** | Default for all requests. | Portfolio Reviewer for that application's portfolio |
| **Direct to Solution Architecture** | Application spans multiple portfolios; no reviewer assigned to the portfolio; reviewer is the design author (conflict of interest); reviewer unavailable beyond SLA; request is clearly T3 by published criteria. | SA intake queue |
| **Escalation** | An in-flight review that the Portfolio Reviewer refers upward. Raised by the reviewer, not the team. | SA, with review history attached |

Note the conflict-of-interest path explicitly — a reviewer cannot approve their own design, and in a federated model this *will* happen.

### 4. Intake form — required fields

Single Jira issue type (suggest "Architecture Review Request") with:

- Requesting team and named requester
- Application(s) and portfolio — a picklist driven by the application inventory, not free text
- Change summary and business driver
- Proposed tier (with the classification criteria linked from the form)
- Trigger(s) that apply, from the mandatory list
- Target decision date and what it is driven by
- Data classification involved
- Link to design package (or "in progress", with expected date)
- Known standards exceptions being sought
- Dependencies on other in-flight work
- Requested path (standard / direct-to-SA, with reason)

Make portfolio and application picklists; free-text portfolio names will break routing within a month.

### 5. Routing

- Portfolio → Reviewer mapping maintained in a single published register with a named backup per portfolio.
- Auto-assign on submission from the portfolio field where Jira allows it; otherwise a triage rota.
- Unmapped portfolio → falls through to the SA queue, and the gap is logged as an action against the Portfolio Reviewer Program.

### 6. Acknowledgement and confirmation

- Acknowledgement within 2 business days: reviewer named, tier confirmed or corrected, and either target review date or a list of what's missing.
- Requests dormant for 20 business days are closed as stale and can be reopened.

### 7. Escalation handoff (reference only)

When a Portfolio Reviewer escalates, the request carries forward: original submission, design package, findings recorded to date, the reviewer's stated reason for escalation, and the specific question being put to SA. Detailed triggers and paths are defined in the escalation story — link, don't duplicate.

## Acceptance criteria

- [ ] Mandatory review triggers published as a checklist.
- [ ] Explicit "no review required" list published.
- [ ] Timing rule stated (request during solution shaping, before build commitment).
- [ ] All three request paths documented with entry conditions, including conflict of interest.
- [ ] Intake form fields specified; Jira request type configuration raised with the administrator.
- [ ] Portfolio-to-reviewer register created, with named backups, and an owner for keeping it current.
- [ ] Routing logic defined, including the unmapped-portfolio fallback.
- [ ] Acknowledgement SLA and stale-request rule defined.
- [ ] Escalation handoff contents specified and cross-linked to the escalation story.
- [ ] Process communicated to delivery leads across at least the pilot portfolios.

## Suggested sub-tasks

1. Draft trigger and non-trigger checklists
2. Design intake form fields; raise Jira config request
3. Build portfolio→reviewer register and assign an owner
4. Define routing and fallback rules
5. Document direct-to-SA and escalation handoff paths
6. Write the requester-facing "how to request a review" page
7. Socialise with delivery leads

## Open decisions to raise

- Jira issue type in the EA project, or a Jira Service Management portal? A portal gives a better requester experience and cleaner SLA reporting; a Jira issue type is faster to stand up. Decide before configuration work starts.
- Who owns the portfolio→reviewer register, and how often is it reconciled against the application inventory?
- Is direct-to-SA self-declared by the team, or does SA triage and bounce it back? Self-declared is faster but leaks; SA triage is cleaner but adds a hop.

---

# EA-327 — Define Portfolio Reviewer Responsibilities

## Suggested description (extends what's there)

Create and document a list of the responsibilities of an application portfolio reviewer, including scope of authority, decision rights, expected time commitment, required competencies, and what is explicitly out of scope for the role.

## Draft content

### 1. Role summary

The Portfolio Reviewer is a senior technical practitioner aligned to an application portfolio who exercises architecture review authority delegated by Enterprise Architecture. They are accountable for the architectural integrity of designs within their portfolio and for escalating what falls outside their delegated authority.

### 2. Core responsibilities

**Review and decision**
- Confirm or correct the review tier for incoming requests
- Assess designs against published standards, reference architectures, and the approved technology list
- Convene and run T2 reviews; invite the right SMEs
- Record findings with severity, owner, and due date
- Issue decisions within delegated authority
- Escalate cases that exceed that authority, with a clearly stated question

**Documentation and traceability**
- Author or approve the decision record for every review
- Maintain the portfolio's architecture documentation currency
- Log observations to the portfolio's tech-debt register

**Portfolio stewardship**
- Maintain a current view of the portfolio's application landscape and target state
- Identify duplication, drift, and end-of-life risk; feed these into portfolio planning
- Advise delivery teams during solution shaping — this is the highest-leverage part of the role, and the part most often squeezed out

**Community and standards**
- Participate in the reviewer community of practice
- Feed recurring findings back to EA/SA as candidate new standards or patterns
- Contribute to reference architecture development
- Mentor delivery-team engineers so that fewer designs need correcting at review

### 3. Decision rights — what a reviewer may and may not decide

| Reviewer **may** | Reviewer **must escalate** |
|---|---|
| Approve designs using approved technology and established patterns | Introduction of technology not on the approved list |
| Approve with conditions, and set condition due dates | Any request for an exception to a published standard |
| Require rework and refuse approval within their portfolio | Designs with cross-portfolio impact |
| Waive *Recommended* findings with recorded rationale | Restricted/regulated data crossing a new boundary |
| Confirm or correct review tier | Material unbudgeted cost or enterprise-level risk |
| — | Any design they authored or materially contributed to |

Being explicit here is what makes federation safe. Ambiguous authority produces either rubber-stamping or everything escalating.

### 4. Time commitment

Suggested baseline, to be validated against real volumes in the pilot: **0.5–1 day per week**, comprising review sessions, pre-reads and decision records, community of practice, and advisory time with delivery teams. This must be formally protected by the reviewer's line manager, in writing. An unfunded reviewer role degrades into a rubber stamp within a quarter — this is the most common failure mode of federated review.

### 5. Competencies

- Solution design experience across integration, data, and infrastructure concerns
- Working knowledge of the enterprise's standards, reference architectures, and approved technology
- Deep familiarity with their portfolio's applications and business domain
- Ability to write a clear, defensible decision record
- Comfort holding a position with delivery teams under schedule pressure

### 6. Explicitly out of scope

- Producing designs on behalf of delivery teams (advisory, not authorship)
- Line management of delivery engineers
- Project delivery accountability
- Setting enterprise standards unilaterally (they propose; EA/SA ratify)
- Approving their own designs
- Security, data privacy, or compliance sign-off where a separate accountable function exists — the reviewer coordinates, they don't substitute

### 7. Success measures

- Requests acknowledged and decided within SLA
- Every review has a published decision record
- Conditions closed within due dates
- Escalation rate within an expected band — high means authority is too narrow, near-zero means escalation criteria are being ignored
- Reduction in repeat findings across the portfolio over time
- Delivery-team satisfaction with the review experience

### 8. Appointment and support

- Nominated by the portfolio's technology leader, endorsed by EA
- Named backup per portfolio
- Onboarding covers workflow, standards, decision-record writing, and shadowing at least two reviews
- Refreshed annually; standing forum for reviewers to raise ambiguity

## Acceptance criteria

- [ ] Role summary, responsibilities, competencies, and out-of-scope items documented in Confluence.
- [ ] Decision rights table published, mapped to the escalation criteria in the escalation story.
- [ ] Expected time commitment stated and agreed with the portfolio technology leaders.
- [ ] Appointment, backup, and onboarding path defined.
- [ ] Success measures defined and reportable from Jira/Confluence data.
- [ ] Explicit statement of what the role does *not* cover, including the relationship to security, data privacy, and compliance functions.
- [ ] Reviewed with at least two nominated reviewers and their line managers.
- [ ] Signed off by EA lead.

## Suggested sub-tasks

1. Draft responsibilities and out-of-scope list
2. Draft decision rights table; reconcile with escalation story
3. Validate time commitment with a pilot portfolio
4. Define appointment, backup, and onboarding
5. Define success measures and confirm they are reportable
6. Review with nominated reviewers and their managers

## Open decisions to raise

- Is this role recognised in job descriptions and performance objectives, or purely goodwill? Goodwill does not survive a busy quarter.
- One reviewer per portfolio, or a small panel for larger portfolios?
- What happens when a reviewer and their own portfolio's delivery pressure conflict — who backs the reviewer?

---

# Cross-cutting notes

**Sequencing.** EA-327 (decision rights) and the escalation story constrain both EA-320 and EA-321. Draft the decision rights table first, or you'll rewrite the other two. Suggested order: EA-327 decision rights → escalation triggers → EA-320 workflow → EA-321 intake.

**The dependency to raise now.** All three stories assume published standards, reference architectures, and an approved technology list exist and are current. If they don't, reviewers have nothing objective to review against, and the process will produce inconsistent decisions that delivery teams will learn to route around. If that's the situation, raise it as a blocking dependency on the epic rather than absorbing it silently into these stories.

**Pilot before rollout.** Run this with one or two portfolios for a quarter, instrument the SLAs and escalation rate, then adjust tier criteria and decision rights before going enterprise-wide.
