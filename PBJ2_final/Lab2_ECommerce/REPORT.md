# Lab 2 — End-to-End E-Commerce Order Processing and Fulfilment

## Objective
Create a workflow that validates an order, checks simulated stock, assigns delivery priority by DMN, processes a mock payment, and routes the order to fulfilment or review.

## Architecture and execution flow
The Tasklist Order Intake form captures customer reference, product, quantity, unit price, stock count, delivery preference, customer category, and a mock payment token. The Java `validate-order` worker validates inputs and calculates `orderTotal`. The `check-inventory` worker compares requested quantity with `availableStock`. Exclusive gateways stop invalid or out-of-stock orders. The `orderPriorityDecision` DMN uses order value, customer category, and delivery preference. A high-value or high-priority order is sent to a Tasklist manual-verification task. Approved orders and normal-priority orders call the payment REST Connector. Payment approval routes to the fulfilment end event; decline routes to a failed-payment end event.

## DMN rule assumptions
A `FIRST`-hit decision returns HIGH for very high order value, qualifying premium-customer orders, or EXPRESS delivery; other orders are NORMAL. The monetary thresholds are educational assumptions in INR.

## REST integration
The REST Connector posts synthetic order amount and a mock token to `/api/payments/charge`. `tok_test_declined` or `forcePaymentDecline=true` returns DECLINED; `simulatePaymentFailure=true` returns HTTP 503. No real credentials or transactions are used.

## Worker implementation
`validate-order` checks order fields and computes the total. `check-inventory` evaluates stock. The test-only flags can deliberately fail the worker or API so the incident and recovery path can be demonstrated in Operate.

## Results and limitations
BPMN/DMN models, forms, shared Java workers, mock API, sample API payloads, variable dictionary, and five test scenarios are included. Actual deployment, runtime results, Tasklist evidence, and Operate incident/recovery screenshots remain to be captured from the user's running Camunda instance. The inventory is synthetic and in-memory; payment is simulated.
