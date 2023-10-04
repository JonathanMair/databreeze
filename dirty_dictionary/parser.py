# Programmatically accessing arbitrarily deeply-nested values in a dictionary:
# https://stackoverflow.com/questions/30648317/programmatically-accessing-arbitrarily-deeply-nested-values-in-a-dictionary


from typing import List, Dict, Any, Optional


# TODO: this would make a good python library for quick and dirty data processing... function that takes list and
# builds a list comprehension that automatically does this...
# function to provide _NONE value when attempts to dig into the dict fail for a given record, e.g. because the field
# doesn't exist for that record


def _catch(func, value_if_none: Optional[Any] = None) -> Any:
    try:
        return func()
    except Exception as e:
        return value_if_none


def _value_by_arbitrary_nested_keys(dict_: Dict, keys_: List) -> Any:
    out_ = dict_
    for key in keys_:
        out_ = _catch(lambda: out_[key])
    return out_


def holey_parsing(list_: List[Dict], key: Any, value_if_none: Optional[Any] = None) -> List[Any]:
    return [_catch(lambda: x[key], value_if_none) for x in list_]


def holey_nested_parsing(list_: List[Dict], keys_: List[Any], value_if_none: Optional[Any] = None) -> List[Any]:
    return [_value_by_arbitrary_nested_keys(l, keys_) for l in list_]


