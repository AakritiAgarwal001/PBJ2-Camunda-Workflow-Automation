# Lab 3 — End-to-End Hospital Appointment and Patient Triage Management

## Objective
Model an educational appointment workflow using synthetic patient references, DMN urgency rules, Java/Spring Boot validation, mock REST scheduling, Tasklist staff review, and Operate monitoring/recovery.

## Architecture and execution flow
A Tasklist registration form captures a synthetic patient reference, appointment preference, symptoms summary, red-flag boolean, and an urgency indicator. The Java `validate-registration` worker checks required fields. An exclusive gateway rejects invalid registration. The `triageDecision` DMN classifies the request as ROUTINE, PRIORITY_REVIEW, or URGENT_ASSESSMENT. For routine and staff-approved priority requests, the Java `check-appointment-availability` worker first calls the mock scheduling API and stores pre-check availability/slots. The BPMN REST Connector then independently calls the same scheduling endpoint and its response controls the availability gateway. Urgent cases are sent directly to an immediate staff assessment task. Priority cases are sent to a staff review task; staff may proceed to scheduling or escalate/defer. Routine and staff-approved priority requests call the mock scheduling REST API. If slots exist, Tasklist captures a selected slot and a second REST call books it. No-slot and booking-exception cases return to staff review.

## Educational triage assumptions
A red-flag input is mapped to URGENT_ASSESSMENT; HIGH and MEDIUM indicators are mapped to PRIORITY_REVIEW; remaining requests are ROUTINE. These rules are solely illustrative for the assignment and must never be interpreted as clinical advice or used with real patients.

## REST integration
The REST Connector calls `/api/appointments/check` to retrieve slot availability, and `/api/appointments/book` to reserve a synthetic selected slot. The mock service can return no slots or HTTP 503 to support exception and recovery demonstrations. No real patient data is stored or sent.

## Worker implementation
`validate-registration` checks the registration fields and exposes `registrationValid` and `registrationMessage`. `check-appointment-availability` makes an HTTP request to the mock scheduling service and returns worker-side availability variables; the BPMN REST Connector also retrieves the available slots for the orchestration gateway. The test-only failure flag can force a worker incident.

## Results and limitations
BPMN/DMN models, linked Tasklist forms, Java worker source, mock scheduling API, request/response examples, variable dictionary, and five test scenarios are included. Runtime execution, real Tasklist/Operate evidence, and incident-recovery screenshots must be captured from the local Camunda instance. This is a simulated educational scheduling workflow and must not contain real health information.
