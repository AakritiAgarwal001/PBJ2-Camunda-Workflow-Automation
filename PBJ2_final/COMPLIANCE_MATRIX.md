# Assignment compliance matrix

This matrix follows the supplied `Camunda8_Practical_Assignment_Labs_1_to_3.pdf` requirements.

| Teacher requirement | Lab 1 | Lab 2 | Lab 3 |
|---|---|---|---|
| Separate executable BPMN workflow | `Loan_Approval.bpmn` | `ECommerce_Order_Processing.bpmn` | `Hospital_Appointment_Triage.bpmn` |
| DMN decision table with documented rules | `Loan_Approval.dmn` + report | `Order_Priority.dmn` + report | `Triage_Decision.dmn` + report |
| Java/Spring Boot worker | `validate-applicant` | `validate-order`, `check-inventory` | `validate-registration`, `check-appointment-availability` |
| REST Connector / mock API | Credit assessment | Mock payment gateway | Scheduling check and booking |
| Process-variable dictionary | `VARIABLES.md` | `VARIABLES.md` | `VARIABLES.md` |
| Gateways and routing | Validation, DMN, review | Validation, stock, priority, payment | Registration, triage, availability, booking |
| Tasklist human task | Manual loan review | High-value / exception verification | Priority, urgent, no-slot/exception review |
| Minimum five test scenarios | Test plan included | Test plan included | Test plan included |
| Operate monitoring / failure and recovery | Failure flags + instructions | Failure flags + instructions | Failure flags + instructions |
| Report and REST examples | Report + shared examples | Report + shared examples | Report + shared examples |
| Genuine screenshots from student's running instance | **Must capture** | **Must capture** | **Must capture** |
| Actual test outcome records | **Must update after live run** | **Must update after live run** | **Must update after live run** |

## Important

The source package supplies the models, code, API stubs, and reproducible test plans. Deployment, execution, Tasklist/Operate observation, and screenshots are runtime activities on the student's local Camunda instance and are not represented as completed here.
