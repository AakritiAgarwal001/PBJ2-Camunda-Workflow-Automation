# Lab 1 — DMN sample evaluations

Educational rules only. DMN ID: `loanEligibilityDecision`; hit policy: `FIRST`.

| Sample | creditAssessment.creditScore | monthlyIncome (INR) | requestedLoanAmount / monthlyIncome | employmentStatus | Expected output |
|---|---:|---:|---:|---|---|
| Strong salaried applicant | 760 | 50000 | 6 | SALARIED | `APPROVED` (Rule 3) |
| Low credit score | 420 | 50000 | 6 | SALARIED | `REJECTED` (Rule 1) |
| Low income | 720 | 18000 | 6 | SALARIED | `REJECTED` (Rule 2) |
| Borderline applicant | 620 | 30000 | 30 | SELF_EMPLOYED | `MANUAL_REVIEW` (Rule 5) |
| Qualifying self-employed | 680 | 40000 | 10 | SELF_EMPLOYED | `APPROVED` (Rule 4) |

These sample outcomes are decision-table walkthroughs, not Camunda runtime evaluation evidence.
