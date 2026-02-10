"""

This module contains the functions to interact with the Todoist API.

"""


class ColorCode:
    """
    ANSI escape codes for terminal text coloring.
    These codes can be used to change the color of text and background in terminal output.
    """

    RESET = "\033[0m"

    # Red
    LIGHT_RED_TXT = "\033[91m"
    LIGHT_RED_BG = "\033[48;5;217m\033[30m"
    DARK_RED_TXT = "\033[1;91m"
    DARK_RED_BG = "\033[48;5;88m\033[30m"
    BRIGHT_RED_TXT = "\033[91;1m"
    BRIGHT_RED_BG = "\033[48;5;197m\033[30m"
    BOLDARK_RED_TXT = "\033[1;91m"
    BOLDARK_RED_BG = "\033[48;5;197m\033[30;1m"

    # Green
    LIGHT_GREEN_TXT = "\033[92m"
    LIGHT_GREEN_BG = "\033[48;5;157m\033[30m"
    DARK_GREEN_TXT = "\033[1;92m"
    DARK_GREEN_BG = "\033[48;5;22m\033[30m"
    BRIGHT_GREEN_TXT = "\033[92;1m"
    BRIGHT_GREEN_BG = "\033[48;5;34m\033[30m"

    # Cyan
    LIGHT_CYAN_TXT = "\033[96m"
    LIGHT_CYAN_BG = "\033[48;5;159m\033[30m"
    DARK_CYAN_TXT = "\033[1;96m"
    DARK_CYAN_BG = "\033[48;5;31m\033[30m"
    BRIGHT_CYAN_TXT = "\033[96;1m"
    BRIGHT_CYAN_BG = "\033[48;5;51m\033[30m"

    # Yellow
    LIGHT_YELLOW_TXT = "\033[93m"
    LIGHT_YELLOW_BG = "\033[48;5;226m\033[30m"
    DARK_YELLOW_TXT = "\033[1;93m"
    DARK_YELLOW_BG = "\033[48;5;184m\033[30m"
    BRIGHT_YELLOW_TXT = "\033[93;1m"
    BRIGHT_YELLOW_BG = "\033[48;5;226m\033[30m"

    # Blue
    LIGHT_BLUE_TXT = "\033[94m"
    LIGHT_BLUE_BG = "\033[48;5;153m\033[30m"
    DARK_BLUE_TXT = "\033[1;94m"
    DARK_BLUE_BG = "\033[48;5;17m\033[30m"
    BRIGHT_BLUE_TXT = "\033[94;1m"
    BRIGHT_BLUE_BG = "\033[48;5;20m\033[30m"

    # Magenta
    LIGHT_MAGENTA_TXT = "\033[95m"
    LIGHT_MAGENTA_BG = "\033[48;5;207m\033[30m"
    DARK_MAGENTA_TXT = "\033[1;95m"
    DARK_MAGENTA_BG = "\033[48;5;54m\033[30m"
    BRIGHT_MAGENTA_TXT = "\033[95;1m"
    BRIGHT_MAGENTA_BG = "\033[48;5;127m\033[30m"

    # Orange
    LIGHT_ORANGE_TXT = "\033[38;5;208m"
    LIGHT_ORANGE_BG = "\033[48;5;208m\033[30m"
    DARK_ORANGE_TXT = "\033[38;5;166m"
    DARK_ORANGE_BG = "\033[48;5;166m\033[30m"
    BRIGHT_ORANGE_TXT = "\033[38;5;214m"
    BRIGHT_ORANGE_BG = "\033[48;5;214m\033[30m"

    # White
    LIGHT_WHITE_TXT = "\033[97m"
    LIGHT_WHITE_BG = "\033[48;5;231m\033[30m"
    DARK_WHITE_TXT = "\033[1;97m"
    DARK_WHITE_BG = "\033[48;5;231m\033[30;1m"

    # Light Gray
    LIGHT_GRAY_TXT = "\033[37m"
    LIGHT_GRAY_BG = "\033[48;5;251m\033[30m"

    # Black
    LIGHT_BLACK_TXT = "\033[30m"
    LIGHT_BLACK_BG = "\033[48;5;0m\033[30m"
    DARK_BLACK_TXT = "\033[1;30m"
    DARK_BLACK_BG = "\033[48;5;238m\033[30;1m"


def coloring(text: str, code: str = ColorCode.LIGHT_CYAN_TXT) -> str:
    """
    Return the text wrapped in the given color code.
    Args:
        text (str): The text to be colored.
        code (str): The ANSI color code to apply.
    Returns:
        str: The text wrapped in the given color code.
    """
    r_text = f"{code}{text}{ColorCode.RESET}"
    try:
        return r_text.encode("utf-8").decode("utf-8")
    except UnicodeDecodeError:
        return text


if __name__ == "__main__":
    print(f"{ColorCode.LIGHT_RED_TXT}Light Red Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_RED_BG}Light Red Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_RED_TXT}Dark Red Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_RED_BG}Dark Red Background{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_RED_TXT}Bright Red Text{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_RED_BG}Bright Red Background{ColorCode.RESET}")
    print(f"{ColorCode.BOLDARK_RED_TXT}Bold Red Text{ColorCode.RESET}")
    print(f"{ColorCode.BOLDARK_RED_BG}Bold Red Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_GREEN_TXT}Light Green Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_GREEN_BG}Light Green Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_GREEN_TXT}Dark Green Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_GREEN_BG}Dark Green Background{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_GREEN_TXT}Bright Green Text{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_GREEN_BG}Bright Green Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_CYAN_TXT}Light Cyan Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_CYAN_BG}Light Cyan Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_CYAN_TXT}Dark Cyan Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_CYAN_BG}Dark Cyan Background{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_CYAN_TXT}Bright Cyan Text{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_CYAN_BG}Bright Cyan Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_YELLOW_TXT}Light Yellow Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_YELLOW_BG}Light Yellow Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_YELLOW_TXT}Dark Yellow Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_YELLOW_BG}Dark Yellow Background{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_YELLOW_TXT}Bright Yellow Text{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_YELLOW_BG}Bright Yellow Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_BLUE_TXT}Light Blue Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_BLUE_BG}Light Blue Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_BLUE_TXT}Dark Blue Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_BLUE_BG}Dark Blue Background{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_BLUE_TXT}Bright Blue Text{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_BLUE_BG}Bright Blue Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_MAGENTA_TXT}Light Magenta Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_MAGENTA_BG}Light Magenta Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_MAGENTA_TXT}Dark Magenta Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_MAGENTA_BG}Dark Magenta Background{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_MAGENTA_TXT}Bright Magenta Text{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_MAGENTA_BG}Bright Magenta Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_ORANGE_TXT}Light Orange Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_ORANGE_BG}Light Orange Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_ORANGE_TXT}Dark Orange Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_ORANGE_BG}Dark Orange Background{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_ORANGE_TXT}Bright Orange Text{ColorCode.RESET}")
    print(f"{ColorCode.BRIGHT_ORANGE_BG}Bright Orange Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_WHITE_TXT}Light White Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_WHITE_BG}Light White Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_WHITE_TXT}Dark White Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_WHITE_BG}Dark White Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_GRAY_TXT}Light Gray Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_GRAY_BG}Light Gray Background{ColorCode.RESET}")

    print(f"{ColorCode.LIGHT_BLACK_TXT}Light Black Text{ColorCode.RESET}")
    print(f"{ColorCode.LIGHT_BLACK_BG}Light Black Background{ColorCode.RESET}")
    print(f"{ColorCode.DARK_BLACK_TXT}Dark Black Text{ColorCode.RESET}")
    print(f"{ColorCode.DARK_BLACK_BG}Dark Black Background{ColorCode.RESET}")
