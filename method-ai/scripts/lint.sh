#!/bin/bash
# Linting script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "Running ruff linter..."
ruff check backend/

echo ""
echo "Running ruff formatter check..."
ruff format --check backend/

echo ""
echo "Linting complete!"
