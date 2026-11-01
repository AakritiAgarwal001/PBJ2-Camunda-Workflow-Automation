# Lab 2 — DMN sample evaluations

DMN ID: `orderPriorityDecision`; hit policy: `FIRST`. Monetary values are synthetic INR.

| Sample | orderTotal | customerCategory | deliveryPreference | Expected output |
|---|---:|---|---|---|
| Standard order | 1000 | STANDARD | STANDARD | `NORMAL` (Rule 4) |
| High amount | 2500 | STANDARD | STANDARD | `HIGH` (Rule 1) |
| Premium order | 1500 | PREMIUM | STANDARD | `HIGH` (Rule 2) |
| Express delivery | 500 | STANDARD | EXPRESS | `HIGH` (Rule 3) |

These sample outcomes are decision-table walkthroughs, not Camunda runtime evaluation evidence.
