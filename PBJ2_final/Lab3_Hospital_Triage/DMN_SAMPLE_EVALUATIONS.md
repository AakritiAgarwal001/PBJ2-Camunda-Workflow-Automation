# Lab 3 — DMN sample evaluations

DMN ID: `triageDecision`; hit policy: `FIRST`. The rules are illustrative classroom routing only, not clinical guidance.

| Sample | redFlag | urgencyIndicator | Expected output |
|---|---|---|---|
| Routine request | false | LOW | `ROUTINE` (Rule 4) |
| Medium indicator | false | MEDIUM | `PRIORITY_REVIEW` (Rule 3) |
| High indicator | false | HIGH | `PRIORITY_REVIEW` (Rule 2) |
| Red flag | true | LOW | `URGENT_ASSESSMENT` (Rule 1) |

These sample outcomes are decision-table walkthroughs, not Camunda runtime evaluation evidence.
