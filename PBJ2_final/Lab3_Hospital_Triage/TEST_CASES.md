# Lab 3 — Test plan and execution record

| ID | Input highlights | Expected route | Actual outcome | Status |
|---|---|---|---|---|
| L3-T1 | redFlag=false, urgencyIndicator=LOW, forceNoSlots=false | ROUTINE → REST availability → slot selection → REST booking → BOOKED end | Record in Operate | Pending live run |
| L3-T2 | redFlag=false, urgencyIndicator=HIGH | PRIORITY_REVIEW → Tasklist staff review; PROCEED continues to scheduling | Record Tasklist/Operate | Pending live run |
| L3-T3 | redFlag=true | URGENT_ASSESSMENT → immediate human assessment task | Record Tasklist/Operate | Pending live run |
| L3-T4 | forceNoSlots=true | REST response contains empty slots → no-slot staff review → follow-up end | Record in Operate | Pending live run |
| L3-T5 | simulateSchedulingFailure=true or simulateWorkerFailure=true | Incident visible; correct flag and retry; workflow resumes | Record before/after in Operate | Pending live run |

## Sample input sets

- **Routine booked:** `patientRef=PAT-001`, `appointmentPreference=Morning`, `symptomsSummary=Routine synthetic consultation`, `redFlag=false`, `urgencyIndicator=LOW`, `forceNoSlots=false`, `simulateSchedulingFailure=false`.
- **Priority review:** same but `urgencyIndicator=HIGH`, `redFlag=false`; choose `priorityOutcome=PROCEED` in Tasklist to continue to scheduling.
- **Urgent assessment:** `redFlag=true`, `urgencyIndicator=HIGH`; workflow goes directly to an urgent staff assessment task.
- **No slots:** routine test with `forceNoSlots=true`.
- **Scheduling API error:** set `simulateSchedulingFailure=true`; after incident creation correct to false and retry.

All test patient identifiers and summaries are synthetic. Do not use real patient data.
