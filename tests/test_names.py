import pytest

from pytekla.coreutils.names import is_pascal_case, to_pascal_case


def test_is_pascal_case():
    assert is_pascal_case("MyVariableName") == True
    assert is_pascal_case("My_variable_name") == False
    assert is_pascal_case("myVariableName") == False
    assert is_pascal_case("my_variable_name") == False
    assert is_pascal_case("") == False
    assert is_pascal_case("123") == False
    assert is_pascal_case("123MyVariable") == False
    assert is_pascal_case("MyVariable123") == False
    assert is_pascal_case("MyVariable_Name") == False


def test_to_pascal_case():
    assert to_pascal_case("first_name") == "FirstName"
    assert to_pascal_case("snake_case_example") == "SnakeCaseExample"
    assert to_pascal_case("my_long_variable_name") == "MyLongVariableName"
    assert to_pascal_case("camel_case") == "CamelCase"
    assert to_pascal_case("alllowercase") == "Alllowercase"
    assert to_pascal_case("ALL_UPPERCASE") == "AllUppercase"
    assert to_pascal_case("_leading_underscore") == "LeadingUnderscore"
    assert to_pascal_case("trailing_underscore_") == "TrailingUnderscore"
    assert to_pascal_case("__double_underscore__") == "DoubleUnderscore"
