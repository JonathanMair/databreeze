"""`fillna`for dictionaries: provides methods that assist in parsing dictionaries and lists of dictionaries.
When the user tries to get a value using a key that does not exist in a given dictionary, the exception is caught
and `None`or an arbitrary `fillna`value is provided. Eliminates the need for repeated exception catching when parsing
lists of dictionaries, e.g. when processing data from json."""


from typing import List, Dict, Any, Optional, Union


# Ref: Stackoverflow: How to handle exceptions in a list comprehensions?
# https://stackoverflow.com/a/8915613
def _fill_exceptions(func, value_if_none: Optional[Any] = None, *args, **kwargs) -> Any:
    """Return the result of supplied function or if the function throws an error, either `None` or the value supplied.

    :param func: the function to be called
    :param value_if_none: the value to be returned in case of Exception, defaults to `None`
    :param args: optional arguments to `func`
    :param kwargs: optional keyword arguments to `func`
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return value_if_none


# Ref: Stackoverflow: Programmatically accessing arbitrarily deeply-nested values in a dictionary:
# https://stackoverflow.com/a/30648524/18331020
def _get_values_from_arbitrary_keys_fillna(data: Dict, keys_: List, value_if_none: Optional[Any] = None) -> Any:
    """Return a specific value stored in `dict_` an arbitrary number of nested levels deep

    :param data: a possibly nested dictionary from which to find the value
    :param keys_: the list of dictionary keys in hierarchical order that will be used to drill down into the data
    :param value_if_none: a value to be returned if any of the sequence of keys throws as KeyError, defaults to `None`
    """
    out_ = data
    for key in keys_:
        out_ = _fill_exceptions(lambda: out_[key], value_if_none)
    return out_


def drill(
        data: Union[List[Dict], Dict],
        keys_: Union[List[Any], Any],
        value_if_none: Optional[Any] = None
) -> List[Any]:
    """Iterates through a list of (possibly nested) dictionaries attempting to drill down to find a value using a list
    of hierarchical dictionary keys. Returns a list containing the values found, or, where any key in the chain is
    missing, a supplied default (defaults to `None`). Also works with a single dictionary, in which case it returns a
    single value.

    Usage
    -----

        Nested dictionaries: these have two levels, but could be any level of nesting:

        >>> d = {"name": "Tony", "contact": {"phone": 878787878, "city": "Madrid"}}
        >>> e = {"name": "Marta", "contact": {"city": "Madrid"}}

        Pass the possibly nested dictionary and the list of keys to the function and it will drill down:

        >>> drill(d, ["contact", "phone"])
        878787878

        >>> drill(d, ["name"])
        'Tony'

        If it reaches a point in the chain of keys where the key doesn't exist, the error is caught and
        `None`is returned

        >>> drill(e, ["contact", "phone"]) is None
        True

        Pass a list of dictionaries, get a list of values or `value_if_none` if the Key is missing:

        >>> drill([d, e], ["contact", "phone"], value_if_none="Missing Data")
        [878787878, 'Missing Data']

    :param data: dictionary or list of dictionaries in which the values are to be found
    :param keys_: list of hierarchically ordered keys that will be used to drill down to the desired value
    :param value_if_none: value to append to the list returned representing missing values, defaults to `None`
    :return: value or a list of values representing the result from each dictionary supplied in `data`
    """
    keys_ = keys_ if isinstance(keys_, list) else [keys_]
    return (
        [_get_values_from_arbitrary_keys_fillna(list_item, keys_, value_if_none) for list_item in data]
        if isinstance(data, list) else
        _get_values_from_arbitrary_keys_fillna(data, keys_, value_if_none)
    )



