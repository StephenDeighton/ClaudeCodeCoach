#!/bin/bash
# C3 Startup Script - Clean start with proper environment
set -e

echo "🚀 Starting Claude Code Coach (C3)"
echo "=================================="

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" < "3.12" ]]; then
    echo "❌ Error: Python 3.12+ required"
    exit 1
fi

# Clean Python cache
echo "🧹 Cleaning Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Run from project root."
    exit 1
fi

# Check for required dependencies
echo "📦 Checking dependencies..."
python3 -c "import flet" 2>/dev/null || {
    echo "❌ Flet not installed. Run: pip install flet==0.28.3"
    exit 1
}

echo "✓ Dependencies OK"
echo ""
echo "🎯 Launching C3..."
echo "Press Ctrl+C to stop"
echo ""

# Start the app
exec python3 main.py
