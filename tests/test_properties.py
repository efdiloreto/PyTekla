import pytest

from pytekla.coreutils.properties import check_property_type


def test_check_property_type():
    check_property_type(str)
    check_property_type(int)
    check_property_type(float)

    with pytest.raises(TypeError):
        assert check_property_type(list)
