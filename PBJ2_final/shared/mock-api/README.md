# PBJ-2 synthetic REST API reference

The mock service uses Python's standard library only and listens on `http://localhost:8081`.
Run it from the repository root with `powershell -ExecutionPolicy Bypass -File .\scripts\Run-MockApi.ps1`.

| Method | Endpoint | Purpose | Successful response / failure controls |
|---|---|---|---|
| GET | `/health` | Health check | `{"status":"UP"}` |
| POST | `/api/credit-assessment` | Lab 1 synthetic credit assessment | Returns `creditScore`, `riskBand`, `assessmentStatus`, and reference. `simulateFailure=true` returns 503; `simulateTimeout=true` waits 25 seconds and returns 504 (the BPMN connector read timeout is 20 seconds). |
| POST | `/api/payments/charge` | Lab 2 mock payment | Returns `paymentStatus` APPROVED or DECLINED. `tok_test_declined` or `forceDecline=true` declines; `simulateFailure=true` returns 503. |
| POST | `/api/appointments/check` | Lab 3 synthetic slot search | Returns `available`, `slots`, and status. `forceNoSlots=true` returns an empty list; `simulateFailure=true` returns 503. |
| POST | `/api/appointments/book` | Lab 3 synthetic appointment booking | Accepts only `09:00`, `11:30`, or `14:00`; returns BOOKED or HTTP 409. `simulateFailure=true` returns 503. |

## Example calls

```powershell
Invoke-RestMethod http://localhost:8081/health
Invoke-RestMethod -Method Post -Uri http://localhost:8081/api/credit-assessment -ContentType 'application/json' -Body '{"applicantId":"APP-001","creditScore":760}'
Invoke-RestMethod -Method Post -Uri http://localhost:8081/api/payments/charge -ContentType 'application/json' -Body '{"paymentToken":"tok_test_approved","amount":1000}'
Invoke-RestMethod -Method Post -Uri http://localhost:8081/api/appointments/check -ContentType 'application/json' -Body '{"patientRef":"PAT-001","appointmentPreference":"Morning"}'
```

Request and response JSON files are in `examples/`. Every identifier, token, transaction, appointment, and response is synthetic. This service is for coursework demonstration only, not production use.
