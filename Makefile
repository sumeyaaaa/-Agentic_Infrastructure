.PHONY: setup test lint spec-check help

help:
	@echo "Project Chimera - Makefile Commands"
	@echo "  make setup      - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make spec-check - Verify code aligns with specs (optional)"

setup:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check .
	black --check .

spec-check:
	@echo "🚧 Spec-check script to be implemented in Task 3.3"
	@echo "This will verify that code aligns with specs/ directory"

