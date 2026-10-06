Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Bank Fraud Detection - Setup Environment " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host "[1/3] Creating virtual environment..."
python -m venv .venv

Write-Host "[2/3] Activating venv and installing requirements..."
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "[3/3] Checking dependencies..."
if (Get-Command java -ErrorAction SilentlyContinue) {
    Write-Host "✅ Java is installed (Required for PySpark)." -ForegroundColor Green
} else {
    Write-Host "⚠️ WARNING: Java is not installed or not in PATH." -ForegroundColor Yellow
    Write-Host "PySpark requires Java 8, 11, or 17 to run locally on Windows." -ForegroundColor Yellow
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup complete! 🎉" -ForegroundColor Green
Write-Host "Run '.venv\Scripts\Activate.ps1' followed by 'make generate' to start."
