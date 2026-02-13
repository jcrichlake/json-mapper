"""Tests for the utils module."""

import json
from pathlib import Path

import pytest
import yaml

from json_mapper.utils import (
    load_data_file,
    load_json_file,
    save_data_file,
    save_json_file,
)


class TestLoadJsonFile:
    """Tests for load_json_file function."""

    def test_load_valid_json(self, tmp_path: Path) -> None:
        """Test loading a valid JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = load_json_file(str(test_file))
        assert result == test_data

    def test_load_nonexistent_file(self) -> None:
        """Test loading a file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_json_file("nonexistent.json")

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        """Test loading a file with invalid JSON."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("not valid json {")

        with pytest.raises(json.JSONDecodeError):
            load_json_file(str(test_file))

    def test_load_non_object_json(self, tmp_path: Path) -> None:
        """Test loading JSON that is not an object."""
        test_file = tmp_path / "array.json"
        test_file.write_text("[1, 2, 3]")

        with pytest.raises(TypeError, match="Expected JSON object"):
            load_json_file(str(test_file))


class TestSaveJsonFile:
    """Tests for save_json_file function."""

    def test_save_json(self, tmp_path: Path) -> None:
        """Test saving JSON to a file."""
        test_file = tmp_path / "output.json"
        test_data = {"key": "value", "nested": {"data": [1, 2, 3]}}

        save_json_file(test_data, str(test_file))

        assert test_file.exists()
        loaded_data = json.loads(test_file.read_text())
        assert loaded_data == test_data

    def test_save_creates_directories(self, tmp_path: Path) -> None:
        """Test that save_json_file creates parent directories."""
        test_file = tmp_path / "subdir" / "nested" / "output.json"
        test_data = {"test": "data"}

        save_json_file(test_data, str(test_file))

        assert test_file.exists()
        assert test_file.parent.exists()

    def test_save_with_custom_indent(self, tmp_path: Path) -> None:
        """Test saving JSON with custom indentation."""
        test_file = tmp_path / "output.json"
        test_data = {"key": "value"}

        save_json_file(test_data, str(test_file), indent=4)

        content = test_file.read_text()
        # Check that the file is indented with 4 spaces
        assert '    "key"' in content


class TestLoadDataFile:
    """Tests for load_data_file function."""

    def test_load_json_file(self, tmp_path: Path) -> None:
        """Test loading a JSON file via load_data_file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = load_data_file(str(test_file))
        assert result == test_data

    def test_load_yaml_file(self, tmp_path: Path) -> None:
        """Test loading a YAML file with .yaml extension."""
        test_file = tmp_path / "test.yaml"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(yaml.safe_dump(test_data))

        result = load_data_file(str(test_file))
        assert result == test_data

    def test_load_yml_file(self, tmp_path: Path) -> None:
        """Test loading a YAML file with .yml extension."""
        test_file = tmp_path / "test.yml"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(yaml.safe_dump(test_data))

        result = load_data_file(str(test_file))
        assert result == test_data

    def test_load_nonexistent_file(self) -> None:
        """Test loading a file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_data_file("nonexistent.yaml")

    def test_load_invalid_yaml(self, tmp_path: Path) -> None:
        """Test loading a file with invalid YAML."""
        test_file = tmp_path / "invalid.yaml"
        test_file.write_text("invalid: yaml: content:")

        with pytest.raises(yaml.YAMLError):
            load_data_file(str(test_file))

    def test_load_non_object_yaml(self, tmp_path: Path) -> None:
        """Test loading YAML that is not an object."""
        test_file = tmp_path / "array.yaml"
        test_file.write_text("- item1\n- item2")

        with pytest.raises(TypeError, match="Expected JSON object"):
            load_data_file(str(test_file))

    def test_load_empty_yaml(self, tmp_path: Path) -> None:
        """Test loading an empty YAML file."""
        test_file = tmp_path / "empty.yaml"
        test_file.write_text("")

        with pytest.raises(TypeError, match="Expected JSON object"):
            load_data_file(str(test_file))

    def test_load_unsupported_extension(self, tmp_path: Path) -> None:
        """Test loading a file with unsupported extension."""
        test_file = tmp_path / "test.xml"
        test_file.write_text("<root></root>")

        with pytest.raises(ValueError, match="Unsupported file format"):
            load_data_file(str(test_file))


class TestSaveDataFile:
    """Tests for save_data_file function."""

    def test_save_json_file(self, tmp_path: Path) -> None:
        """Test saving to a JSON file via save_data_file."""
        test_file = tmp_path / "output.json"
        test_data = {"key": "value", "nested": {"data": [1, 2, 3]}}

        save_data_file(test_data, str(test_file))

        assert test_file.exists()
        loaded_data = json.loads(test_file.read_text())
        assert loaded_data == test_data

    def test_save_yaml_file(self, tmp_path: Path) -> None:
        """Test saving to a YAML file with .yaml extension."""
        test_file = tmp_path / "output.yaml"
        test_data = {"key": "value", "nested": {"data": [1, 2, 3]}}

        save_data_file(test_data, str(test_file))

        assert test_file.exists()
        loaded_data = yaml.safe_load(test_file.read_text())
        assert loaded_data == test_data

    def test_save_yml_file(self, tmp_path: Path) -> None:
        """Test saving to a YAML file with .yml extension."""
        test_file = tmp_path / "output.yml"
        test_data = {"key": "value", "nested": {"data": [1, 2, 3]}}

        save_data_file(test_data, str(test_file))

        assert test_file.exists()
        loaded_data = yaml.safe_load(test_file.read_text())
        assert loaded_data == test_data

    def test_save_creates_directories(self, tmp_path: Path) -> None:
        """Test that save_data_file creates parent directories."""
        test_file = tmp_path / "subdir" / "nested" / "output.yaml"
        test_data = {"test": "data"}

        save_data_file(test_data, str(test_file))

        assert test_file.exists()
        assert test_file.parent.exists()

    def test_save_yaml_custom_indent(self, tmp_path: Path) -> None:
        """Test saving YAML with custom indentation."""
        test_file = tmp_path / "output.yaml"
        test_data = {"key": "nested", "data": {"inner": "value"}}

        save_data_file(test_data, str(test_file), indent=4)

        content = test_file.read_text()
        # Check that nested content is indented with 4 spaces
        assert "    inner" in content

    def test_save_yaml_preserves_key_order(self, tmp_path: Path) -> None:
        """Test that save_data_file preserves key insertion order in YAML."""
        test_file = tmp_path / "output.yaml"
        test_data = {"zebra": 1, "alpha": 2, "middle": 3}

        save_data_file(test_data, str(test_file))

        content = test_file.read_text()
        # Verify keys appear in insertion order, not alphabetical
        zebra_pos = content.find("zebra")
        alpha_pos = content.find("alpha")
        middle_pos = content.find("middle")

        assert zebra_pos < alpha_pos < middle_pos

    def test_save_unsupported_extension(self, tmp_path: Path) -> None:
        """Test saving to a file with unsupported extension."""
        test_file = tmp_path / "output.xml"
        test_data = {"test": "data"}

        with pytest.raises(ValueError, match="Unsupported file format"):
            save_data_file(test_data, str(test_file))
