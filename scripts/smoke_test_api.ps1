Write-Host "=== API Smoke Test ===" -ForegroundColor Cyan

Write-Host ""
Write-Host "GET /health" -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get

Write-Host ""
Write-Host "POST /predict" -ForegroundColor Yellow

$body = @{
    title = "VPN connection keeps dropping"
    description = "User reports unstable remote access since this morning and needs help urgently."
    channel = "email"
    priority = "high"
    requester_type = "external"
    created_hour = 7
    request_type = "problem"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/predict" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body