"""Text processing utilities."""


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def sanitize_smiles(smiles: str) -> str:
    """
    Basic sanitization of SMILES string.

    Args:
        smiles: SMILES string to sanitize

    Returns:
        Sanitized SMILES string
    """
    # Remove leading/trailing whitespace
    sanitized = smiles.strip()

    # Remove any newlines or tabs
    sanitized = sanitized.replace("\n", "").replace("\t", "").replace("\r", "")

    return sanitized


def format_step_number(number: int, total: int) -> str:
    """
    Format a step number with appropriate padding.

    Args:
        number: Current step number
        total: Total number of steps

    Returns:
        Formatted step string
    """
    width = len(str(total))
    return f"Step {number:0{width}d}/{total}"
