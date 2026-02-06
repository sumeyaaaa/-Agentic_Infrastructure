.PHONY: setup test lint spec-check docker-test docker-build help

help:
	@echo "Project Chimera - Makefile Commands"
	@echo "  make setup       - Install dependencies"
	@echo "  make test        - Run tests locally"
	@echo "  make docker-test - Run tests in Docker (Task 3.2 requirement)"
	@echo "  make docker-build - Build Docker image"
	@echo "  make lint        - Run linters"
	@echo "  make spec-check  - Verify code aligns with specs (optional)"

setup:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

docker-build:
	docker build -t chimera-test .

docker-test: docker-build
	@echo "Running tests in Docker container..."
	docker run --rm chimera-test make test

lint:
	ruff check .
	black --check .

spec-check:
	@python scripts/spec_check.py

