#!/usr/bin/env python3
"""
Script to list all loggers used in the application.

This script scans all Python files in the src directory and identifies:
- logging.getLogger() calls with their logger names
- Logger variable assignments
- Logger method calls (info, error, warning, debug, critical)
- get_logger() function calls
"""

import ast
from pathlib import Path
from typing import Any


class LoggerFinder(ast.NodeVisitor):
    """AST visitor to find all logger-related code."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.loggers: set[str] = set()
        self.logger_vars: set[str] = set()
        self.logger_calls: list[dict[str, Any]] = []
        self.get_logger_calls: list[dict[str, Any]] = []

    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls to find logging.getLogger() and logger method calls."""
        # Check for logging.getLogger() calls
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "logging":
                if node.func.attr == "getLogger":
                    if node.args and isinstance(node.args[0], ast.Constant):
                        logger_name = node.args[0].value
                        self.loggers.add(logger_name)
                        self.logger_calls.append(
                            {
                                "type": "getLogger",
                                "name": logger_name,
                                "line": node.lineno,
                                "file": str(self.file_path),
                            }
                        )
                    elif node.args and isinstance(node.args[0], ast.Name):
                        # Variable-based logger name
                        var_name = node.args[0].id
                        self.loggers.add(f"<variable: {var_name}>")
                        self.logger_calls.append(
                            {
                                "type": "getLogger",
                                "name": f"<variable: {var_name}>",
                                "line": node.lineno,
                                "file": str(self.file_path),
                            }
                        )

        # Check for get_logger() calls
        if isinstance(node.func, ast.Name) and node.func.id == "get_logger":
            self.get_logger_calls.append(
                {
                    "type": "get_logger",
                    "line": node.lineno,
                    "file": str(self.file_path),
                }
            )

        # Check for logger method calls (logger.info, logger.error, etc.)
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                var_name = node.func.value.id
                if "logger" in var_name.lower():
                    method_name = node.func.attr
                    if method_name in ["info", "error", "warning", "debug", "critical", "exception"]:
                        self.logger_calls.append(
                            {
                                "type": "logger_method",
                                "method": method_name,
                                "variable": var_name,
                                "line": node.lineno,
                                "file": str(self.file_path),
                            }
                        )

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignments to find logger variable assignments."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                if "logger" in var_name.lower():
                    self.logger_vars.add(var_name)
                    # Check if it's assigned from getLogger or get_logger
                    if isinstance(node.value, ast.Call):
                        if isinstance(node.value.func, ast.Attribute):
                            if (
                                isinstance(node.value.func.value, ast.Name)
                                and node.value.func.value.id == "logging"
                                and node.value.func.attr == "getLogger"
                            ):
                                if (
                                    node.value.args
                                    and isinstance(node.value.args[0], ast.Constant)
                                ):
                                    logger_name = node.value.args[0].value
                                    self.loggers.add(logger_name)
        self.generic_visit(node)


def find_loggers_in_file(file_path: Path) -> LoggerFinder:
    """Parse a Python file and find all logger usage."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        finder = LoggerFinder(file_path)
        finder.visit(tree)
        return finder
    except SyntaxError as e:
        print(f"Warning: Could not parse {file_path}: {e}")
        return LoggerFinder(file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return LoggerFinder(file_path)


def main() -> None:
    """Main function to scan all Python files and list loggers."""
    # Get the project root (assuming script is in scripts/)
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    if not src_dir.exists():
        print(f"Error: Source directory not found at {src_dir}")
        return

    all_loggers: set[str] = set()
    all_logger_vars: set[str] = set()
    all_logger_calls: list[dict[str, Any]] = []
    all_get_logger_calls: list[dict[str, Any]] = []

    # Find all Python files
    python_files = list(src_dir.rglob("*.py"))

    print(f"Scanning {len(python_files)} Python files...\n")
    print("=" * 80)

    for py_file in sorted(python_files):
        finder = find_loggers_in_file(py_file)
        if finder.loggers or finder.logger_vars or finder.logger_calls or finder.get_logger_calls:
            all_loggers.update(finder.loggers)
            all_logger_vars.update(finder.logger_vars)
            all_logger_calls.extend(finder.logger_calls)
            all_get_logger_calls.extend(finder.get_logger_calls)

    # Print results
    print("\n📋 LOGGER NAMES FOUND:")
    print("=" * 80)
    if all_loggers:
        for logger_name in sorted(all_loggers):
            print(f"  • {logger_name}")
    else:
        print("  (none found)")

    print("\n📝 LOGGER VARIABLES FOUND:")
    print("=" * 80)
    if all_logger_vars:
        for var_name in sorted(all_logger_vars):
            print(f"  • {var_name}")
    else:
        print("  (none found)")

    print("\n🔍 get_logger() FUNCTION CALLS:")
    print("=" * 80)
    if all_get_logger_calls:
        for call in all_get_logger_calls:
            print(f"  • {call['file']}:{call['line']}")
    else:
        print("  (none found)")

    print("\n📊 DETAILED LOGGER USAGE BY FILE:")
    print("=" * 80)

    # Group calls by file
    calls_by_file: dict[str, list[dict[str, Any]]] = {}
    for call in all_logger_calls:
        file_path = call["file"]
        if file_path not in calls_by_file:
            calls_by_file[file_path] = []
        calls_by_file[file_path].append(call)

    for file_path in sorted(calls_by_file.keys()):
        print(f"\n  📄 {file_path}")
        for call in calls_by_file[file_path]:
            if call["type"] == "getLogger":
                print(f"    Line {call['line']}: logging.getLogger('{call['name']}')")
            elif call["type"] == "logger_method":
                print(
                    f"    Line {call['line']}: {call['variable']}.{call['method']}()"
                )

    print("\n" + "=" * 80)
    print("\n📈 SUMMARY:")
    print(f"  • Unique logger names: {len(all_loggers)}")
    print(f"  • Logger variables: {len(all_logger_vars)}")
    print(f"  • get_logger() calls: {len(all_get_logger_calls)}")
    print(f"  • Total logger method calls: {len(all_logger_calls)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
