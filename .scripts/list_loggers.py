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

    def _record_get_logger_constant(self, node: ast.Call) -> None:
        """Record logging.getLogger(<constant>) and add to loggers if name is str."""
        if not node.args or not isinstance(node.args[0], ast.Constant):
            return
        logger_name = node.args[0].value
        if not isinstance(logger_name, str):
            return
        self.loggers.add(logger_name)
        self.logger_calls.append(
            {
                "type": "getLogger",
                "name": logger_name,
                "line": node.lineno,
                "file": str(self.file_path),
            }
        )

    def _record_get_logger_name(self, node: ast.Call) -> None:
        """Record logging.getLogger(<name>) variable-based logger."""
        if not node.args or not isinstance(node.args[0], ast.Name):
            return
        var_name = node.args[0].id
        name = f"<variable: {var_name}>"
        self.loggers.add(name)
        self.logger_calls.append(
            {
                "type": "getLogger",
                "name": name,
                "line": node.lineno,
                "file": str(self.file_path),
            }
        )

    def _record_logger_method(self, node: ast.Call) -> None:
        """Record logger method calls (logger.info, etc.) if matching method."""
        func = node.func
        if not isinstance(func, ast.Attribute) or not isinstance(func.value, ast.Name):
            return
        var_name = func.value.id
        if "logger" not in var_name.lower():
            return
        if func.attr not in (
            "info",
            "error",
            "warning",
            "debug",
            "critical",
            "exception",
        ):
            return
        self.logger_calls.append(
            {
                "type": "logger_method",
                "method": func.attr,
                "variable": var_name,
                "line": node.lineno,
                "file": str(self.file_path),
            }
        )

    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls to find logging.getLogger() and logger method calls."""
        is_get_logger = (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "logging"
            and node.func.attr == "getLogger"
        )
        if is_get_logger and node.args and isinstance(node.args[0], ast.Constant):
            self._record_get_logger_constant(node)
        elif is_get_logger and node.args and isinstance(node.args[0], ast.Name):
            self._record_get_logger_name(node)

        if isinstance(node.func, ast.Name) and node.func.id == "get_logger":
            self.get_logger_calls.append(
                {
                    "type": "get_logger",
                    "line": node.lineno,
                    "file": str(self.file_path),
                }
            )

        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            self._record_logger_method(node)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignments to find logger variable assignments."""
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            var_name = target.id
            if "logger" not in var_name.lower():
                continue
            self.logger_vars.add(var_name)
            if not isinstance(node.value, ast.Call) or not isinstance(
                node.value.func, ast.Attribute
            ):
                continue
            func_val = node.value.func.value
            if (
                isinstance(func_val, ast.Name)
                and func_val.id == "logging"
                and node.value.func.attr == "getLogger"
                and node.value.args
                and isinstance(node.value.args[0], ast.Constant)
            ):
                logger_name = node.value.args[0].value
                if isinstance(logger_name, str):
                    self.loggers.add(logger_name)
        self.generic_visit(node)


def find_loggers_in_file(file_path: Path) -> LoggerFinder:
    """Parse a Python file and find all logger usage."""
    try:
        with open(file_path, encoding="utf-8") as f:
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


def _collect_finder_results(
    python_files: list[Path],
) -> tuple[set[str], set[str], list[dict[str, Any]], list[dict[str, Any]]]:
    """Run finders on files and aggregate results."""
    all_loggers: set[str] = set()
    all_logger_vars: set[str] = set()
    all_logger_calls: list[dict[str, Any]] = []
    all_get_logger_calls: list[dict[str, Any]] = []
    for py_file in sorted(python_files):
        finder = find_loggers_in_file(py_file)
        if finder.loggers or finder.logger_vars or finder.logger_calls or finder.get_logger_calls:
            all_loggers.update(finder.loggers)
            all_logger_vars.update(finder.logger_vars)
            all_logger_calls.extend(finder.logger_calls)
            all_get_logger_calls.extend(finder.get_logger_calls)
    return all_loggers, all_logger_vars, all_logger_calls, all_get_logger_calls


def _group_calls_by_file(calls: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group logger calls by file path."""
    out: dict[str, list[dict[str, Any]]] = {}
    for call in calls:
        file_path = call["file"]
        if file_path not in out:
            out[file_path] = []
        out[file_path].append(call)
    return out


def _print_detailed_usage(calls_by_file: dict[str, list[dict[str, Any]]]) -> None:
    """Print per-file logger usage."""
    for file_path in sorted(calls_by_file.keys()):
        print(f"\n  📄 {file_path}")
        for call in calls_by_file[file_path]:
            if call["type"] == "getLogger":
                print(f"    Line {call['line']}: logging.getLogger('{call['name']}')")
            elif call["type"] == "logger_method":
                print(f"    Line {call['line']}: {call['variable']}.{call['method']}()")


def main() -> None:
    """Main function to scan all Python files and list loggers."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    if not src_dir.exists():
        print(f"Error: Source directory not found at {src_dir}")
        return

    python_files = list(src_dir.rglob("*.py"))
    print(f"Scanning {len(python_files)} Python files...\n")
    print("=" * 80)

    all_loggers, all_logger_vars, all_logger_calls, all_get_logger_calls = (
        _collect_finder_results(python_files)
    )

    print("\n📋 LOGGER NAMES FOUND:")
    print("=" * 80)
    for logger_name in sorted(all_loggers) if all_loggers else []:
        print(f"  • {logger_name}")
    if not all_loggers:
        print("  (none found)")

    print("\n📝 LOGGER VARIABLES FOUND:")
    print("=" * 80)
    for var_name in sorted(all_logger_vars) if all_logger_vars else []:
        print(f"  • {var_name}")
    if not all_logger_vars:
        print("  (none found)")

    print("\n🔍 get_logger() FUNCTION CALLS:")
    print("=" * 80)
    for call in all_get_logger_calls:
        print(f"  • {call['file']}:{call['line']}")
    if not all_get_logger_calls:
        print("  (none found)")

    print("\n📊 DETAILED LOGGER USAGE BY FILE:")
    print("=" * 80)
    _print_detailed_usage(_group_calls_by_file(all_logger_calls))

    print("\n" + "=" * 80)
    print("\n📈 SUMMARY:")
    print(f"  • Unique logger names: {len(all_loggers)}")
    print(f"  • Logger variables: {len(all_logger_vars)}")
    print(f"  • get_logger() calls: {len(all_get_logger_calls)}")
    print(f"  • Total logger method calls: {len(all_logger_calls)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
