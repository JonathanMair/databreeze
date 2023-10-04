from dirty_dictionary.parser import holey_parsing, holey_nested_parsing

import random
from typing import Dict, List, Any
import lorem
import yaml

def parse_hard(list_: List, key: int) -> List:
    out_ = []
    for i in list_:
        if key in i.keys():
            out_.append(i[key])
        else:
            out_.append(None)
    return out_

def parse_hard_2_deep(list_: List, keys_: Any) -> List:
    out_ = []
    for i in list_:
        if keys_[0] in i.keys():
            if keys_[1] in i[keys_[0]].keys():
                out_.append(i[keys_[0]][keys_[1]])
            else:
                out_.append(None)
        else:
            out_.append(None)
    return out_


def get_dummy_dict() -> Dict:
    keys = list(range(1, 11))
    length = random.randint(1,10)
    present = random.sample(keys, length)
    dict_ = {k: lorem.sentence() for k in present}
    return dict_


def get_dummy_dict_2_deep() -> Dict:
    keys = list(range(1, 11))
    length = random.randint(1, 10)
    present = random.sample(keys, length)
    dict_ = {k: get_dummy_dict() for k in present}
    return dict_


def get_dummy_list() -> List:
    length = random.randint(10, 10)
    list_ = [get_dummy_dict() for _ in range(0, length +1)]
    return list_


def get_dummy_list_2_deep() -> List:
    length = random.randint(10, 10)
    list_ = [get_dummy_dict_2_deep() for _ in range(0, length +1)]
    return list_


def test_without_lambda():
    dummy = get_dummy_list()
    key = random.randint(1, 10)
    out_ = holey_parsing(dummy, key)
    should_be = parse_hard(dummy, key)
    assert out_ == should_be


def test_2_deep():
    keys = [random.randint(1, 10), random.randint(1, 10)]
    dummy = get_dummy_list_2_deep()
    out_ = holey_nested_parsing(dummy, keys)
    should_be = parse_hard_2_deep(dummy, keys)
    assert out_ == should_be
