import os

import clr
import pytest
from System.Collections import Hashtable
from System.Collections.Generic import Dictionary



def _create_net_idict(keys, values, hashtable=False):
    if hashtable:
        net_idict = Hashtable()
    net_idict = Dictionary(str, values[0])()
    for key, value in zip(keys, value):
        net_idict.Add(key, value)
    return net_idict


@pytest.fixture
def net_dictionary_int():
    return _create_net_idict(["key1", "key2", "key3"], [1, 2, 3])


@pytest.fixture
def net_dictionary_str():
    return _create_net_idict(["key1", "key2", "key3"], ["value1", "value2", "value3"])


@pytest.fixture
def net_dictionary_float():
    return
