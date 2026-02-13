.PHONY: help install format format-check lint lint-fix type-check test test-cov checks clean examples

RUN_CMD := poetry run

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install dependencies using poetry"
	@echo "  format       - Format code with black"
	@echo "  lint         - Lint code with ruff"
	@echo "  type-check   - Run type checking with mypy"
	@echo "  test         - Run tests with pytest"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  checks       - Run format, lint, type-check, and test-cov"
	@echo "  clean        - Remove build artifacts and cache files"

# Install dependencies
install:
	$(RUN_CMD) poetry install

# Format code with black
format:
	@echo "==> Formatting code with black..."
	$(RUN_CMD) black .

format-check:
	@echo "==> Checking code formatting with black..."
	$(RUN_CMD) black --check .

lint-fix:
	@echo "==> Fixing linting errors with ruff..."
	$(RUN_CMD) ruff check --fix .

# Lint code with ruff
lint:
	@echo "==> Linting code with ruff..."
	$(RUN_CMD) ruff check .

# Run type checking with mypy
type-check:
	@echo "==> Running type checks with mypy..."
	$(RUN_CMD) mypy json_mapper/

# Run tests without coverage
test:
	@echo "==> Running tests..."
	$(RUN_CMD) pytest

# Run tests with coverage
test-cov:
	@echo "==> Running tests with coverage..."
	$(RUN_CMD) pytest --cov=json_mapper --cov-report=term-missing --cov-fail-under=95

# Run example
examples:
	@echo "==> Running examples..."
	@echo "\n\n==> Example 1: Print to stdout"
	$(RUN_CMD) json-mapper examples/input.json -m examples/mapping.json
	@echo "\n\n==> Example 2: Print to file"
	$(RUN_CMD) json-mapper examples/input.json -m examples/mapping.json -o output/output.json
	@echo "\n\n==> Example 3: YAML input and mapping to stdout"
	$(RUN_CMD) json-mapper examples/input.yaml -m examples/mapping.yaml
	@echo "\n\n==> Example 4: Mixed formats — YAML input to YAML output file"
	$(RUN_CMD) json-mapper examples/input.yaml -m examples/mapping.json -o output/output.yaml
	@echo "\n\n==> Example 5: JSON input with --yaml stdout"
	$(RUN_CMD) json-mapper examples/input.json -m examples/mapping.json --yaml

# Run all checks (format, lint, type-check, and test with coverage)
checks: format-check lint type-check test-cov
	@echo "==> All checks passed! ✓"

fix: format lint-fix
	@echo "==> All fixes applied! ✓"

# Clean build artifacts and cache
clean:
	@echo "==> Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
