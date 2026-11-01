# Lab 3 — Process-variable dictionary

| Variable | Type | Created by / supplied at | Purpose |
|---|---|---|---|
| `patientRef` | string | Registration form | Synthetic patient reference only |
| `appointmentPreference` | string | Registration form | Preferred appointment time window |
| `symptomsSummary` | string | Registration form | Educational synthetic summary; no real patient data |
| `redFlag` | boolean | Registration form | Synthetic red-flag input to the DMN |
| `urgencyIndicator` | string | Registration form | `LOW`, `MEDIUM`, or `HIGH` |
| `forceNoSlots` | boolean | Form (testing only) | Forces scheduling API to return no slots |
| `simulateWorkerFailure` | boolean | Form (testing only) | Forces registration worker failure |
| `simulateSchedulingFailure` | boolean | Form (testing only) | Makes scheduling API return HTTP 503 |
| `registrationValid` | boolean | `validate-registration` worker | Controls registration gateway |
| `registrationMessage` | string | `validate-registration` worker | Validation detail |
| `triageCategory` | string | `triageDecision` DMN | `ROUTINE`, `PRIORITY_REVIEW`, or `URGENT_ASSESSMENT` |
| `priorityOutcome` | string | Priority Staff Review form | `PROCEED` or `ESCALATE` |
| `workerAvailabilityChecked` | boolean | `check-appointment-availability` worker | Confirms the Java worker successfully requested synthetic slot availability |
| `workerAppointmentAvailable` | boolean | `check-appointment-availability` worker | Availability pre-check result returned by the Spring Boot worker |
| `workerAvailableSlots` | array of strings | `check-appointment-availability` worker | Synthetic slots observed by the worker pre-check |
| `workerSchedulingCheckMessage` | string | `check-appointment-availability` worker | Availability pre-check status message |
| `appointmentAvailable` | boolean | REST Connector | Controls availability gateway |
| `availableSlots` | array of strings | REST Connector | Synthetic appointment slots |
| `schedulingStatus` | string | REST Connector | `AVAILABLE` or `NO_SLOTS` |
| `selectedSlot` | string | Slot Selection form | Selected synthetic slot |
| `bookingStatus` | string | REST Connector | `BOOKED` or an unsuccessful status |
| `bookingReference` | string | REST Connector | Synthetic booking reference |
| `assessmentDisposition` | string | Urgent Assessment form | Staff assessment action |
| `staffAction` | string | No Slot Review form | Staff follow-up action |
| `staffNotes` | string | Review form | Staff follow-up notes |

## Gateway routing

1. `registrationValid = true` proceeds to DMN; the default route ends as incomplete registration.
2. `triageCategory = "URGENT_ASSESSMENT"` routes directly to an urgent Tasklist task; `PRIORITY_REVIEW` routes to priority staff review; the default route is routine scheduling.
3. `priorityOutcome = "PROCEED"` proceeds to slot checking; otherwise the process ends as escalated/deferred.
4. The `check-appointment-availability` Spring Boot worker requests a synthetic availability pre-check; the REST Connector then independently retrieves the authoritative slot list.
5. `appointmentAvailable = true` proceeds to Tasklist slot selection; the default route requests staff follow-up.
6. `bookingStatus = "BOOKED"` ends booked; otherwise the process returns to the staff follow-up task.

**Safety boundary:** triage rules are illustrative classroom logic only. They are not medical advice, clinical triage, or for use with real people.
