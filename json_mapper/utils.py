"""Common utility functions for json-mapper."""

import json
from pathlib import Path
from typing import Any

import yaml


def load_json_file(file_path: str) -> dict[str, Any]:
    """Load and parse a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON data as a dictionary

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        TypeError: If the JSON content is not an object
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with path.open("r") as f:
        data = json.load(f)
        if not isinstance(data, dict):
            raise TypeError(f"Expected JSON object, got {type(data).__name__}")
        return data


def save_json_file(
    data: dict[str, Any],
    file_path: str,
    indent: int = 2,
) -> None:
    """Save data to a JSON file.

    Args:
        data: Dictionary to save as JSON
        file_path: Path where the JSON file should be saved
        indent: Number of spaces for indentation (default: 2)
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as f:
        json.dump(data, f, indent=indent)


def load_data_file(file_path: str) -> dict[str, Any]:
    """Load and parse a data file in JSON or YAML format.

    Args:
        file_path: Path to the data file (.json, .yaml, or .yml)

    Returns:
        Parsed data as a dictionary

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        yaml.YAMLError: If the file contains invalid YAML
        TypeError: If the file content is not an object/dict
        ValueError: If the file format is not supported
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".json":
        return load_json_file(file_path)
    elif suffix in (".yaml", ".yml"):
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with path.open("r") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise TypeError(f"Expected JSON object, got {type(data).__name__}")
            return data
    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. Supported formats: .json, .yaml, .yml",
        )


def save_data_file(
    data: dict[str, Any],
    file_path: str,
    indent: int = 2,
) -> None:
    """Save data to a file in JSON or YAML format.

    Args:
        data: Dictionary to save
        file_path: Path where the file should be saved (.json, .yaml, or .yml)
        indent: Number of spaces for indentation (default: 2)

    Raises:
        ValueError: If the file format is not supported
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".json":
        save_json_file(data, file_path, indent)
    elif suffix in (".yaml", ".yml"):
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w") as f:
            yaml.safe_dump(
                data,
                f,
                indent=indent,
                sort_keys=False,
                default_flow_style=False,
            )
    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. Supported formats: .json, .yaml, .yml",
        )
