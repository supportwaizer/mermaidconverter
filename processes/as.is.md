# Federated Architecture Review Process

## 1. Purpose

The Federated Architecture Review Process defines the current process for reviewing proposed solutions and architecture changes.

The process distributes architecture review responsibilities across the following teams:

- **APT**
- **Solution Architecture (SA)**
- **ODT**
- **ITG**

The process uses a federated review model in which APT performs the initial review. Requests requiring additional architecture oversight are escalated to the Solution Architecture team.

Solution Architecture may engage ODT for additional advice during an escalated review.

Both the APT approval path and the Solution Architecture approval path ultimately converge on the ITG tollgate approval process.

---

# 2. Process Participants

| Participant | Responsibility |
|---|---|
| **APT** | Receives review requests, validates request documentation, conducts the initial review, determines whether Solution Architecture escalation is required, approves reviews that do not require escalation, and coordinates resubmission when Solution Architecture requests changes. |
| **Solution Architecture (SA)** | Reviews escalated requests, validates escalated-request documentation, conducts Solution Architecture review, determines whether ODT advice is required, and determines whether the architecture review can be approved. |
| **ODT** | Provides advice to Solution Architecture and APT when requested during an escalated architecture review. |
| **ITG** | Audits the completed architecture review and approves the applicable tollgate. |

---

# 3. Process Overview

The Federated Architecture Review Process follows the general flow below:

```text
Review Request Initiated
        |
        v
[APT] Submit Review Request
        |
        v
[APT] Validate Request Documentation
        |
        v
Ready for Review?
   |        |
  No       Yes
   |        |
   |        v
   |   Conduct Review
   |        |
   |        v
   |   Require Escalation?
   |       |       |
   |      No      Yes
   |       |       |
   |       v       v
   |    Approve   Escalate Review
   |    Review       to SA
   |       |           |
   |       |           v
   |       |    Validate Escalated
   |       |    Request Documentation
   |       |           |
   |       |           v
   |       |     Ready for Review?
   |       |        |       |
   |       |       No      Yes
   |       |        |       |
   |       |        |       v
   |       |        |   Conduct Escalated
   |       |        |   Request SA Review
   |       |        |       |
   |       |        |       v
   |       |        |   Require ODT Advice?
   |       |        |      |         |
   |       |        |     Yes       No
   |       |        |      |         |
   |       |        |      v         |
   |       |        |   ODT Advises  |
   |       |        |   SA and APT   |
   |       |        |      |         |
   |       |        |      +-----> Conduct
   |       |        |               SA Review
   |       |        |                  |
   |       |        |                  v
   |       |        |          Review Approved?
   |       |        |             |        |
   |       |        |            No       Yes
   |       |        |             |        |
   |       |        |             |        v
   |       |        |             |    Notify APT
   |       |        |             |    and ODT(s)
   |       |        |             |
   |       |        +-------------+
   |       |              Revise
   |       |          Documentation
   |       |
   |       v
   |   Notify SA
   |   and ODT(s)
   |
   +<------ SA Review Not Approved
            with Suggested Changes
            |
            v
      Resubmit Review Request
            |
            v
      Portfolio Review Repeats

Approved paths
        |
        v
[ITG] Audit and Approve Tollgate
        |
        v
Review Completed
```

---

# 4. APT Portfolio Review Process

## 4.1 Review Request Initiated

The process begins when a review request is initiated.

The request enters the APT review process.

---

## 4.2 Step 1 — Submit Review Request

**Owner:** APT

APT submits or receives the review request for processing.

The request contains the information and supporting documentation required to begin the architecture review process.

**Output:** Review request submitted.

---

## 4.3 Step 2 — Validate Request Documentation

**Owner:** APT

APT validates the documentation associated with the review request.

The objective of this activity is to determine whether sufficient information has been provided to allow the review to proceed.

**Output:** Request documentation validated.

---

## 4.4 Step 3 — Ready for Review?

**Owner:** APT  
**Type:** Decision Gateway

APT determines whether the request contains sufficient information to conduct the review.

### No — Revise Documentation

If the request is not ready for review, the request is returned for documentation revisions.

Once the required documentation has been revised, the request is resubmitted through:

**Step 1 — Submit Review Request**

The documentation is then validated again.

### Yes

If the request is ready for review, the process proceeds to:

**Step 4 — Conduct Review**

---

## 4.5 Step 4 — Conduct Review

**Owner:** APT

APT conducts the initial architecture review using the submitted request and supporting documentation.

Following the review, APT determines whether the request can be approved through the federated APT review process or requires escalation to Solution Architecture.

**Output:** Initial architecture review completed.

---

## 4.6 Step 5 — Require Escalation?

**Owner:** APT  
**Type:** Decision Gateway

APT determines whether the review requires escalation to the Solution Architecture team.

### No

If Solution Architecture escalation is not required, the process proceeds to:

**Step 7 — Approve Review**

### Yes

If Solution Architecture review is required, the process proceeds to:

**Step 6 — Escalate Review to SA**

---

## 4.7 Step 6 — Escalate Review to SA

**Owner:** APT

APT escalates the review request to the Solution Architecture team.

The escalated request enters the Solution Architecture Review portion of the Federated Architecture Review Process.

**Output:** Request escalated to Solution Architecture.

---

## 4.8 Step 7 — Approve Review

**Owner:** APT

When Solution Architecture escalation is not required, APT approves the architecture review.

The approved review then proceeds to stakeholder notification.

**Output:** APT review approved.

---

## 4.9 Step 8 — Notify SA and ODT(s)

**Owner:** APT

APT notifies the appropriate Solution Architecture and ODT stakeholders that the review has been approved.

Following notification, the request proceeds to the ITG tollgate process.

**Output:** SA and applicable ODT stakeholders notified.

---

# 5. Escalated Solution Architecture Review Process

## 5.1 Entry into Solution Architecture Review

The Solution Architecture Review Process begins when APT determines that a request requires escalation.

The request enters this process through:

**Step 6 — Escalate Review to SA**

---

## 5.2 Step 6a — Validate Escalated Request Documentation

**Owner:** Solution Architecture

Solution Architecture validates the documentation associated with the escalated request.

The objective is to determine whether sufficient information exists to conduct the Solution Architecture review.

**Output:** Escalated request documentation validated.

---

## 5.3 Step 6b — Ready for Review?

**Owner:** Solution Architecture  
**Type:** Decision Gateway

Solution Architecture determines whether the escalated request contains sufficient information to proceed with the review.

### No — Revise Documentation

If the escalated request is not ready for review, documentation revisions are required.

The request is returned through the escalation path so that the required documentation can be updated.

Once the documentation has been revised, the request is again escalated to Solution Architecture and re-enters:

**Step 6a — Validate Escalated Request Documentation**

This cycle continues until the request is ready for Solution Architecture review.

### Yes

If the request is ready for review, the process proceeds to:

**Step 6c — Conduct Escalated Request SA Review**

---

## 5.4 Step 6c — Conduct Escalated Request SA Review

**Owner:** Solution Architecture

Solution Architecture conducts the detailed architecture review of the escalated request.

During the review, Solution Architecture determines whether input from the appropriate ODT is required.

**Output:** Solution Architecture review performed.

---

## 5.5 Step 6d — Require ODT Advice?

**Owner:** Solution Architecture  
**Type:** Decision Gateway

Solution Architecture determines whether additional advice from an ODT is required.

### Yes

If ODT advice is required, the review proceeds to:

**ODT Advises SA and APT on Review**

### No

If ODT advice is not required, the review proceeds to:

**Step 6e — Review Approved?**

---

# 6. ODT Review Participation

## 6.1 ODT Advises SA and APT on Review

**Owner:** ODT

When requested by Solution Architecture, the appropriate ODT reviews the relevant aspects of the request and provides advice to both:

- Solution Architecture
- APT

Following receipt of ODT advice, the request returns to:

**Step 6c — Conduct Escalated Request SA Review**

Solution Architecture considers the ODT advice as part of the continuing architecture review.

**Output:** ODT advice provided to SA and APT.

---

# 7. Solution Architecture Approval

## 7.1 Step 6e — Review Approved?

**Owner:** Solution Architecture  
**Type:** Decision Gateway

Following the Solution Architecture review, SA determines whether the request can be approved.

### Yes

If the architecture review is approved, the process proceeds to:

**Step 8a — Notify APT and ODT(s)**

### No — With Suggested Changes

If the architecture review is not approved, Solution Architecture returns the request with suggested changes.

The request returns to the APT submission process.

The process re-enters at:

**Step 1 — Submit Review Request**

The revised request then proceeds again through:

```text
Submit Review Request
        |
        v
Validate Request Documentation
        |
        v
Ready for Review?
        |
        v
Conduct Review
        |
        v
Require Escalation?
```

If escalation is again required, the revised request is resubmitted to Solution Architecture through the normal escalation path.

This creates an iterative review cycle until the request is either approved through the APT process or approved through the Solution Architecture review process.

---

## 7.2 Step 8a — Notify APT and ODT(s)

**Owner:** Solution Architecture

After Solution Architecture approves the review, SA notifies:

- APT
- Applicable ODT stakeholder(s)

The approved review then proceeds to ITG.

**Output:** APT and ODT stakeholders notified of SA approval.

---

# 8. ITG Tollgate Approval

## 8.1 Step 9 — Audit and Approve Tollgate

**Owner:** ITG

Both architecture approval paths converge at the ITG tollgate.

Requests may reach ITG through either of the following paths:

### APT Approval Path

```text
APT Conduct Review
        |
        v
No Escalation Required
        |
        v
APT Approve Review
        |
        v
Notify SA and ODT(s)
        |
        v
ITG Audit and Approve Tollgate
```

### Solution Architecture Approval Path

```text
APT Conduct Review
        |
        v
Escalation Required
        |
        v
Solution Architecture Review
        |
        v
SA Review Approved
        |
        v
Notify APT and ODT(s)
        |
        v
ITG Audit and Approve Tollgate
```

ITG audits the completed review and approves the applicable tollgate.

**Output:** Tollgate approved.

---

# 9. Review Completed

Following ITG approval of the tollgate, the Federated Architecture Review is considered complete.

```text
ITG Audit and Approve Tollgate
              |
              v
       Review Completed
```

---

# 10. Decision Summary

| Decision | Owner | Yes | No |
|---|---|---|---|
| **Ready for Review?** | APT | Conduct Review | Revise documentation and resubmit review request |
| **Require Escalation?** | APT | Escalate Review to SA | Approve Review |
| **Ready for Review? — Escalated Request** | SA | Conduct Escalated Request SA Review | Revise documentation and return through escalation path |
| **Require ODT Advice?** | SA | Obtain ODT advice and continue SA review | Proceed to approval decision |
| **Review Approved?** | SA | Notify APT and ODT(s) and proceed to ITG | Return to APT with suggested changes and restart review cycle |

---

# 11. Responsibility Matrix

| Process Activity | APT | SA | ODT | ITG |
|---|:---:|:---:|:---:|:---:|
| Initiate/submit review request | X | | | |
| Validate initial request documentation | X | | | |
| Determine initial review readiness | X | | | |
| Conduct initial review | X | | | |
| Determine whether escalation is required | X | | | |
| Approve non-escalated review | X | | | |
| Escalate review to Solution Architecture | X | | | |
| Validate escalated-request documentation | | X | | |
| Determine escalated-request readiness | | X | | |
| Conduct escalated Solution Architecture review | | X | | |
| Determine whether ODT advice is required | | X | | |
| Provide review advice | | | X | |
| Determine whether SA review is approved | | X | | |
| Return suggested changes for an unapproved SA review | | X | | |
| Revise/resubmit request following SA feedback | X | | | |
| Notify SA and ODT after APT approval | X | | | |
| Notify APT and ODT after SA approval | | X | | |
| Audit completed architecture review | | | | X |
| Approve tollgate | | | | X |

---

# 12. Primary Review Paths

The process supports three significant execution paths.

## 12.1 Federated APT Approval Path

A request that does not require Solution Architecture escalation follows:

```text
Review Request Initiated
        ->
Submit Review Request
        ->
Validate Request Documentation
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
ITG Audit and Approve Tollgate
        ->
Review Completed
```

---

## 12.2 Escalated Solution Architecture Approval Path

A request requiring Solution Architecture review follows:

```text
Review Request Initiated
        ->
Submit Review Request
        ->
Validate Request Documentation
        ->
Ready for Review
        ->
Conduct Review
        ->
Escalation Required
        ->
Escalate Review to SA
        ->
Validate Escalated Request Documentation
        ->
Ready for Review
        ->
Conduct Escalated Request SA Review
        ->
Obtain ODT Advice if Required
        ->
Review Approved
        ->
Notify APT and ODT(s)
        ->
ITG Audit and Approve Tollgate
        ->
Review Completed
```

---

## 12.3 Solution Architecture Rework Path

When Solution Architecture does not approve a review, it returns the request with suggested changes.

```text
Conduct Escalated Request SA Review
        ->
Review Approved?
        ->
No — Suggested Changes
        ->
Return to APT
        ->
Submit Revised Review Request
        ->
Validate Request Documentation
        ->
Conduct Review
        ->
Determine Escalation
        ->
Continue Appropriate Review Path
```

The review therefore remains iterative until an approval path is successfully completed.

---

# 13. Documentation Revision Paths

The process contains two separate documentation-revision loops.

## 13.1 APT Documentation Revision

When APT determines that the initial request is not ready for review:

```text
Validate Request Documentation
        ->
Ready for Review? = No
        ->
Revise Documentation
        ->
Submit Review Request
        ->
Validate Request Documentation
```

---

## 13.2 Escalated Request Documentation Revision

When Solution Architecture determines that an escalated request is not ready:

```text
Validate Escalated Request Documentation
        ->
Ready for Review? = No
        ->
Revise Documentation
        ->
Escalate Review to SA
        ->
Validate Escalated Request Documentation
```

---

# 14. Process Completion Criteria

A Federated Architecture Review is complete when:

1. The architecture review has been approved through either the APT or Solution Architecture review path.
2. Required stakeholder notifications have been completed.
3. ITG has audited the completed review.
4. ITG has approved the applicable tollgate.

The final state of the process is:

**Review Completed**

---

# 15. Process Summary

The Federated Architecture Review Process provides two levels of architecture review.

APT owns the initial review and determines whether the request can be approved through the federated review process or requires escalation to Solution Architecture.

If escalation is required, Solution Architecture validates the escalated request and conducts a detailed architecture review. Solution Architecture may obtain advice from the appropriate ODT and incorporate that advice into its review.

If Solution Architecture does not approve the request, the request is returned to APT with suggested changes and re-enters the review process after revision.

If either APT or Solution Architecture approves the review, the appropriate stakeholders are notified and the request proceeds to ITG.

ITG performs the final audit and approves the applicable tollgate.

ITG tollgate approval marks completion of the Federated Architecture Review Process.
