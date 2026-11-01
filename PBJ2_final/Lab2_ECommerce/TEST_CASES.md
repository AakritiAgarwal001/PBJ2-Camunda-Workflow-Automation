# Lab 2 — Test plan and execution record

| ID | Input highlights | Expected route | Actual outcome | Status |
|---|---|---|---|---|
| L2-T1 | quantity 2, unitPrice 500, availableStock 5, STANDARD customer, STANDARD delivery, approved token | Valid → stock available → normal priority → payment approved → fulfilment | Record in Operate | Pending live run |
| L2-T2 | quantity 8, availableStock 3 | Valid → inventory worker → insufficient-stock end; no payment call | Record in Operate | Pending live run |
| L2-T3 | `paymentToken=tok_test_declined` | Payment returns DECLINED → declined end | Record in Operate | Pending live run |
| L2-T4 | unitPrice 1500, quantity 2 (order total 3000) | High-value exception → Tasklist manual verification → payment after approval | Record Tasklist/Operate | Pending live run |
| L2-T5 | `simulatePaymentFailure=true` or `simulateInventoryFailure=true` | 503 or worker failure creates incident; correct flag and retry | Record before/after in Operate | Pending live run |

## Sample input sets

- **Normal fulfilled order:** `customerRef=CUST-001`, `productId=SKU-101`, `quantity=2`, `unitPrice=500`, `availableStock=10`, `customerCategory=STANDARD`, `deliveryPreference=STANDARD`, `paymentToken=tok_test_approved`.
- **Insufficient stock:** same values but `quantity=8`, `availableStock=3`.
- **Declined:** standard order with `paymentToken=tok_test_declined`.
- **High value:** `quantity=2`, `unitPrice=1500`, `availableStock=10`, `customerCategory=PREMIUM`, `deliveryPreference=EXPRESS`, approved token; complete manual review as APPROVED to continue.

The mock payment API never processes a real card or bank credential. Correct a failure flag before retrying the connector/worker job.
