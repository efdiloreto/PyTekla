import re


def is_pascal_case(s):
    """
    Check if a string is in PascalCase.

    PascalCase is a naming convention where each word is capitalized, with no spaces or underscores between words.

    Parameters
    ----------
    s : str
        The string to be checked.

    Returns
    -------
    bool
        True if the string is in PascalCase, False otherwise.

    """
    pattern = re.compile(r"^[A-Z][a-zA-Z]*$")
    return bool(pattern.match(s))


def to_pascal_case(snake_str):
    """
    Convert a snake_case string to PascalCase.

    PascalCase is a naming convention where each word is capitalized, with no spaces or underscores between words.

    Parameters
    ----------
    snake_str : str
        The snake_case string to be converted.

    Returns
    -------
    str
        The converted PascalCase string.

    Examples
    --------
    >>> to_pascal_case("first_name")
    "FirstName"

    """
    if is_pascal_case(snake_str):
        return snake_str
    components = snake_str.split("_")
    return "".join(x.title() for x in components)
