# Lab 1 — End-to-End Loan Approval Automation

## Objective
Build a synthetic loan-approval workflow demonstrating BPMN orchestration, DMN decisions, a Java/Spring Boot external worker, REST credit assessment, process variables, Tasklist review, Operate monitoring, and incident recovery.

## Architecture and execution flow
The process begins at `loanApprovalProcess`. A Tasklist application form captures synthetic applicant details. The `validate-applicant` Spring Boot worker checks required fields and publishes `validationResult` and `validationMessage`. An exclusive gateway rejects invalid submissions. Valid submissions call the mock `/api/credit-assessment` endpoint through the Camunda REST Connector. The response is mapped to `creditAssessment`; the `loanEligibilityDecision` DMN decision evaluates it along with income, loan amount, and employment status. A second gateway routes to approved, rejected, or manual-review paths. Manual review is completed in Tasklist and the reviewer selects an outcome.

## Decision rules
The `FIRST`-hit DMN rejects scores below 500 or monthly income below INR 20,000; approves strong and standard qualifying applications; and returns `MANUAL_REVIEW` for remaining borderline cases. These are illustrative educational rules, not lending advice or a real credit model.

## REST integration
The REST Connector posts synthetic applicant data to `http://localhost:8081/api/credit-assessment`. No authentication or real credit service is used. The mock API can return a successful assessment or intentional HTTP 503/504 failure for controlled incident tests.

## Worker implementation
The shared Java 21 / Spring Boot 3.5.3 project uses the Camunda 8.9 Spring Boot Starter. `validate-applicant` returns `VALID`/`INVALID` and an explanatory message. The test-only `simulateWorkerFailure` flag deliberately throws an exception to create a worker incident.

## Results and limitations
BPMN, DMN, worker source, form definitions, REST examples, process-variable dictionary, and a five-scenario test plan are included. **No claim is made that process instances have been deployed or executed in the user's Camunda instance.** Actual outcomes and screenshots must be added from Tasklist and Operate before final submission. Educational thresholds are assumptions documented for this practical.
