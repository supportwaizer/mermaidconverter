# Architecture Review --- Manual Tracking Process

## 1. Purpose

The Architecture Review process ensures that proposed solutions are
evaluated for architectural alignment, technical feasibility, compliance
with enterprise standards, operational/domain requirements, and IT
governance requirements before implementation proceeds.

The process provides a documented review and approval trail and defines
how requests are returned for remediation when issues are identified.

------------------------------------------------------------------------

## 2. Process Participants

### APT / Requestor

The APT / Requestor initiates the Architecture Review and is responsible
for:

-   Submitting the Architecture Review Request (ARR).
-   Providing required solution and architecture documentation.
-   Responding to requests for missing information.
-   Updating solution or architecture documentation when rework is
    required.
-   Creating the required PC2 governance tracking entry.

### Solution Architecture (SA)

Solution Architecture owns and coordinates the Architecture Review
process and is responsible for:

-   Creating and maintaining the Jira Architecture Review record.
-   Performing the readiness check.
-   Conducting the architecture review.
-   Identifying required Operational Domain Team (ODT) reviews.
-   Coordinating ODT reviews.
-   Recording review decisions.
-   Coordinating IT Governance review.
-   Managing re-review when changes are required.
-   Closing the Architecture Review after final approval.

### Operational Domain Team (ODT)

ODT performs domain-specific technical reviews when required and is
responsible for:

-   Reviewing the proposed solution within its area of responsibility.
-   Identifying technical concerns, requirements, or exceptions.
-   Approving the design or requesting rework.
-   Documenting its review decision.

Multiple ODT reviews may be required for a single Architecture Review.

### IT Governance (ITG)

IT Governance performs the final governance review and is responsible
for:

-   Reviewing the solution and associated Architecture Review decisions.
-   Identifying governance issues or required changes.
-   Determining whether the solution is approved.
-   Documenting final governance approval or rejection requirements.

------------------------------------------------------------------------

## 3. Process Overview

The Architecture Review consists of seven major phases:

1.  Intake
2.  Readiness Check
3.  Review Preparation
4.  Architecture and ODT Review
5.  Communication and Governance Tracking
6.  Governance Review and Rework
7.  Closure

------------------------------------------------------------------------

## 4. Detailed Process

### Phase 1 --- Intake

#### 4.1 Submit Architecture Review Request

**Owner:** APT / Requestor

The requestor submits an Architecture Review Request (ARR) using the
designated MS Form.

The request should contain sufficient information to identify the
proposed solution, scope of change, business context, and appropriate
contacts.

#### 4.2 Create Jira Architecture Review

**Owner:** Solution Architecture

SA creates the parent Jira item used to track the Architecture Review.

The Jira item represents the authoritative workflow record for the
review.

#### 4.3 Create APT Sub-task

**Owner:** Solution Architecture

SA creates an APT sub-task under the Architecture Review parent item to
track requestor activities and supporting documentation.

#### 4.4 Upload Supporting Documentation

**Owner:** APT / Requestor

The requestor uploads all required supporting documentation to the
designated shared repository and provides the appropriate link in the
Jira Architecture Review.

Supporting documentation may include:

-   Solution architecture diagrams
-   Integration diagrams
-   Data flows
-   Technology selections
-   Security information
-   Infrastructure or deployment architecture
-   Relevant patterns and standards
-   Architecture Decision Records (ADRs)
-   Other supporting design documentation

------------------------------------------------------------------------

### Phase 2 --- Readiness Check

#### 4.5 Review Submission

**Owner:** Solution Architecture

SA reviews the submitted request and supporting documentation to
determine whether sufficient information exists to conduct an
Architecture Review.

#### 4.6 Gateway --- Ready for Review?

**Decision Owner:** Solution Architecture

**If No:**

1.  SA identifies missing or incomplete information.
2.  The request is returned to APT / Requestor.
3.  APT updates the documentation or provides the requested information.
4.  The request returns to **Review Submission**.

This cycle continues until the submission is ready.

**If Yes:**

The process proceeds to Review Preparation.

------------------------------------------------------------------------

### Phase 3 --- Review Preparation

#### 4.7 Mark Review In Progress

**Owner:** Solution Architecture

SA updates the Architecture Review tracking item to indicate that formal
review has started.

Where Jira labels are used, the review is marked `ar-in-progress`.

#### 4.8 Schedule Architecture Review

**Owner:** Solution Architecture

SA schedules the Architecture Review with the appropriate stakeholders.

#### 4.9 Conduct Architecture Review

**Owner:** Solution Architecture

SA evaluates the proposed solution for alignment with enterprise
architecture principles, standards, patterns, technology direction, and
other applicable architectural requirements.

#### 4.10 Gateway --- ODT Review Required?

**Decision Owner:** Solution Architecture

SA determines whether one or more Operational Domain Team reviews are
required.

**If No:**

The process proceeds to communication and governance tracking.

**If Yes:**

SA identifies the required ODTs and creates the necessary ODT review
sub-tasks.

------------------------------------------------------------------------

### Phase 4 --- ODT Review

#### 4.11 Create Required ODT Sub-task(s)

**Owner:** Solution Architecture

SA creates one review sub-task for each required ODT.

When multiple ODTs are required, their reviews may be performed in
parallel.

#### 4.12 Conduct ODT Review

**Owner:** Operational Domain Team

Each identified ODT performs its domain-specific technical review.

#### 4.13 Gateway --- ODT Approved?

**Decision Owner:** ODT

**If Yes:**

1.  ODT documents its approval and decision.
2.  SA records the ODT decision in the parent Architecture Review.
3.  When multiple ODT reviews are required, all required approvals must
    be obtained before proceeding.

**If No:**

1.  ODT documents the issues and required changes.
2.  The solution is returned for remediation.
3.  APT updates the solution and supporting documentation.
4.  SA conducts the applicable architecture review again.
5.  Required ODT reviews are repeated.

The review cannot proceed to Governance until required ODT approvals
have been obtained.

------------------------------------------------------------------------

### Phase 5 --- Communication and Governance Tracking

#### 4.14 Notify APT of Architecture Review Results

**Owner:** Solution Architecture

SA communicates the Architecture Review results to APT / Requestor.

#### 4.15 Create PC2 Governance Tracking Entry

**Owner:** APT / Requestor

APT creates the required PC2 governance tracking entry.

#### 4.16 Create IT Governance Sub-task

**Owner:** Solution Architecture

SA creates the IT Governance sub-task and notifies the appropriate IT
Governance contact.

The process then proceeds to Governance Review.

------------------------------------------------------------------------

### Phase 6 --- Governance Review and Rework

#### 4.17 Conduct Governance Review

**Owner:** IT Governance

IT Governance evaluates the proposed solution and the results of the
Architecture and ODT reviews.

#### 4.18 Gateway --- Governance Approved?

**Decision Owner:** IT Governance

**If Yes:**

IT Governance documents final approval and the process proceeds toward
closure.

**If No:**

IT Governance documents the rejection, identified issues, and required
changes.

The process then evaluates the nature of the requested changes.

#### 4.19 Document Governance Rejection / Required Changes

**Owner:** IT Governance

The governance decision should clearly identify:

-   Reason for rejection
-   Required remediation
-   Applicable governance requirement
-   Whether the change affects the approved architecture or technical
    design

#### 4.20 Gateway --- Technical Re-review Required?

This gateway distinguishes a documentation/governance correction from a
material technical or architectural change.

##### No --- Documentation Only

When the requested correction does not materially change the approved
architecture:

1.  APT updates the required governance documentation.
2.  The corrected information is resubmitted to IT Governance.
3.  IT Governance repeats the Governance Review.
4.  No additional SA or ODT approval is required unless Governance
    determines that the correction introduces a material technical
    change.

Examples may include:

-   Missing governance documentation
-   Administrative corrections
-   Clarification of previously approved information
-   Missing references or evidence
-   Non-architectural governance requirements

##### Yes --- Material Technical or Architecture Change

When remediation changes the proposed solution or architecture:

1.  APT updates the solution and architecture documentation.
2.  The solution returns to Solution Architecture.
3.  SA performs the applicable Architecture Review again.
4.  SA determines whether ODT review is required.
5.  Applicable ODT reviews and approvals are repeated.
6.  The updated solution returns through the governance process.

Examples may include:

-   Changing an integration approach
-   Introducing a new technology
-   Changing security architecture
-   Changing data storage or data movement
-   Changing deployment architecture
-   Changing a system-of-record relationship
-   Introducing a new external dependency
-   Deviating from an approved enterprise pattern

This prevents minor governance corrections from unnecessarily restarting
the entire Architecture Review while ensuring material design changes
receive appropriate technical review.

------------------------------------------------------------------------

### Phase 7 --- Approval and Closure

#### 4.21 Document Final Governance Approval

**Owner:** IT Governance

IT Governance records final governance approval.

#### 4.22 Record Governance Decision

**Owner:** Solution Architecture

SA records the IT Governance decision in the parent Architecture Review
Jira item.

The decision and any associated approval evidence should be retained
with the review record.

#### 4.23 Complete Architecture Review

**Owner:** Solution Architecture

After all required approvals have been obtained, SA:

-   Confirms Architecture Review decisions are documented.
-   Confirms required ODT approvals are documented.
-   Confirms IT Governance approval is documented.
-   Changes the review status or label from `ar-in-progress` to
    `ar-complete`.
-   Closes the applicable Jira tasks and sub-tasks.

#### 4.24 End --- Architecture Review Complete

The Architecture Review is complete and the solution may proceed subject
to any conditions documented in the approval.

------------------------------------------------------------------------

## 5. Key Decision Points

  -----------------------------------------------------------------------
  Decision          Owner             Yes               No
  ----------------- ----------------- ----------------- -----------------
  Ready for Review? SA                Begin formal      Return to APT for
                                      review            missing
                                                        information

  ODT Review        SA                Create ODT        Proceed toward
  Required?                           review(s)         Governance

  ODT Approved?     ODT               Record approval   Remediate and
                                      and continue      repeat applicable
                                                        technical review

  Governance        IT Governance     Proceed to        Document
  Approved?                           closure           rejection and
                                                        determine
                                                        re-review
                                                        requirement

  Technical         SA / IT           Return to         Correct
  Re-review         Governance        Architecture      documentation and
  Required?                           Review            return directly
                                                        to Governance
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 6. Process Controls

The following controls should apply to the process:

-   The review must not proceed until the submission is considered
    ready.
-   Required ODT approvals must be obtained before Governance approval.
-   ODT and Governance decisions must be documented.
-   Material design changes introduced during remediation must be
    re-reviewed.
-   Documentation-only Governance corrections do not require a complete
    Architecture Review restart.
-   The Architecture Review cannot be closed until all required
    approvals are documented.
-   Jira serves as the workflow and decision tracking record.
-   Supporting architecture documentation should remain linked to the
    review record.

------------------------------------------------------------------------

## 7. Primary Process Records

The process produces or maintains the following records:

-   Architecture Review Request (ARR)
-   Parent Jira Architecture Review item
-   APT sub-task
-   Supporting architecture documentation
-   ODT review sub-task(s)
-   ODT decisions and approvals
-   Architecture Review decision
-   PC2 governance tracking entry
-   IT Governance sub-task
-   Governance decision and approval
-   Final closed Architecture Review record

------------------------------------------------------------------------

## 8. Process Flow Summary

``` text
Architecture Review Requested
        |
        v
Submit ARR
        |
        v
Create Jira Review + APT Sub-task
        |
        v
Upload Supporting Documentation
        |
        v
Review Submission
        |
        v
Ready for Review?
   | No                | Yes
   v                   v
Update Information   Conduct Architecture Review
   |                   |
   +-----> Recheck     v
                 ODT Review Required?
                    | No       | Yes
                    |          v
                    |     Conduct ODT Review(s)
                    |          |
                    |      ODT Approved?
                    |       |       |
                    |      No      Yes
                    |       |       |
                    |       v       v
                    |    Rework   Record Decision
                    |       |       |
                    |       +-------+
                    v
             Notify APT / Create PC2
                    |
                    v
              Governance Review
                    |
                    v
             Governance Approved?
                |            |
               Yes           No
                |            |
                |            v
                |    Document Required Changes
                |            |
                |            v
                |   Technical Re-review Required?
                |        |               |
                |       No              Yes
                |        |               |
                |        v               v
                |   Update Governance  Update Solution /
                |   Documentation      Architecture
                |        |               |
                |        v               v
                |   Governance Review  Architecture Review
                |                        |
                +------------------------+
                |
                v
       Document Final Approval
                |
                v
       Record Governance Decision
                |
                v
       Complete / Close Review
                |
                v
     Architecture Review Complete
```
