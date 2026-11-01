# PBJ-2 Practical Assignment — Camunda 8 End-to-End Workflow Automation

This repository contains separate workflow implementations for all three labs in the supplied PBJ-2 assignment brief. It targets the local Camunda 8.9 / Modeler 5.50.1 environment and Java 21.

## Repository contents

- `Lab1_Loan_Approval/` — Loan Approval BPMN and DMN, two Tasklist forms, decision sample evaluations, report, variable dictionary, test plan, evidence instructions, and REST examples (shared examples are under `shared/mock-api/examples`).
- `Lab2_ECommerce/` — E-Commerce BPMN and priority DMN, Tasklist forms, decision sample evaluations, report, variable dictionary, test plan, and evidence instructions.
- `Lab3_Hospital_Triage/` — Hospital Appointment/Triage BPMN and DMN, Tasklist forms, decision sample evaluations, report, variable dictionary, test plan, and evidence instructions.
- `shared/` — one Java/Spring Boot external-worker application serving all job types (including Lab 3 scheduling availability pre-check) and a synthetic REST API for all labs.
- `scripts/` — PowerShell scripts to start the mock service, run the workers, create process instances, and check local endpoints.

## Assignment coverage

The repository is organized into three independent implementations matching the supplied PBJ-2 brief. Each lab has a BPMN process, DMN decision table, linked Tasklist forms, Spring Boot job workers, REST integration, process-variable dictionary, sample decision evaluations, five or more test scenarios, evidence checklist, and implementation report. See `COMPLIANCE_MATRIX.md` for a requirement-by-requirement map.

## Important submission truth

The assignment explicitly requires screenshots captured from the student's own running implementation and prohibits placeholder evidence. Therefore this repository deliberately does **not** contain fake Tasklist/Operate screenshots or claim that local process instances have been executed. The three `evidence/README.md` files specify the genuine screenshots to capture. The test tables currently say “Pending live run”; update them with actual results from your Camunda environment before handing in the submission.

## Prerequisites

- Camunda 8.9 self-managed / Camunda 8 Run started locally (Orchestration Cluster REST API at `http://localhost:8080`).
- Camunda Modeler 5.50.1 or compatible 8.9 modeler.
- Java 21.
- Maven 3.9+.
- Python 3.10+ (standard library only).
- Camunda Connectors runtime with the REST connector enabled and connected to the same Camunda 8.9 cluster.

## Run locally (three terminals)

1. Start Camunda 8 Run and keep its terminal running. Confirm `http://localhost:8080` is reachable.
2. Open a PowerShell terminal at this repository and run `powershell -ExecutionPolicy Bypass -File .\scripts\Run-MockApi.ps1`. Leave it running. Check `http://localhost:8081/health`.
3. Open a second PowerShell terminal and run `powershell -ExecutionPolicy Bypass -File .\scripts\Run-Worker.ps1`. Leave it running. The worker connects outbound to the Camunda REST API at port 8080; it does not need to expose a separate HTTP health port.

## Deploy the models

For **each lab**, open its `.bpmn` and `.dmn` file in Camunda Modeler and deploy both to the same running Camunda 8.9 cluster. Also deploy every `.form` file referenced by that lab's BPMN (use Modeler's form deployment / deployment resource selection so the form IDs resolve). Verify successful deployment in the Modeler output and in Operate. Keep the BPMN process ID and the DMN decision ID unchanged; they are referenced by scripts and business-rule tasks.

The REST Connector tasks are configured as `io.camunda:connector-rest` with `noAuth`, POST, JSON payload, timeouts, and result expressions. In Lab 3, the Java worker also performs a scheduling availability pre-check, followed by the REST Connector call whose response drives the gateway. The connector runtime must be running and must be able to reach `http://localhost:8081`. In a containerized deployment, `localhost` may refer to the connector container rather than the Windows host; use the host-reachable address in all three BPMNs if necessary.

## Tasklist assignment groups

The BPMN files use the candidate-group IDs `loan-officers`, `order-operators`, `order-reviewers`, `registration-staff`, `clinical-reviewers`, and `scheduling-staff`. For a secured Camunda environment, create these groups in the Identity provider and add the Tasklist users who should work the tasks. If your local Camunda 8 Run instance uses a different identity setup, replace the candidate-group IDs with IDs that exist in that environment before deployment. This keeps the human tasks explicitly assignable instead of assuming identity groups are pre-created.

## Start a workflow instance

From the repository root, use one command after deploying the matching lab:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Start-ProcessInstance.ps1 -Lab lab1
powershell -ExecutionPolicy Bypass -File .\scripts\Start-ProcessInstance.ps1 -Lab lab2
powershell -ExecutionPolicy Bypass -File .\scripts\Start-ProcessInstance.ps1 -Lab lab3
```

Open Tasklist at `http://localhost:8080/tasklist` and complete the first user task. Follow the Tasklist forms and complete any review tasks with the values described in each lab's `TEST_CASES.md`. Open Operate at `http://localhost:8080/operate` to inspect variables, element states, incidents, and retries.

## Incident and recovery demonstrations

- Worker failure: set a lab's `simulateWorkerFailure` to true (or Lab 2 `simulateInventoryFailure`) in its intake form. Let worker retries exhaust until Operate shows an incident. Correct the variable to false using the variable update operation supported by your local 8.9 deployment, then retry the failed job/instance where supported.
- REST failure: set `simulateApiFailure`, `simulatePaymentFailure`, or `simulateSchedulingFailure` to true. The mock API returns HTTP 503. Correct the variable to false and retry the failed connector job in Operate.
- Timeout testing is supported by the mock credit API's `simulateTimeout` property, but the standard form uses the failure flag for a quicker demonstration.

Take screenshots before and after correction/retry. Exact menu names may vary between Tasklist/Operate builds.

## Validate package and run mock API tests

Run the static BPMN/DMN/form checks, then the mock API tests:

```powershell
python .\scripts\Validate-Package.py
python -m unittest discover -s .\shared\mock-api\tests -v
```

These tests verify the mock API endpoint contracts only. They do not substitute for Camunda model deployment or process execution evidence.

## Suggested GitHub upload

Create a new GitHub repository, extract this ZIP, and upload/push the complete `PBJ2_FINAL_SUBMISSION` folder contents (the files inside the root folder, not a nested ZIP). Do not commit real credentials or real patient data. Add genuine screenshots to each `evidence/` folder and update the test execution tables before giving the repository link to the instructor.

## Model conventions and safety

All sample applicants, customers, payments, patient references, and appointments are synthetic. Payment tokens are mock tokens only. Lab 3 decision rules are educational workflow examples only and are not clinical triage guidance or suitable for real patient care.
