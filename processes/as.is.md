# Federated Architecture Review Process

## 1. Purpose

The Federated Architecture Review Process defines the current process for reviewing proposed solutions and architecture changes.

The process distributes architecture review responsibilities across the **APT**, **Solution Architecture (SA)**, **ODT**, and **ITG** teams.

The process consists of two related review workflows:

1. **Portfolio Review Process**
2. **Solution Architecture Review Process**

The Portfolio Review Process serves as the initial review path. Requests requiring additional architectural review are escalated to the Solution Architecture Review Process.

Both review paths ultimately proceed through the ITG tollgate approval process.

---

## 2. Process Participants

| Participant | Role in the Review Process |
|---|---|
| **APT** | Receives and performs Portfolio Reviews, validates submitted documentation, determines review readiness, conducts the initial review, determines whether escalation is required, and coordinates completion of non-escalated reviews. |
| **SA – Solution Architecture** | Performs Solution Architecture Reviews for requests that are submitted or escalated to Solution Architecture. SA validates documentation, conducts the architecture review, determines whether ODT advice is required, and determines whether the review can be approved. |
| **ODT** | Provides advice to SA and APT when requested as part of a Solution Architecture Review. |
| **ITG** | Performs the final audit and approves the applicable tollgate after completion of the architecture review. |

---

# 3. Portfolio Review Process

## 3.1 Overview

The Portfolio Review Process is the initial architecture review path.

APT evaluates the submitted request and determines whether the review can be completed within the Portfolio Review Process or requires escalation to the Solution Architecture team.

The high-level process is:

```text
Submit Review Request
        |
        v
Validate Request Documentation
        |
        v
  Ready for Review?
     /        \
   No          Yes
   |            |
   |            v
   |      Conduct Review
   |            |
   |            v
   |    Require Escalation?
   |        /        \
   |      No          Yes
   |      |            |
   |      v            v
   |  Approve      Escalate Review
   |  Review          to SA
   |      |
   |      v
   |  Notify SA
   |  and ODT(s)
   |      |
   +------+
          |
          v
   Audit and Approve
        Tollgate
          |
          v
    Review Completed
```

---

## 3.2 Step 1 — Submit Review Request

**Owner:** APT

A review request is submitted to initiate the Portfolio Review Process.

The submitted request provides the information and supporting documentation necessary for the architecture review.

**Output:** Review request submitted.

---

## 3.3 Step 2 — Validate Request Documentation

**Owner:** APT

APT validates the documentation included with the review request.

The purpose of this step is to determine whether sufficient information has been provided to allow the architecture review to proceed.

**Output:** Documentation validated for review readiness.

---

## 3.4 Step 3 — Ready for Review?

**Owner:** APT  
**Type:** Decision

APT determines whether the submitted request contains sufficient information to begin the review.

### No

If the request is not ready for review, the documentation must be revised.

The request is returned for documentation updates and subsequently re-enters the validation process.

### Yes

If the request is ready for review, the process proceeds to:

**Step 4 — Conduct Review**

---

## 3.5 Step 4 — Conduct Review

**Owner:** APT

APT conducts the Portfolio Review using the submitted request and supporting documentation.

Following completion of the review, APT determines whether the request can continue through the Portfolio Review approval path or whether Solution Architecture involvement is required.

**Output:** Portfolio Review performed.

---

## 3.6 Step 5 — Require Escalation?

**Owner:** APT  
**Type:** Decision

APT determines whether the review requires escalation to the Solution Architecture team.

### No

If escalation is not required, the request proceeds to:

**Step 7 — Approve Review**

### Yes

If escalation is required, the request proceeds to:

**Step 6 — Escalate Review to SA**

The request then enters the **Solution Architecture Review Process**.

---

## 3.7 Step 6 — Escalate Review to SA

**Owner:** SA

The review request is escalated from the Portfolio Review Process to the Solution Architecture team.

The request becomes an input to the Solution Architecture Review Process described in Section 4.

**Output:** Request transferred to Solution Architecture Review.

---

## 3.8 Step 7 — Approve Review

**Owner:** APT

If Solution Architecture escalation is not required, APT approves the Portfolio Review.

**Output:** Portfolio Review approved.

---

## 3.9 Step 8 — Notify SA and ODT(s)

**Owner:** APT

Following approval of the Portfolio Review, APT notifies the appropriate Solution Architecture and ODT stakeholders.

**Output:** Relevant stakeholders notified of the review disposition.

---

## 3.10 Step 9 — Audit and Approve Tollgate

**Owner:** ITG

ITG audits the completed review and approves the applicable tollgate.

Following tollgate approval, the review is considered complete.

**Output:** Tollgate approved and review completed.

---

# 4. Solution Architecture Review Process

## 4.1 Overview

The Solution Architecture Review Process is used when a review request is submitted or escalated to the Solution Architecture team.

This process provides an additional level of architectural review and allows the Solution Architect to obtain ODT advice when necessary.

The high-level process is:

```text
Submitted or Escalated
    Review Request
          |
          v
Validate Request Documentation
          |
          v
    Ready for Review?
       /        \
     No          Yes
     |            |
     |            v
     |      Conduct Review
     |            |
     |            v
     |    Require ODT Advice?
     |        /        \
     |      Yes         No
     |       |           |
     |       v           |
     |   ODT Advises     |
     |   SA and APT      |
     |       |           |
     |       +-----------+
     |            |
     |            v
     |      Conduct Review
     |            |
     |            v
     |     Review Approved?
     |        /        \
     |      No          Yes
     |       |           |
     |       |           v
     |       |      Notify APT
     |       |      and ODT(s)
     |       |           |
     |       +--> Conduct|
     |            Review |
     |                  |
     +------------------+
                        |
                        v
                Audit and Approve
                     Tollgate
                        |
                        v
                 Review Completed
```

---

## 4.2 Step 1 — Submitted or Escalated Review Request

**Owner:** APT

The Solution Architecture Review Process begins when a review request is submitted or escalated for Solution Architecture review.

An escalated request may originate from the Portfolio Review Process.

**Output:** Review request received for Solution Architecture review.

---

## 4.3 Step 2 — Validate Request Documentation

**Owner:** SA

The Solution Architect validates the documentation associated with the request.

The objective is to determine whether sufficient documentation exists to conduct the Solution Architecture Review.

**Output:** Documentation validated for Solution Architecture review.

---

## 4.4 Step 3 — Ready for Review?

**Owner:** SA  
**Type:** Decision

The Solution Architect determines whether the request contains sufficient information to begin the architecture review.

### No

If the request is not ready for review, the documentation must be revised.

The request is returned for documentation updates and subsequently re-enters the validation process.

### Yes

If the request is ready for review, the process proceeds to:

**Step 4 — Conduct Review**

---

## 4.5 Step 4 — Conduct Review

**Owner:** SA

The Solution Architect conducts the architecture review using the submitted solution information and supporting documentation.

During the review, the Solution Architect may determine that additional advice from the appropriate ODT is necessary.

**Output:** Solution Architecture Review performed.

---

## 4.6 Step 5 — Require ODT Advice?

**Owner:** SA  
**Type:** Decision

The Solution Architect determines whether ODT input or advice is required to continue or complete the review.

### No

If ODT advice is not required, the process proceeds to:

**Step 7 — Review Approved?**

### Yes

If ODT advice is required, the process proceeds to:

**Step 6 — Advise SA and APT on Review**

---

## 4.7 Step 6 — Advise SA and APT on Review

**Owner:** ODT

The appropriate ODT reviews the relevant aspects of the proposed solution and provides advice to SA and APT.

After ODT advice has been provided, the review returns to the Solution Architect for continued review.

The process returns to:

**Step 4 — Conduct Review**

**Output:** ODT advice provided to SA and APT.

---

## 4.8 Step 7 — Review Approved?

**Owner:** SA  
**Type:** Decision

The Solution Architect determines whether the architecture review can be approved.

### No

If the review cannot be approved, the process returns to:

**Step 4 — Conduct Review**

The review continues until the outstanding issues are addressed and the request can again be evaluated for approval.

### Yes

If the review is approved, the process proceeds to:

**Step 8 — Notify APT and ODT(s)**

---

## 4.9 Step 8 — Notify APT and ODT(s)

**Owner:** SA

Following approval of the Solution Architecture Review, the Solution Architect notifies APT and the appropriate ODT stakeholders.

**Output:** Relevant stakeholders notified of the approved Solution Architecture Review.

---

## 4.10 Step 9 — Audit and Approve Tollgate

**Owner:** ITG

ITG audits the completed Solution Architecture Review and approves the applicable tollgate.

Following tollgate approval, the review is considered complete.

**Output:** Tollgate approved and review completed.

---

# 5. Combined Federated Architecture Review Flow

The Portfolio Review Process and Solution Architecture Review Process together constitute the current Federated Architecture Review model.

```text
                         FEDERATED ARCHITECTURE REVIEW
                                      |
                                      v
                   +----------------------------------+
                   |     PORTFOLIO REVIEW PROCESS     |
                   +----------------------------------+
                                      |
                                      v
                           Submit Review Request
                                      |
                                      v
                       Validate Request Documentation
                                      |
                                      v
                          +---------------------+
                          |  Ready for Review?  |
                          +---------------------+
                              /             \
                            No               Yes
                            |                 |
                            |                 v
                            |          Conduct Review
                            |                 |
                            |                 v
                            |      +---------------------+
                            |      | Require Escalation? |
                            |      +---------------------+
                            |          /             \
                            |        No               Yes
                            |        |                 |
                            |        v                 v
                            |   Approve Review    Escalate to SA
                            |        |                 |
                            |        v                 |
                            |  Notify SA and           |
                            |     ODT(s)               |
                            |        |                 |
                            |        |                 v
                            |        |   +----------------------------------+
                            |        |   | SOLUTION ARCHITECTURE REVIEW     |
                            |        |   |            PROCESS               |
                            |        |   +----------------------------------+
                            |        |                 |
                            |        |                 v
                            |        |       Validate Request Documentation
                            |        |                 |
                            |        |                 v
                            |        |        +--------------------+
                            |        |        | Ready for Review?  |
                            |        |        +--------------------+
                            |        |            /          \
                            |        |          No            Yes
                            |        |          |              |
                            |        |          |              v
                            |        |          |       Conduct Review
                            |        |          |              |
                            |        |          |              v
                            |        |          |   +----------------------+
                            |        |          |   | Require ODT Advice?  |
                            |        |          |   +----------------------+
                            |        |          |       /             \
                            |        |          |     Yes              No
                            |        |          |      |                |
                            |        |          |      v                |
                            |        |          | ODT Advises SA        |
                            |        |          |    and APT            |
                            |        |          |      |                |
                            |        |          |      +-----> Conduct Review
                            |        |          |                     |
                            |        |          |                     v
                            |        |          |           +------------------+
                            |        |          |           | Review Approved? |
                            |        |          |           +------------------+
                            |        |          |              /          \
                            |        |          |            No            Yes
                            |        |          |            |              |
                            |        |          |            +----->        v
                            |        |          |              Conduct   Notify APT
                            |        |          |               Review   and ODT(s)
                            |        |          |                            |
                            |        |          +----------------------------+
                            |        |                                       |
                            +--------+---------------------------------------+
                                     |
                                     v
                           +-------------------------+
                           |           ITG           |
                           | Audit and Approve       |
                           | Tollgate                |
                           +-------------------------+
                                     |
                                     v
                              REVIEW COMPLETED
```

---

# 6. Responsibility Matrix

| Process Activity | APT | SA | ODT | ITG |
|---|:---:|:---:|:---:|:---:|
| Submit/receive Portfolio Review request | X | | | |
| Validate Portfolio Review documentation | X | | | |
| Determine Portfolio Review readiness | X | | | |
| Conduct Portfolio Review | X | | | |
| Determine need for SA escalation | X | | | |
| Escalate review to Solution Architecture | X | X | | |
| Receive submitted/escalated SA Review | X | X | | |
| Validate Solution Architecture Review documentation | | X | | |
| Determine SA Review readiness | | X | | |
| Conduct Solution Architecture Review | | X | | |
| Determine whether ODT advice is required | | X | | |
| Provide review advice | | | X | |
| Determine whether SA Review is approved | | X | | |
| Approve non-escalated Portfolio Review | X | | | |
| Notify SA and ODT following Portfolio Review | X | | | |
| Notify APT and ODT following SA Review | | X | | |
| Audit completed review | | | | X |
| Approve tollgate | | | | X |

---

# 7. Review Paths

The Federated Architecture Review Process supports two primary paths.

## 7.1 Portfolio Review Path

A request that can be completed without Solution Architecture escalation follows this path:

```text
Submit Request
    ->
Validate Documentation
    ->
Ready for Review
    ->
Conduct Review
    ->
No Escalation Required
    ->
Approve Review
    ->
Notify SA and ODT(s)
    ->
ITG Audit and Tollgate Approval
    ->
Review Completed
```

## 7.2 Escalated Solution Architecture Review Path

A request requiring Solution Architecture involvement follows this path:

```text
Submit Request
    ->
Validate Documentation
    ->
Portfolio Review
    ->
Escalation Required
    ->
Solution Architecture Review
    ->
Validate Documentation
    ->
Ready for Review
    ->
Conduct Review
    ->
ODT Advice, if Required
    ->
Review Approval
    ->
Notify APT and ODT(s)
    ->
ITG Audit and Tollgate Approval
    ->
Review Completed
```

---

# 8. Review Outcomes

A review concludes when the appropriate architecture review process has been completed and the applicable ITG tollgate has been audited and approved.

A review may therefore reach completion through either of the following routes:

**Portfolio Review Approval**

```text
APT Review
    ->
APT Approval
    ->
Stakeholder Notification
    ->
ITG Tollgate Approval
    ->
Review Completed
```

**Solution Architecture Review Approval**

```text
APT Review
    ->
Escalation
    ->
SA Review
    ->
SA Approval
    ->
Stakeholder Notification
    ->
ITG Tollgate Approval
    ->
Review Completed
```

---

# 9. Process Summary

The current Federated Architecture Review Process establishes a tiered architecture review model.

APT provides the initial Portfolio Review and determines whether the request requires additional Solution Architecture involvement.

Requests that do not require escalation can be approved through the Portfolio Review Process.

Requests requiring additional architecture review are escalated to the Solution Architecture team. The Solution Architect conducts the review and may seek advice from the appropriate ODT where necessary.

After the applicable architecture review is approved, relevant stakeholders are notified and ITG performs the final audit and tollgate approval.

Completion of the ITG tollgate approval marks completion of the architecture review process.
