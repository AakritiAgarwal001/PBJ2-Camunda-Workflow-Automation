$project = Join-Path $PSScriptRoot "..\shared"
Set-Location $project
mvn spring-boot:run
