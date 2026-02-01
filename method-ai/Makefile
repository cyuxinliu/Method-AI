.PHONY: help install dev test lint format type-check clean docker-build docker-up docker-down

# Default target
help:
	@echo "Method.AI Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Setup:"
	@echo "  install        Install all dependencies"
	@echo "  install-dev    Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  dev            Run the development server"
	@echo "  test           Run all tests"
	@echo "  test-cov       Run tests with coverage report"
	@echo "  lint           Run linter (ruff)"
	@echo "  format         Format code (ruff)"
	@echo "  type-check     Run type checker (mypy)"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build   Build Docker images"
	@echo "  docker-up      Start Docker containers"
	@echo "  docker-down    Stop Docker containers"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean          Remove build artifacts and caches"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Development
dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest backend/tests -v

test-cov:
	pytest backend/tests -v --cov=backend/app --cov-report=html --cov-report=term-missing

lint:
	ruff check backend/

format:
	ruff check backend/ --fix
	ruff format backend/

type-check:
	mypy backend/app

# Docker
docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-up:
	docker-compose -f docker/docker-compose.yml up

docker-down:
	docker-compose -f docker/docker-compose.yml down

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
