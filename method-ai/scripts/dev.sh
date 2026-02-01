#!/bin/bash
# Development server script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Starting Method.AI development server..."
echo "API docs will be available at: http://localhost:8000/docs"
echo ""

cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
