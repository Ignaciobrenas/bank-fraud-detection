#!/bin/bash
echo "=========================================="
echo " Bank Fraud Detection - Setup Environment "
echo "=========================================="

echo "[1/3] Creating virtual environment..."
python -m venv .venv

echo "[2/3] Activating venv and installing requirements..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/3] Checking dependencies..."
if type -p java > /dev/null; then
    echo "✅ Java is installed (Required for PySpark)."
else
    echo "⚠️ WARNING: Java is not installed or not in PATH."
    echo "PySpark requires Java 8, 11, or 17 to run locally."
fi

echo "=========================================="
echo "Setup complete! 🎉"
echo "Run 'source .venv/bin/activate' followed by 'make generate' to start."
