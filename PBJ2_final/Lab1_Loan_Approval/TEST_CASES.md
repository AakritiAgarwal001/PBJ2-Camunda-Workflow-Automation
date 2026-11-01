# Lab 1 — Test plan and execution record

The values below are synthetic. **Expected routes are design expectations; actual Camunda outcomes must be recorded after running the model.**

| ID | Input highlights | Expected route | Actual outcome | Status |
|---|---|---|---|---|
| L1-T1 | `APP-001`, amount 300000, income 50000, SALARIED, GOOD, score 760 | VALID → credit API → DMN APPROVED → approved end | Record from Operate | Pending live run |
| L1-T2 | `APP-002`, amount 300000, income 50000, score 420 | VALID → credit API → DMN REJECTED → rejected end | Record from Operate | Pending live run |
| L1-T3 | `APP-003`, amount 900000, income 30000, score 620 | DMN MANUAL_REVIEW → Tasklist → reviewer outcome | Record from Tasklist/Operate | Pending live run |
| L1-T4 | `simulateApiFailure=true` | REST connector receives HTTP 503; incident/retries visible in Operate; set flag false and retry | Record incident key and recovery | Pending live run |
| L1-T5 | `simulateWorkerFailure=true` | Worker throws intentional exception; retries exhaust and incident appears; set flag false and retry | Record incident key and recovery | Pending live run |

| L1-T6 | `simulateApiTimeout=true` | Credit API exceeds the connector read timeout; incident visible in Operate; correct flag and retry | Record timeout and recovery | Pending live run |

## Sample input sets

- **Approve:** `applicantId=APP-001`, `applicantName=Sample One`, `requestedLoanAmount=300000`, `monthlyIncome=50000`, `employmentStatus=SALARIED`, `creditHistory=GOOD`, `creditScore=760`.
- **Reject:** `applicantId=APP-002`, `applicantName=Sample Two`, `requestedLoanAmount=300000`, `monthlyIncome=50000`, `employmentStatus=SALARIED`, `creditHistory=POOR`, `creditScore=420`.
- **Manual review:** `applicantId=APP-003`, `applicantName=Sample Three`, `requestedLoanAmount=900000`, `monthlyIncome=30000`, `employmentStatus=SELF_EMPLOYED`, `creditHistory=AVERAGE`, `creditScore=620`.

For failure tests, submit the corresponding boolean as `true` in the Tasklist form. For the Lab 1 timeout case, set `simulateApiTimeout=true`; the mock API waits 25 seconds while the REST connector read timeout is set to 20 seconds. After the incident is created, correct the variable to `false` using the supported Operate variable-editing workflow for the installed 8.9 environment, then retry the failed instance/job where supported. Capture the before/after screens.
