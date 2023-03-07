import pytest
from System import Array
from System.Collections import ArrayList, Hashtable
from System.Collections.Generic import Dictionary, List

from pytekla.coreutils.collections import (
    iterable_to_net_array,
    iterable_to_net_array_list,
    iterable_to_net_list,
    net_idictionary_to_dict,
)


def test_net_idictionary_to_dict():
    ht = Hashtable()
    ht["key1"] = "value1"
    ht["key2"] = 42
    ht["key3"] = 3.14

    expected_dict_ht = {"key1": "value1", "key2": 42, "key3": 3.14}
    actual_dict_ht = net_idictionary_to_dict(ht)
    assert actual_dict_ht == expected_dict_ht

    net_dict = Dictionary[str, int]()
    net_dict.Add("key1", 1)
    net_dict.Add("key2", 2)
    net_dict.Add("key3", 3)

    expected_dict = {"key1": 1, "key2": 2, "key3": 3}
    actual_dict = net_idictionary_to_dict(net_dict)
    assert actual_dict == expected_dict


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ([1, 2, 3], [1, 2, 3]),
        (["foo", "bar"], ["foo", "bar"]),
        ((4.5, 6.7), [4.5, 6.7]),
    ],
)
def test_iterable_to_net_array_list(test_input, expected_output):
    result = iterable_to_net_array_list(test_input)
    assert isinstance(result, ArrayList)
    assert list(result) == expected_output


@pytest.mark.parametrize(
    "input_iterable, error_type, element_type",
    [
        ([1, 2, 3], None, int),
        (["foo", "bar", "baz"], None, str),
        ((4.5, 6.7), None, float),
        ([], IndexError, None),
        ({"a": 1, "b": 2}, None, str),
        ((1, 2, 3), None, int),
        (("foo", 3, 6.73), TypeError, str),
    ],
)
def test_iterable_to_net_list(input_iterable, error_type, element_type):
    if error_type is not None:
        with pytest.raises(error_type):
            iterable_to_net_list(input_iterable)
    else:
        expected_list = List[element_type]()
        result_list = iterable_to_net_list(input_iterable)
        assert result_list.GetType() == expected_list.GetType()
        assert all(isinstance(item, element_type) for item in result_list)
        assert len(input_iterable) == result_list.Count


@pytest.mark.parametrize(
    "input_list, expected_array, error_type, element_type",
    [
        ([1, 2, 3], Array[int]([1, 2, 3]), None, int),
        (["foo", "bar", "baz"], Array[str](["foo", "bar", "baz"]), None, str),
        ((4.5, 6.7), Array[float]([4.5, 6.7]), None, float),
        ([], None, IndexError, None),
        ({"a": 1, "b": 2}, Array[str](["a", "b"]), None, str),
        ((1, 2, 3), Array[int]([1, 2, 3]), None, int),
    ],
)
def test_iterable_to_net_array(input_list, expected_array, error_type, element_type):
    if error_type is not None:
        with pytest.raises(error_type):
            iterable_to_net_array(input_list)
    else:
        result_array = iterable_to_net_array(input_list)
        assert result_array.GetType() == expected_array.GetType()
        assert all(isinstance(item, element_type) for item in result_array)
        assert list(result_array) == list(input_list)
