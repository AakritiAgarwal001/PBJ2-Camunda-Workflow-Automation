Write-Host "Checking Camunda REST API..."
try { Invoke-RestMethod -Uri "http://localhost:8080/actuator/health" -TimeoutSec 5 | ConvertTo-Json -Depth 4 } catch { Write-Host "Actuator health endpoint unavailable; confirming base port instead." }
Test-NetConnection localhost -Port 8080
Write-Host "Checking mock API..."
try { Invoke-RestMethod -Uri "http://localhost:8081/health" -TimeoutSec 5 | ConvertTo-Json -Depth 4 } catch { Write-Host "Mock API is not running yet. Start scripts/Run-MockApi.ps1 in a separate terminal." }
