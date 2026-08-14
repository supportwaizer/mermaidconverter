# Federated Architecture Review Process

## Purpose

The Architecture Review Process defines the activities required to initiate, review, approve, govern, and close an Architecture Review Request.

The process provides a consistent workflow for:

- Submitting an Architecture Review Request.
- Creating and maintaining the associated Jira records.
- Conducting a Portfolio Architecture Review.
- Escalating a review to Solution Architecture (SA) when required.
- Obtaining Specialist/ODT consultation when required.
- Recording review findings, required changes, and approvals.
- Creating and maintaining the Tollgate Governance Record (PC2 Entry).
- Completing the IT Governance review.
- Recording the final review status and closing the associated Jira tasks.

The process begins when a review request is initiated and ends when the Architecture Review is completed.

---

# Process Participants

The process includes the following participants.

## APT Initiator

The APT Initiator initiates the Architecture Review Request and provides the information and supporting documentation required for the review.

The APT Initiator also participates in PC2 creation and updates when required.

## APT Reviewer

The APT Reviewer coordinates the Architecture Review process and performs the Portfolio Architecture Review.

The APT Reviewer creates and maintains the applicable Jira records, validates documentation, records Portfolio Review findings, determines whether escalation to SA is required, coordinates downstream activities, and completes the final Jira closure activities.

## Solution Architecture (SA)

Solution Architecture performs the escalated Architecture Review when an SA Review is required.

SA validates the escalated review documentation, conducts the SA Review, determines whether Specialist/ODT consultation is required, identifies required changes, and records SA approval.

## ODT

ODT provides specialist consultation when requested during the SA Review.

ODT participation is based on the needs of the specific Architecture Review.

## IT Governance (ITG)

IT Governance performs the governance review after the required architecture review and approval activities have been completed.

ITG reviews the documentation and approvals recorded in Jira and records the Governance Approval in the ITG Jira subtask.

---

# Process Diagram

The following BPMN diagram provides an end-to-end view of the
Architecture Review Process and the responsibilities across the
participating teams.

![Architecture Review Process](images/architecture-review-process.png)

---

# Process Flow

## 1. Initiate Architecture Review Request

The process begins with:

**Review Request Initiated**

The APT Initiator performs:

**Submit Architecture Review Request via MS Form**

The Microsoft Form is used to initiate the Architecture Review process and provide the initial information required to establish the review.

---

## 2. Create Architecture Review Jira Records

Following submission of the request, the APT Reviewer creates the Jira records used to track the review.

The APT Reviewer performs:

**Create Architecture Review Jira Task**

The Architecture Review Jira task serves as the parent Jira record for the review.

The APT Reviewer then performs:

**Create APT Jira Sub-task**

The APT Jira sub-task is used to track the Portfolio Review activities associated with the Architecture Review.

---

## 3. Attach Supporting Documentation

The APT Initiator performs:

**Attach Supporting Documentation**

The documentation required to support the Architecture Review is attached to the review.

The review then proceeds to documentation validation.

---

## 4. Validate Portfolio Review Documentation

The APT Reviewer performs:

**Validate and Review Documentation**

The submitted information and supporting documentation are reviewed to determine whether the request contains sufficient information to proceed with the Portfolio Review.

The process reaches the gateway:

**Review Ready?**

### No — Review Is Not Ready

If the review is not ready, the APT Initiator performs:

**Provide Required Information**

The requested information or documentation is provided.

The process returns to the documentation submission and validation activities.

The cycle continues until the review is ready.

### Yes — Review Is Ready

If sufficient information has been provided, the APT Reviewer performs:

**Set Portfolio Review to In Progress**

The Portfolio Review is then ready to be scheduled and conducted.

---

## 5. Conduct Portfolio Architecture Review

The APT Reviewer performs:

**Schedule Portfolio Review**

The Portfolio Architecture Review is scheduled.

The APT Reviewer then performs:

**Conduct Portfolio Architecture Review**

The proposed architecture and supporting documentation are reviewed.

Following the review, the APT Reviewer performs:

**Record Portfolio Review Findings in Jira**

The findings from the Portfolio Architecture Review are recorded in Jira.

The process then reaches the gateway:

**SA Review Required?**

---

# Portfolio Review Decision

## 6. SA Review Is Not Required

If an SA Review is not required, the APT Reviewer performs:

**Record Portfolio Review Approval in Jira**

The Portfolio Review approval is recorded in Jira.

The process can then proceed toward Tollgate Governance / PC2 processing.

As part of this path, SA is notified and the activities required to establish the PC2 record are initiated.

---

## 7. SA Review Is Required

If the Portfolio Review determines that an SA Review is required, the APT Reviewer performs:

**Assign Escalated Review to SA**

The review then enters the Solution Architecture portion of the process.

---

# Solution Architecture Review

## 8. Validate Escalated Review Documentation

SA performs:

**Validate Escalated Review Documentation**

The documentation supporting the escalated Architecture Review is reviewed to determine whether sufficient information exists to conduct the SA Review.

The process reaches the gateway:

**Review Ready?**

### No — Escalated Review Is Not Ready

If additional information is required:

**Request Required Information**

The required information is requested.

Once the additional information is supplied, the escalated review documentation is validated again.

This cycle continues until the review is ready.

### Yes — Escalated Review Is Ready

When the review is ready:

**Set SA Review to In Progress**

The SA Review proceeds.

---

## 9. Schedule and Conduct SA Review

SA performs:

**Schedule SA Review**

followed by:

**Conduct SA Review**

The architecture is reviewed by Solution Architecture.

During the review, SA determines whether additional specialist input is required.

The process reaches the gateway:

**Specialist Consultation Required?**

---

# Specialist / ODT Consultation

## 10. Specialist Consultation Is Required

If specialist consultation is required:

**Obtain Specialist/ODT Consultation**

The appropriate Specialist/ODT is consulted.

The specialist consultation provides additional input to the SA Review.

After the consultation is obtained, the review returns to SA so that the specialist input can be incorporated into the review.

## 11. Specialist Consultation Is Not Required

If specialist consultation is not required, the process proceeds directly to the SA approval decision.

---

# SA Approval

## 12. Determine SA Approval

The process reaches the gateway:

**SA Approval Granted?**

### No — SA Approval Is Not Granted

If SA does not approve the architecture, SA performs:

**Record Required Changes in Jira**

The required architecture changes are recorded in Jira.

The required changes are then returned to APT through:

**Return Required Changes to APT**

APT addresses the required changes and the review is returned through the appropriate review cycle.

### Yes — SA Approval Is Granted

If SA approves the architecture, SA performs:

**Record SA Approval in Jira**

The SA approval becomes part of the Architecture Review record.

The process can then proceed to Tollgate Governance / PC2 processing.

---

# Tollgate Governance / PC2

## 13. Notify SA

On the applicable Portfolio Review path:

**Notify SA**

SA is notified of the review outcome.

---

## 14. Create APT Subtask for PC2 Creation

The process performs:

**Create APT Subtask for PC2 Creation**

The subtask is used to track the work required to establish the PC2 governance record.

---

## 15. Create Tollgate Governance Record

The APT Initiator performs:

**Create Tollgate Governance Record (PC2 Entry)**

The PC2 Entry becomes the Tollgate Governance Record associated with the Architecture Review.

---

# IT Governance

## 16. Create ITG Subtask and Notify IT Governance

The APT Reviewer performs:

**Create ITG Subtask and Notify IT Governance (Email Template)**

An ITG Jira subtask is created to track the governance review.

IT Governance is notified using the applicable email template.

---

## 17. Review Documentation and Approval

IT Governance performs:

**Review Documentation and Approval recorded in Jira**

IT Governance reviews the documentation and the applicable architecture approval recorded in Jira.

The process reaches the gateway:

**Governance Review Complete?**

---

## 18. Governance Review Is Not Complete

If the Governance Review is not complete, updates to the PC2 Entry are required.

The APT Initiator performs:

**Update PC2 Entry with suggested changes**

The requested changes are made to the PC2 Entry.

The updated information is then returned to IT Governance for review.

The cycle continues until the Governance Review is complete.

---

## 19. Governance Review Is Complete

When the Governance Review is complete, IT Governance performs:

**Record Governance Approval in ITG Jira Subtask**

The Governance Approval is recorded in the ITG Jira subtask.

The Architecture Review can then proceed to final closure.

---

# Architecture Review Closure

## 20. Record Final Review Status

The APT Reviewer performs:

**Record Final Review Status in Parent Jira**

The final Architecture Review status is recorded in the parent Architecture Review Jira task.

---

## 21. Complete and Close Jira Tasks

The APT Reviewer performs:

**Set ar-complete and Close Jira Tasks**

The Architecture Review Jira records are updated to indicate completion and the applicable Jira tasks are closed.

The process reaches the end event:

**Architecture Review Completed**

---

# Review and Rework Loops

The process contains several feedback loops to ensure that a review does not proceed without the required information, changes, or governance updates.

## Portfolio Review Documentation

If the initial Portfolio Review documentation is incomplete:

**Validate and Review Documentation → Review Ready? → Provide Required Information → Attach Supporting Documentation → Validate and Review Documentation**

## Escalated SA Review Documentation

If an escalated review does not contain sufficient information:

**Validate Escalated Review Documentation → Review Ready? → Request Required Information → Validate Escalated Review Documentation**

## SA Required Changes

If SA approval is not granted:

**SA Approval Granted? → Record Required Changes in Jira → Return Required Changes to APT → Rework / Review**

## Governance / PC2 Changes

If the Governance Review is not complete:

**Review Documentation and Approval recorded in Jira → Governance Review Complete? → Update PC2 Entry with suggested changes → Governance Review**

These loops allow issues to be corrected without closing and recreating the Architecture Review.

---

# Jira and Governance Records

The process uses the following primary records.

| Record | Description |
|---|---|
| Architecture Review Request | Initial request submitted through the MS Form |
| Architecture Review Jira Task | Parent Jira record used to track the Architecture Review |
| APT Jira Sub-task | Tracks the Portfolio Review activities |
| Portfolio Review Findings | Findings recorded as a result of the Portfolio Architecture Review |
| Portfolio Review Approval | Approval recorded when the Portfolio Review does not require escalation to SA |
| Escalated SA Review | SA review initiated when escalation is required |
| Required Changes | Architecture changes identified during SA Review and recorded in Jira |
| SA Approval | Solution Architecture approval recorded in Jira |
| APT Subtask for PC2 Creation | Tracks creation of the PC2 governance record |
| Tollgate Governance Record (PC2 Entry) | PC2 governance record associated with the review |
| ITG Jira Subtask | Tracks the IT Governance review |
| Governance Approval | IT Governance approval recorded in the ITG Jira subtask |
| Parent Jira Final Review Status | Final Architecture Review outcome |
| `ar-complete` | Jira status/label used to identify the completed Architecture Review |

---

# RACI Matrix

The RACI Matrix identifies ownership, roles, and expectations for the major activities in the Architecture Review Process.

| Activity | APT Initiator | APT Reviewer | Solution Architect (SA) | ODT Contact | ITG Contact |
|---|:---:|:---:|:---:|:---:|:---:|
| Submit Architecture Review Request | **R/A** | I | I | I | I |
| Attach / Upload Supporting Documentation | **R/A** | C | I | I | I |
| Create Architecture Review Jira Task | I | **R/A** | I | I | I |
| Create APT Jira Sub-task | I | **R/A** | I | I | I |
| Validate Portfolio Review Readiness | C | **R/A** | I | I | I |
| Provide Required Information | **R** | **A** | I | I | I |
| Set Portfolio Review to In Progress | I | **R/A** | I | I | I |
| Schedule Portfolio Review | C | **R/A** | I | I | I |
| Conduct Portfolio Architecture Review | C | **R/A** | I | I | I |
| Record Portfolio Review Findings | I | **R/A** | I | I | I |
| Determine if SA Review Is Required | I | **R/A** | C | I | I |
| Record Portfolio Review Approval | I | **R/A** | I | I | I |
| Assign Escalated Review to SA | I | **R/A** | I | I | I |
| Validate Escalated Review Readiness | C | C | **R/A** | I | I |
| Request Additional Information for SA Review | **R** | C | **A** | I | I |
| Set SA Review to In Progress | I | I | **R/A** | I | I |
| Schedule SA Review | C | I | **R/A** | C | I |
| Conduct SA Review | C | C | **R/A** | C | I |
| Determine if Specialist/ODT Consultation Is Required | I | C | **R/A** | C | I |
| Provide Specialist/ODT Consultation | I | I | **A** | **R** | I |
| Determine SA Approval | I | C | **R/A** | C | I |
| Record Required Changes in Jira | I | C | **R/A** | C | I |
| Return Required Changes to APT | **R** | **A** | C | I | I |
| Record SA Approval in Jira | I | I | **R/A** | I | I |
| Notify SA | I | **R/A** | I | I | I |
| Create APT Subtask for PC2 Creation | C | **R/A** | I | I | I |
| Create Tollgate Governance Record (PC2 Entry) | **R/A** | C | I | I | I |
| Create ITG Subtask | I | **R/A** | I | I | I |
| Notify IT Governance | I | **R/A** | I | I | I |
| Review Documentation and Approval Recorded in Jira | I | C | I | I | **R/A** |
| Request / Identify PC2 Changes | I | C | I | I | **R/A** |
| Update PC2 Entry with Suggested Changes | **R/A** | C | I | I | C |
| Determine Governance Review Completion | I | I | I | I | **R/A** |
| Record Governance Approval in ITG Jira Subtask | I | I | I | I | **R/A** |
| Record Final Review Status in Parent Jira | I | **R/A** | I | I | I |
| Set `ar-complete` and Close Jira Tasks | I | **R/A** | I | I | I |

### Legend

- **R (Responsible):** Performs the work.
- **A (Accountable):** Owns the outcome or final decision.
- **C (Consulted):** Provides input to the activity or decision.
- **I (Informed):** Is kept informed of the activity or outcome.
- **R/A:** The same role is both Responsible and Accountable.

> **RACI Note:** Responsibility (`R`) is primarily derived from the BPMN swimlane in which an activity is performed. Accountability, consultation, and notification assignments reflect the interactions represented by the BPMN flow and should be validated by the applicable process owners before the RACI is formally adopted.

---

# Workflow States

The Architecture Review process tracks high-level workflow state through the Jira records.

The parent Architecture Review Jira task is supported by multiple subtasks. The number and type of subtasks can vary depending on whether the review requires SA escalation, Specialist/ODT consultation, and IT Governance activities.

## In Progress

Reviews that are actively being processed are tracked using:

`ar-in-progress`

The applicable Portfolio Review or SA Review is also explicitly set to **In Progress** at the appropriate point in the BPMN process.

## Complete

When all required review and governance activities have been completed, the APT Reviewer performs:

**Set ar-complete and Close Jira Tasks**

The completed review is tracked using:

`ar-complete`

The final review status is also recorded in the parent Jira task before the associated Jira tasks are closed.

---

# Process Completion Criteria

An Architecture Review is complete when all activities applicable to its review path have been completed.

Depending on the path taken through the process, this includes:

- Architecture Review Request submitted.
- Required supporting documentation provided.
- Portfolio Architecture Review completed.
- Portfolio Review findings recorded in Jira.
- Portfolio Review approval recorded, or SA escalation completed.
- SA Review completed when required.
- Specialist/ODT consultation completed when required.
- Required architecture changes addressed when applicable.
- SA Approval recorded when required.
- Tollgate Governance Record / PC2 Entry created.
- ITG subtask created.
- IT Governance notified.
- Governance Review completed.
- Governance Approval recorded in the ITG Jira subtask.
- Final review status recorded in the parent Jira.
- `ar-complete` set.
- Applicable Jira tasks closed.

Once these activities are complete, the process reaches:

**Architecture Review Completed**
