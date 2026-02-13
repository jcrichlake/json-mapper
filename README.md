# JSON Mapper

A Python CLI tool that translates JSON values from one format to another using a declarative mapping configuration. Supports both JSON and YAML file formats for inputs and outputs.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Development](#development)

## Project Structure

```
root/
├── examples/           # Example input and mapping files
│   ├── input.json      # Sample input data (JSON)
│   ├── input.yaml      # Sample input data (YAML)
│   ├── mapping.json    # Sample mapping configuration (JSON)
│   └── mapping.yaml    # Sample mapping configuration (YAML)
├── json_mapper/        # The package
│   ├── transform.py    # Core transformation logic
│   ├── utils.py        # Utility functions
│   └── cli.py          # CLI implementation with argparse
├── tests/              # Test suite
│   ├── test_transform.py   # Transformation tests
│   ├── test_utils.py       # Utility function tests
│   └── test_cli.py         # CLI tests
├── Makefile            # Common development tasks
├── pyproject.toml      # Project configuration and dependencies
└── poetry.lock         # Locked dependencies
```

## Installation

Prerequisites:
- Python 3.13+
- Poetry

```bash
# Install with poetry
poetry install
```

## Usage

### Basic Usage

```bash
# Map a JSON file using a mapping configuration
poetry run json-mapper examples/input.json -m examples/mapping.json -o output.json

# Print result to stdout 
poetry run json-mapper examples/input.json -m examples/mapping.json

# Use YAML files for input and mapping
poetry run json-mapper examples/input.yaml -m examples/mapping.yaml -o output.yaml

# Mix JSON and YAML formats freely
poetry run json-mapper examples/input.yaml -m examples/mapping.json -o output.json

# Print YAML to stdout instead of JSON
poetry run json-mapper examples/input.json -m examples/mapping.json --yaml
```

You should see the following output:

```json
{
  "title": "Research Grant",
  "opportunityCode": "ABC-123-12345",
  "status": "open",
  "agency": {
    "name": "Department of Examples",
    "type": "Federal"
  },
  "contact": {
    "name": "Jane Smith",
    "email": "jane.smith@example.gov",
    "phone": "555-0100"
  },
  "funding": {
    "minimum": 10000,
    "maximum": 100000,
    "currency": "USD"
  },
  "eligibility": [
    "state_governments",
    "nonprofit"
  ],
  "deadline": "2025-07-15"
}
```

### Command-Line Options

```
positional arguments:
  input                 Input data file (JSON or YAML format)

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -m MAPPING, --mapping MAPPING
                        Mapping configuration file (JSON or YAML format)
  -o OUTPUT, --output OUTPUT
                        Output file (default: stdout)
  --indent INDENT       Number of spaces for JSON indentation (default: 2)
  --yaml                Output as YAML when printing to stdout (default: JSON)
```

### Supported Transformations

| Transformation | Handler  | Description                                                  | Example                                                                    |
| -------------- | -------- | ------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Field plucking | `field`  | Plucks a value from the input data using a dot-notation path | `{"field": "name.firstName"}`                                              |
| Literal value  | --       | Passes through a literal value unchanged                     | `{"amount": 42}`                                                           |
| Switch         | `switch` | Performs a case-based lookup based on a field value          | `{"switch": {"field": "status", "case": {...}, "default": "unknown"}}`     |
| Concatenation  | `concat` | Joins multiple values together                               | `{"concat": {"parts": [{"field": "amount"}, " ", {"field": "currency"}]}}` |

## Examples

### Example 1: Simple JSON Mapping

**input.json:**
```json
{
  "first_name": "John Doe",
  "last_name": "Doe",
  "age": 30,
  "email_address": "john@example.com"
}
```

**mapping.json:**
```json
{
  "name": {
    "firstName": { "field": "first_name" },
    "lastName": { "field": "last_name" }
  },
  "email": { "field": "email_address" },
  "age": { "field": "age" }
}
```

**Command:**
```bash
poetry run json-mapper examples/input.json -m examples/mapping.json
```

**Output:**
```json
{
  "name": {
    "firstName": "John",
    "lastName": "Doe"
  },
  "email": "john@example.com",
  "age": 30
}
```

### Example 2: Concatenation

**input.json:**
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```

**mapping.json:**
```json
{
  "fullName": {
    "concat": {
      "parts": [
        { "field": "first_name" },
        " ",
        { "field": "last_name" }
      ]
    }
  }
}
```

**Output:**
```json
{
  "fullName": "John Doe"
}
```

### Example 3: Switch

**input.json:**
```json
{
  "opportunity_status": "posted"
}
```

**mapping.json:**
```json
{
  "status": {
    "switch": {
      "field": "opportunity_status",
      "case": {
        "posted": "open",
        "forecasted": "upcoming",
        "archived": "closed"
      },
      "default": "unknown"
    }
  }
}
```

**Output:**
```json
{
  "status": "open"
}
```

## Development

### Quickstart commands

```bash
# Install dependencies
make install

# Fix auto-formatting and linting errors.
# You may need to run this multiple times to catch linting errors introduced by reformatting.
make fix

# Run all checks (formatting, linting, type-checking, and tests with coverage)
make checks

# Run examples
make examples
```

### Individual Commands

```bash
# Format code with black
make format

# Lint code with ruff
make lint

# Run type checking with mypy
make type-check

# Run tests
make test

# Run tests with coverage report
make test-cov

# Clean build artifacts
make clean
```

### Manual Commands

If you prefer to run commands directly:

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Type check
poetry run mypy json_mapper/

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=json_mapper --cov-report=term-missing --cov-report=html
```
