# Lab 1 — Process-variable dictionary

| Variable | Type | Created by / supplied at | Purpose |
|---|---|---|---|
| `applicantId` | string | Loan Application form | Synthetic applicant identifier |
| `applicantName` | string | Loan Application form | Synthetic applicant name |
| `requestedLoanAmount` | number | Loan Application form | Amount requested in INR |
| `monthlyIncome` | number | Loan Application form | Monthly income in INR |
| `employmentStatus` | string | Loan Application form | `SALARIED` or `SELF_EMPLOYED` |
| `creditHistory` | string | Loan Application form | `GOOD`, `AVERAGE`, or `POOR` |
| `creditScore` | number | Loan Application form | Synthetic score from 300 to 900 sent to the mock credit API |
| `simulateWorkerFailure` | boolean | Form (testing only) | Forces `validate-applicant` to fail so an Operate incident can be inspected |
| `simulateApiFailure` | boolean | Form (testing only) | Makes the mock credit API return HTTP 503 |
| `simulateApiTimeout` | boolean | Form (testing only) | Delays the mock credit API response so it exceeds the REST Connector's 20-second read timeout |
| `validationResult` | string | `validate-applicant` worker | `VALID` or `INVALID`; controls first gateway |
| `validationMessage` | string | `validate-applicant` worker | Worker validation explanation |
| `creditAssessment` | object | REST Connector | Mock credit API response, including `creditScore`, `riskBand`, and `assessmentStatus` |
| `loanDecision` | string | `loanEligibilityDecision` DMN | `APPROVED`, `REJECTED`, or `MANUAL_REVIEW` |
| `reviewOutcome` | string | Manual Review form | `APPROVED` or `REJECTED`; controls reviewer gateway |
| `reviewComments` | string | Manual Review form | Explanation recorded by the reviewer |

## Gateway routing

1. `validationResult = "VALID"` proceeds to credit assessment; the default route rejects invalid data.
2. DMN `loanDecision = "APPROVED"` ends approved; `REJECTED` ends rejected; the default route opens Tasklist manual review.
3. `reviewOutcome = "APPROVED"` ends approved; the default route ends rejected.

The REST connector maps its response with `resultExpression` into `creditAssessment`. Connector inputs use the local mock API at port 8081 and no authentication. The connector's retry/incident path is observable in Operate.

