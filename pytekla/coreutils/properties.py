def check_property_type(property_type):
    """
    Checks if the property type is one of [str, int, float].

    Parameters
    ----------
    property_type : type
        The type of the property.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If the property type is not one of [str, int, float].
    """
    if property_type not in (str, int, float):
        raise TypeError("'parameter_type' must be one of these type: [str, int, float]")
