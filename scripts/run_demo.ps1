Write-Host "=== Work Intake Intelligence Demo Run ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "1) Activate virtual environment" -ForegroundColor Yellow
Write-Host ".venv\Scripts\Activate.ps1"
Write-Host ""

Write-Host "2) Start FastAPI service" -ForegroundColor Yellow
Write-Host "uvicorn src.api.main:app --reload"
Write-Host ""

Write-Host "3) In another terminal, run smoke test" -ForegroundColor Yellow
Write-Host ".\scripts\smoke_test_api.ps1"
Write-Host ""

Write-Host "4) Generate monitoring outputs if needed" -ForegroundColor Yellow
Write-Host "python -m src.monitoring.run_monitoring"
Write-Host "python -m src.monitoring.export_monitoring_csv"
Write-Host ""

Write-Host "5) Open API docs" -ForegroundColor Yellow
Write-Host "http://127.0.0.1:8000/docs"
Write-Host ""

Write-Host "6) Open Power BI monitoring screenshot / dashboard evidence" -ForegroundColor Yellow
Write-Host "reports/monitoring/assets/monitoring_dashboard.png"
Write-Host ""

Write-Host "Demo sequence ready." -ForegroundColor Green