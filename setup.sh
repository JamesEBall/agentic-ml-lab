#!/usr/bin/env bash
set -euo pipefail

echo "=== Agentic ML Research Lab Setup ==="

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

# Create project subdirectories
mkdir -p project/{data,configs,results,visualizations,logs}

# Initialize MLflow
echo "Initializing MLflow tracking..."
mkdir -p mlruns
python3 -c "import mlflow; mlflow.set_tracking_uri('file:./mlruns'); print('MLflow initialized at ./mlruns')"

echo ""
echo "=== Setup Complete ==="
echo "To activate: source venv/bin/activate"
echo "To start MLflow UI: mlflow ui --backend-store-uri file:./mlruns"
echo "To begin: describe your ML problem to Claude Code in this directory"
