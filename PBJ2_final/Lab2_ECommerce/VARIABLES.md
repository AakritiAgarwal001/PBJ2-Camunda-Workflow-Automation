# Lab 2 — Process-variable dictionary

| Variable | Type | Created by / supplied at | Purpose |
|---|---|---|---|
| `customerRef` | string | Order Intake form | Synthetic customer reference |
| `productId` | string | Order Intake form | Product identifier |
| `quantity` | number | Order Intake form | Requested quantity |
| `unitPrice` | number | Order Intake form | Unit price in INR |
| `availableStock` | number | Order Intake form | Synthetic inventory count |
| `customerCategory` | string | Order Intake form | `STANDARD` or `PREMIUM` |
| `deliveryPreference` | string | Order Intake form | `STANDARD` or `EXPRESS` |
| `paymentToken` | string | Order Intake form | Mock token only; use `tok_test_approved` or `tok_test_declined` |
| `simulateWorkerFailure` | boolean | Form (testing only) | Forces validation worker failure |
| `simulateInventoryFailure` | boolean | Form (testing only) | Forces inventory worker failure |
| `simulatePaymentFailure` | boolean | Form (testing only) | Makes payment API return 503 |
| `forcePaymentDecline` | boolean | Form (testing only) | Makes payment return DECLINED |
| `orderValid` | boolean | `validate-order` worker | Result of order validation |
| `orderValidationMessage` | string | `validate-order` worker | Validation detail |
| `orderTotal` | number | `validate-order` worker | `quantity × unitPrice` |
| `currency` | string | `validate-order` worker | `INR` |
| `stockAvailable` | boolean | `check-inventory` worker | Controls stock gateway |
| `inventoryStatus` | string | `check-inventory` worker | `AVAILABLE` or `INSUFFICIENT_STOCK` |
| `orderPriority` | string | `orderPriorityDecision` DMN | `HIGH` or `NORMAL` |
| `reviewOutcome` | string | Manual Verification form | `APPROVED` or `REJECTED` |
| `reviewComments` | string | Manual Verification form | Reviewer explanation |
| `paymentStatus` | string | REST Connector | `APPROVED` or `DECLINED` |
| `paymentReference` | string | REST Connector | Synthetic transaction reference |

## Gateway routing

1. `orderValid = true` proceeds; invalid order uses the default rejection route.
2. `stockAvailable = true` proceeds; insufficient stock ends without fulfilment.
3. If `orderTotal >= 2000` or `orderPriority = "HIGH"`, the order goes to Tasklist manual verification. Otherwise it proceeds directly to payment.
4. `reviewOutcome = "APPROVED"` proceeds to payment; the default route ends without fulfilment.
5. `paymentStatus = "APPROVED"` ends at fulfilment; the default route ends as payment declined.
