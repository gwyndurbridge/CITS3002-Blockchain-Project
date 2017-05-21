"""
PrintStyle
"""

MONEY_BAG = u"\U0001F4B0"
BOLD = "\033[1m"
PURPLE = "\033[95m"
RESET = "\033[0m"


def title(input_string):
    """
    Returns title message with print style effects
    """
    output = "\n" + MONEY_BAG + BOLD + PURPLE + " "
    output += input_string
    output += " " + RESET + MONEY_BAG + "\n"
    return output
    