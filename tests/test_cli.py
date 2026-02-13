"""Tests for the CLI module."""

import json
import sys
from unittest.mock import patch

import pytest
import yaml

from json_mapper.cli import (
    CliArgs,
    create_parser,
    load_input,
    load_mapping,
    main,
    transform_input,
    write_output,
)


class TestLoadMapping:
    """Tests for load_mapping function."""

    def test_load_mapping(self, tmp_path) -> None:
        """Test loading a mapping configuration file."""
        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"field1": {"field": "source_field"}}
        mapping_file.write_text(json.dumps(mapping_data))

        args = CliArgs(mapping=str(mapping_file), input="input.json")
        result = load_mapping(args)

        assert result == mapping_data

    def test_load_mapping_nonexistent_file(self, tmp_path) -> None:
        """Test loading a non-existent mapping file."""
        args = CliArgs(mapping=str(tmp_path / "nonexistent.json"), input="input.json")

        with pytest.raises(FileNotFoundError):
            load_mapping(args)

    def test_load_mapping_invalid_json(self, tmp_path) -> None:
        """Test loading an invalid JSON mapping file."""
        mapping_file = tmp_path / "invalid.json"
        mapping_file.write_text("{ invalid json }")

        args = CliArgs(mapping=str(mapping_file), input="input.json")

        with pytest.raises(json.JSONDecodeError):
            load_mapping(args)

    def test_load_mapping_yaml(self, tmp_path) -> None:
        """Test loading a YAML mapping configuration file."""
        mapping_file = tmp_path / "mapping.yaml"
        mapping_data = {"field1": {"field": "source_field"}}
        mapping_file.write_text(yaml.safe_dump(mapping_data))

        args = CliArgs(mapping=str(mapping_file), input="input.json")
        result = load_mapping(args)

        assert result == mapping_data

    def test_load_mapping_yml(self, tmp_path) -> None:
        """Test loading a YML mapping configuration file."""
        mapping_file = tmp_path / "mapping.yml"
        mapping_data = {"field1": {"field": "source_field"}}
        mapping_file.write_text(yaml.safe_dump(mapping_data))

        args = CliArgs(mapping=str(mapping_file), input="input.json")
        result = load_mapping(args)

        assert result == mapping_data


class TestLoadInput:
    """Tests for load_input function."""

    def test_load_input_from_file(self, tmp_path) -> None:
        """Test loading input from a file."""
        input_file = tmp_path / "input.json"
        input_data = {"key": "value"}
        input_file.write_text(json.dumps(input_data))

        args = CliArgs(mapping="mapping.json", input=str(input_file))
        result = load_input(args)

        assert result == input_data

    def test_load_input_nonexistent_file(self, tmp_path) -> None:
        """Test loading from a non-existent input file."""
        args = CliArgs(mapping="mapping.json", input=str(tmp_path / "nonexistent.json"))

        with pytest.raises(FileNotFoundError):
            load_input(args)

    def test_load_input_yaml(self, tmp_path) -> None:
        """Test loading input from a YAML file."""
        input_file = tmp_path / "input.yaml"
        input_data = {"key": "value"}
        input_file.write_text(yaml.safe_dump(input_data))

        args = CliArgs(mapping="mapping.json", input=str(input_file))
        result = load_input(args)

        assert result == input_data

    def test_load_input_yml(self, tmp_path) -> None:
        """Test loading input from a YML file."""
        input_file = tmp_path / "input.yml"
        input_data = {"key": "value"}
        input_file.write_text(yaml.safe_dump(input_data))

        args = CliArgs(mapping="mapping.json", input=str(input_file))
        result = load_input(args)

        assert result == input_data


class TestTransformInput:
    """Tests for transform_input function."""

    def test_transform_input(self) -> None:
        """Test transforming input data with a mapping."""
        input_data = {"source_field": "test_value"}
        mapping = {"target_field": {"field": "source_field"}}

        result = transform_input(input_data, mapping)

        assert result == {"target_field": "test_value"}

    def test_transform_input_complex_mapping(self) -> None:
        """Test transforming with a complex nested mapping."""
        input_data = {
            "user": {"name": "John", "status": "active"},
            "amount": 100,
        }
        mapping = {
            "person": {
                "fullName": {"field": "user.name"},
                "isActive": {
                    "switch": {
                        "field": "user.status",
                        "case": {"active": True, "inactive": False},
                        "default": None,
                    },
                },
            },
            "total": {"field": "amount"},
        }

        result = transform_input(input_data, mapping)

        assert result == {
            "person": {"fullName": "John", "isActive": True},
            "total": 100,
        }


class TestCreateParser:
    """Tests for create_parser function."""

    def test_parser_creation(self) -> None:
        """Test that parser is created successfully."""
        parser = create_parser()
        assert parser.prog == "json-mapper"

    def test_parser_missing_all_arguments(self) -> None:
        """Test that required arguments are enforced."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_missing_mapping(self) -> None:
        """Test that mapping argument is required."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["input.json"])

    def test_parser_missing_input(self) -> None:
        """Test that input argument is required."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["-m", "mapping.json"])

    def test_parser_with_required_arguments(self) -> None:
        """Test parser with required arguments."""
        parser = create_parser()
        args = parser.parse_args(["input.json", "-m", "mapping.json"])

        assert args.input == "input.json"
        assert args.mapping == "mapping.json"
        assert args.output is None

    def test_parser_all_arguments(self) -> None:
        """Test parser with all arguments."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "input.json",
                "-m",
                "mapping.json",
                "-o",
                "output.json",
                "--indent",
                "4",
            ],
        )

        assert args.input == "input.json"
        assert args.mapping == "mapping.json"
        assert args.output == "output.json"
        assert args.indent == 4

    def test_parser_yaml_flag(self) -> None:
        """Test parser with --yaml flag."""
        parser = create_parser()
        args = parser.parse_args(["input.json", "-m", "mapping.json", "--yaml"])

        assert args.yaml is True

    def test_parser_yaml_flag_default(self) -> None:
        """Test parser --yaml flag defaults to False."""
        parser = create_parser()
        args = parser.parse_args(["input.json", "-m", "mapping.json"])

        assert args.yaml is False


class TestCliArgs:
    """Tests for CliArgs dataclass."""

    def test_from_namespace(self) -> None:
        """Test creating CliArgs from argparse Namespace."""
        parser = create_parser()
        namespace = parser.parse_args(["-m", "mapping.json", "input.json"])
        args = CliArgs.from_namespace(namespace)

        assert args.mapping == "mapping.json"
        assert args.input == "input.json"
        assert args.output is None
        assert args.indent == 2

    def test_from_namespace_all_options(self) -> None:
        """Test creating CliArgs with all options."""
        parser = create_parser()
        namespace = parser.parse_args(
            [
                "input.json",
                "-m",
                "mapping.json",
                "-o",
                "output.json",
                "--indent",
                "4",
            ],
        )
        args = CliArgs.from_namespace(namespace)

        assert args.mapping == "mapping.json"
        assert args.input == "input.json"
        assert args.output == "output.json"
        assert args.indent == 4

    def test_from_namespace_with_yaml(self) -> None:
        """Test creating CliArgs with --yaml flag."""
        parser = create_parser()
        namespace = parser.parse_args(
            ["input.json", "-m", "mapping.json", "--yaml"],
        )
        args = CliArgs.from_namespace(namespace)

        assert args.yaml is True


class TestWriteOutput:
    """Tests for write_output function."""

    def test_write_output_to_file(self, tmp_path) -> None:
        """Test writing output to a file."""
        output_file = tmp_path / "output.json"
        output_data = {"result": "success"}

        args = CliArgs(
            mapping="mapping.json",
            input="input.json",
            output=str(output_file),
        )
        write_output(output_data, args)

        assert output_file.exists()
        with output_file.open() as f:
            loaded_data = json.load(f)
        assert loaded_data == output_data

    def test_write_output_to_stdout(self, capsys) -> None:
        """Test writing output to stdout."""
        output_data = {"result": "success"}

        args = CliArgs(mapping="mapping.json", input="input.json", output=None)
        write_output(output_data, args)

        captured = capsys.readouterr()
        assert json.loads(captured.out.strip()) == output_data

    def test_write_output_custom_indent(self, tmp_path) -> None:
        """Test writing output with custom indentation."""
        output_file = tmp_path / "output.json"
        output_data = {"result": "success", "data": {"nested": "value"}}

        args = CliArgs(
            mapping="mapping.json",
            input="input.json",
            output=str(output_file),
            indent=4,
        )
        write_output(output_data, args)

        content = output_file.read_text()
        assert "    " in content

    def test_write_output_to_yaml_file(self, tmp_path) -> None:
        """Test writing output to a YAML file."""
        output_file = tmp_path / "output.yaml"
        output_data = {"result": "success"}

        args = CliArgs(
            mapping="mapping.json",
            input="input.json",
            output=str(output_file),
        )
        write_output(output_data, args)

        assert output_file.exists()
        loaded_data = yaml.safe_load(output_file.read_text())
        assert loaded_data == output_data

    def test_write_output_to_yml_file(self, tmp_path) -> None:
        """Test writing output to a YML file."""
        output_file = tmp_path / "output.yml"
        output_data = {"result": "success"}

        args = CliArgs(
            mapping="mapping.json",
            input="input.json",
            output=str(output_file),
        )
        write_output(output_data, args)

        assert output_file.exists()
        loaded_data = yaml.safe_load(output_file.read_text())
        assert loaded_data == output_data

    def test_write_output_yaml_stdout(self, capsys) -> None:
        """Test writing YAML output to stdout with --yaml flag."""
        output_data = {"result": "success"}

        args = CliArgs(
            mapping="mapping.json",
            input="input.json",
            output=None,
            yaml=True,
        )
        write_output(output_data, args)

        captured = capsys.readouterr()
        loaded_data = yaml.safe_load(captured.out)
        assert loaded_data == output_data

    def test_write_output_yaml_custom_indent(self, capsys) -> None:
        """Test writing YAML to stdout with custom indent."""
        output_data = {"result": "success", "data": {"nested": "value"}}

        args = CliArgs(
            mapping="mapping.json",
            input="input.json",
            output=None,
            indent=4,
            yaml=True,
        )
        write_output(output_data, args)

        captured = capsys.readouterr()
        assert "    nested" in captured.out

    def test_write_output_yaml_preserves_key_order(self, capsys) -> None:
        """Test that YAML stdout output preserves key order."""
        output_data = {"zebra": 1, "alpha": 2, "middle": 3}

        args = CliArgs(
            mapping="mapping.json",
            input="input.json",
            output=None,
            yaml=True,
        )
        write_output(output_data, args)

        captured = capsys.readouterr()
        zebra_pos = captured.out.find("zebra")
        alpha_pos = captured.out.find("alpha")
        middle_pos = captured.out.find("middle")
        assert zebra_pos < alpha_pos < middle_pos


class TestMainIntegration:
    """Integration tests for main function with various scenarios."""

    def test_main_success(self, tmp_path) -> None:
        """Test successful CLI execution."""
        # Create input file
        input_file = tmp_path / "input.json"
        input_data = {"source": "value"}
        input_file.write_text(json.dumps(input_data))

        # Create mapping file
        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        # Create output file path
        output_file = tmp_path / "output.json"

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
            "-o",
            str(output_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        assert output_file.exists()
        with output_file.open() as f:
            result = json.load(f)
        assert result == {"target": "value"}

    def test_main_file_not_found(self, tmp_path, capsys) -> None:
        """Test CLI with non-existent input file."""
        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        test_args = [
            "json-mapper",
            str(tmp_path / "nonexistent.json"),
            "-m",
            str(mapping_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "File not found" in captured.err

    def test_main_invalid_json(self, tmp_path, capsys) -> None:
        """Test CLI with invalid JSON input."""
        input_file = tmp_path / "input.json"
        input_file.write_text("{ invalid json }")

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error: Invalid JSON in file" in captured.err


class TestMainCLI:
    """Tests for main function CLI arguments and flags."""

    def test_main_missing_required_arguments(self) -> None:
        """Test main function with missing required arguments."""
        test_args = ["json-mapper"]

        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit):
                main()

    def test_main_missing_mapping_argument(self) -> None:
        """Test main function with missing mapping argument."""
        test_args = ["json-mapper", "input.json"]

        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit):
                main()

    def test_main_with_version(self, capsys) -> None:
        """Test main function with --version flag."""
        test_args = ["json-mapper", "--version"]

        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as excinfo:
                main()

        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "0.1.0" in captured.out

    def test_main_help(self, capsys) -> None:
        """Test main function with --help flag."""
        test_args = ["json-mapper", "--help"]

        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as excinfo:
                main()

        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "json-mapper" in captured.out
        assert "Translate JSON values" in captured.out

    def test_main_end_to_end(self, tmp_path) -> None:
        """Test complete end-to-end CLI workflow."""
        input_file = tmp_path / "input.json"
        input_data = {
            "user": {"name": "Alice", "type": "admin"},
            "value": 42,
        }
        input_file.write_text(json.dumps(input_data))

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {
            "userName": {"field": "user.name"},
            "role": {
                "switch": {
                    "field": "user.type",
                    "case": {"admin": "Administrator", "user": "Regular User"},
                    "default": "Unknown",
                },
            },
            "data": {"amount": {"field": "value"}, "currency": "USD"},
        }
        mapping_file.write_text(json.dumps(mapping_data))

        output_file = tmp_path / "output.json"

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
            "-o",
            str(output_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0

        with output_file.open() as f:
            result = json.load(f)

        expected = {
            "userName": "Alice",
            "role": "Administrator",
            "data": {"amount": 42, "currency": "USD"},
        }
        assert result == expected

    def test_main_yaml_input_json_output(self, tmp_path) -> None:
        """Test YAML input with JSON output."""
        input_file = tmp_path / "input.yaml"
        input_data = {"source": "value"}
        input_file.write_text(yaml.safe_dump(input_data))

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        output_file = tmp_path / "output.json"

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
            "-o",
            str(output_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        with output_file.open() as f:
            result = json.load(f)
        assert result == {"target": "value"}

    def test_main_json_input_yaml_output(self, tmp_path) -> None:
        """Test JSON input with YAML output."""
        input_file = tmp_path / "input.json"
        input_data = {"source": "value"}
        input_file.write_text(json.dumps(input_data))

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        output_file = tmp_path / "output.yaml"

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
            "-o",
            str(output_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        loaded_data = yaml.safe_load(output_file.read_text())
        assert loaded_data == {"target": "value"}

    def test_main_yaml_input_yaml_output(self, tmp_path) -> None:
        """Test YAML input with YAML output."""
        input_file = tmp_path / "input.yaml"
        input_data = {"source": "value"}
        input_file.write_text(yaml.safe_dump(input_data))

        mapping_file = tmp_path / "mapping.yaml"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(yaml.safe_dump(mapping_data))

        output_file = tmp_path / "output.yaml"

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
            "-o",
            str(output_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        loaded_data = yaml.safe_load(output_file.read_text())
        assert loaded_data == {"target": "value"}

    def test_main_mixed_formats(self, tmp_path) -> None:
        """Test YAML input with JSON mapping and YAML output."""
        input_file = tmp_path / "input.yaml"
        input_data = {"source": "value"}
        input_file.write_text(yaml.safe_dump(input_data))

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        output_file = tmp_path / "output.yaml"

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
            "-o",
            str(output_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        loaded_data = yaml.safe_load(output_file.read_text())
        assert loaded_data == {"target": "value"}

    def test_main_yaml_stdout(self, tmp_path, capsys) -> None:
        """Test --yaml flag for stdout output."""
        input_file = tmp_path / "input.json"
        input_data = {"source": "value"}
        input_file.write_text(json.dumps(input_data))

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
            "--yaml",
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 0
        captured = capsys.readouterr()
        loaded_data = yaml.safe_load(captured.out)
        assert loaded_data == {"target": "value"}

    def test_main_invalid_yaml(self, tmp_path, capsys) -> None:
        """Test CLI with invalid YAML input."""
        input_file = tmp_path / "input.yaml"
        input_file.write_text("invalid: yaml: content: [")

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "Invalid YAML" in captured.err

    def test_main_unsupported_extension(self, tmp_path, capsys) -> None:
        """Test CLI with unsupported file extension."""
        input_file = tmp_path / "input.xml"
        input_file.write_text('{"key": "value"}')

        mapping_file = tmp_path / "mapping.json"
        mapping_data = {"target": {"field": "source"}}
        mapping_file.write_text(json.dumps(mapping_data))

        test_args = [
            "json-mapper",
            str(input_file),
            "-m",
            str(mapping_file),
        ]

        with patch.object(sys, "argv", test_args):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "Unsupported file format" in captured.err
