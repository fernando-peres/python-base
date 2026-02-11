#!/usr/bin/env python3
"""
Switch between different environment configuration files.

This script copies the content of environment-specific files (.env.dev, .env.local,
.env.stage, .env.prd) to the main .env file, allowing you to switch between
different environment configurations.

Usage:
    python scripts/switch_env.py --dev    # Switch to development environment
    python scripts/switch_env.py --local  # Switch to local environment
    python scripts/switch_env.py --stage   # Switch to staging environment
    python scripts/switch_env.py --prd     # Switch to production environment
"""

import argparse
import shutil
import sys
from pathlib import Path

# Add project root to path so "service" package can be imported
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from service.shared.terminal_colors import ColorCode, coloring  # noqa: E402


def get_project_root() -> Path:
    """Get the project root directory."""
    # This script is in scripts/, so go up one level
    return Path(__file__).parent.parent


def print_fenced_message(message: str, detail: str = "") -> None:
    """
    Print a message inside a colored square border.

    Args:
        message: Main message to display
        detail: Optional detail message to display below the main message
    """

    # Calculate the width needed for the box (longest line + padding)
    # Account for emoji/wide characters that may take 2 display columns
    def get_display_width(text: str) -> int:
        """Estimate display width, accounting for wide characters like emojis."""
        width = 0
        for char in text:
            code = ord(char)
            # Emojis and wide Unicode characters take 2 display columns
            # Check for emoji ranges and other wide characters
            if (
                (0x1F300 <= code <= 0x1F9FF)
                or (0x1F600 <= code <= 0x1F64F)
                or (0x2700 <= code <= 0x27BF)
                or (0x1F900 <= code <= 0x1F9FF)
                or (code > 0x1F000 and code < 0x1FA00)
            ):
                width += 2
            else:
                width += 1
        return width

    lines = [message]
    if detail:
        lines.append(detail)
    # Use display width instead of character count for better alignment
    max_width = max(get_display_width(line) for line in lines)
    box_width = max_width + 16  # 8 spaces padding on each side for better spacing

    # Box drawing characters
    top_left = "╔"
    top_right = "╗"
    bottom_left = "╚"
    bottom_right = "╝"
    horizontal = "═"
    vertical = "║"
    space = " "

    # Use green colors for success
    border_color = ColorCode.BRIGHT_GREEN_TXT
    text_color = ColorCode.LIGHT_GREEN_TXT

    # Print top border
    top_border = top_left + (horizontal * (box_width - 2)) + top_right
    print(coloring(top_border, border_color))

    # Print empty line for spacing
    empty_line = vertical + (space * (box_width - 2)) + vertical
    print(coloring(empty_line, border_color))

    # Print message line
    # Use display width for padding calculation to account for emoji width
    message_display_width = get_display_width(message)
    message_padding = box_width - message_display_width - 2
    # Use equal padding, rounding down if odd (extra space will be on right)
    left_pad = message_padding // 2
    right_pad = message_padding - left_pad
    colored_border = coloring(vertical, border_color)
    colored_message = coloring(message, text_color)
    colored_spaces_left = space * left_pad
    colored_spaces_right = space * right_pad
    print(
        f"{colored_border}{colored_spaces_left}{colored_message}{colored_spaces_right}{colored_border}"
    )

    # Print detail line if provided
    if detail:
        # Use display width for padding calculation
        detail_display_width = get_display_width(detail)
        detail_padding = box_width - detail_display_width - 2
        # Use equal padding, rounding down if odd (extra space will be on right)
        left_pad_detail = detail_padding // 2
        right_pad_detail = detail_padding - left_pad_detail
        colored_detail = coloring(detail, text_color)
        colored_spaces_left_detail = space * left_pad_detail
        colored_spaces_right_detail = space * right_pad_detail
        print(
            f"{colored_border}{colored_spaces_left_detail}{colored_detail}{colored_spaces_right_detail}{colored_border}"
        )

    # Print empty line for spacing
    print(coloring(empty_line, border_color))

    # Print bottom border
    bottom_border = bottom_left + (horizontal * (box_width - 2)) + bottom_right
    print(coloring(bottom_border, border_color))


def switch_environment(env_type: str) -> None:
    """
    Copy the specified environment file to .env.

    Args:
        env_type: One of 'dev', 'local', 'stage', 'prd'

    Raises:
        FileNotFoundError: If the source environment file doesn't exist
        SystemExit: If the copy operation fails
    """
    project_root = get_project_root()
    source_file = project_root / f".env.{env_type}"
    target_file = project_root / ".env"

    # Check if source file exists
    if not source_file.exists():
        print(f"❌ Error: Environment file '{source_file.name}' not found.", file=sys.stderr)
        print(f"   Please create '{source_file.name}' in the project root.", file=sys.stderr)
        sys.exit(1)

    # Copy source to target
    try:
        shutil.copy2(source_file, target_file)
        print()  # Add spacing before the fence
        print_fenced_message(
            f"✅ Successfully switched to {env_type} environment",
            f"Copied {source_file.name} → .env",
        )
        print()  # Add spacing after the fence
    except Exception as e:
        print(f"❌ Error copying {source_file.name} to .env: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Switch between different environment configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/switch_env.py --dev    # Switch to development environment
  python scripts/switch_env.py --local  # Switch to local environment
  python scripts/switch_env.py --stage   # Switch to staging environment
  python scripts/switch_env.py --prd     # Switch to production environment
        """,
    )

    # Create mutually exclusive group for environment flags
    env_group = parser.add_mutually_exclusive_group(required=True)
    env_group.add_argument(
        "--dev",
        action="store_const",
        const="dev",
        dest="env_type",
        help="Switch to development environment (.env.dev)",
    )
    env_group.add_argument(
        "--local",
        action="store_const",
        const="local",
        dest="env_type",
        help="Switch to local environment (.env.local)",
    )
    env_group.add_argument(
        "--stage",
        action="store_const",
        const="stage",
        dest="env_type",
        help="Switch to staging environment (.env.stage)",
    )
    env_group.add_argument(
        "--prd",
        action="store_const",
        const="prd",
        dest="env_type",
        help="Switch to production environment (.env.prd)",
    )

    args = parser.parse_args()
    switch_environment(args.env_type)


if __name__ == "__main__":
    main()
