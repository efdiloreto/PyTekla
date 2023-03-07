import warnings
from functools import wraps

from System import Array
from System.Collections import ArrayList
from System.Collections.Generic import List


def warn_if_set(func):
    """Warns if input iterable is a set.

    Parameters
    ----------
    func : function
        A function that takes in an iterable and returns a value.

    Returns
    -------
    wrapper : function
        A wrapper function that takes in an iterable and passes it to `func`.

    Warns
    -----
    UserWarning
        If the input iterable is a set, a warning will be issued indicating that sets are unordered collections.
    """

    @wraps(func)
    def wrapper(iterable):
        if isinstance(iterable, set):
            warnings.warn(
                "You are trying to convert a 'set'. Take in mind that sets are unorderer collections."
            )
        return func(iterable)

    return wrapper


def net_idictionary_to_dict(idictionary):
    """
    Convert a .NET IDictionary like object to a Python dictionary.

    Parameters
    ----------
    idictionary : System.Collections.IDictionary
        The IDictionary object to convert.

    Returns
    -------
    dict
        A dictionary with the same key-value pairs as the IDictionary object.
    """
    return {k: v for k, v in zip(idictionary.Keys, idictionary.Values)}


@warn_if_set
def iterable_to_net_array_list(iterable):
    """
    Convert a Python iterable to a .NET ArrayList.

    Parameters
    ----------
    iterable : iterable
        The sequence to convert.

    Returns
    -------
    System.Collections.ArrayList
        An ArrayList with the same elements as the sequence.
    """
    array_list = ArrayList()
    for x in iterable:
        array_list.Add(x)
    return array_list


@warn_if_set
def iterable_to_net_list(iterable):
    """
    Convert an iterable object to a .NET List.

    Parameters
    ----------
    iterable : Iterable
        The iterable object to be converted.

    Returns
    -------
    net_list : List
        The converted .NET List.

    Raises
    ------
    TypeError
        If the input iterable contains elements of different types.
    IndexError
        If the input iterable is empty.
    """
    list_iterable = list(iterable)
    net_list = List[type(list_iterable[0])]()
    for item in list_iterable:
        net_list.Add(item)

    return net_list


@warn_if_set
def iterable_to_net_array(iterable):
    """
    Convert an iterable object to a .NET Array.

    Parameters
    ----------
    iterable : Iterable
        The iterable object to be converted.

    Returns
    -------
    net_array : Array
        The converted .NET Array.

    Raises
    ------
    TypeError
        If the input iterable is empty or contains elements of different types.

    """
    list_iterable = list(iterable)
    net_array = Array[type(list_iterable[0])](list_iterable)

    return net_array


__all__ = [
    "net_idictionary_to_dict",
    "iterable_to_net_array_list",
    "iterable_to_net_list",
    "iterable_to_net_array",
]
