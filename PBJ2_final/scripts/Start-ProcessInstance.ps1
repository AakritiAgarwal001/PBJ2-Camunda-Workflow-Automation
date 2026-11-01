param(
  [Parameter(Mandatory=$true)]
  [ValidateSet("lab1","lab2","lab3")]
  [string]$Lab
)
$processIds = @{
  lab1 = "loanApprovalProcess"
  lab2 = "ecommerceOrderProcess"
  lab3 = "hospitalTriageProcess"
}
$payload = @{
  processDefinitionId = $processIds[$Lab]
  processDefinitionVersion = -1
  variables = @{}
} | ConvertTo-Json -Depth 10
try {
  $result = Invoke-RestMethod -Uri "http://localhost:8080/v2/process-instances" -Method Post -ContentType "application/json" -Body $payload
  Write-Host "Started $Lab process. Instance key: $($result.processInstanceKey)" -ForegroundColor Green
  Write-Host "Open Tasklist at http://localhost:8080/tasklist and complete the initial form."
} catch {
  Write-Error "Could not start process. Confirm Camunda Run is running and the BPMN model has been deployed. Details: $_"
  exit 1
}
