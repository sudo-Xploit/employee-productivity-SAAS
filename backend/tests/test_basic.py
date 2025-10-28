"""
Basic tests that don't require complex fixtures or database access.
"""
import pytest


def test_addition():
    """Simple test to verify pytest is working"""
    assert 1 + 1 == 2


def test_string_operations():
    """Test basic string operations"""
    assert "hello" + " " + "world" == "hello world"
    assert "hello".upper() == "HELLO"
    assert "WORLD".lower() == "world"


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (2, 4),
        (3, 9),
        (4, 16),
        (5, 25),
    ]
)
def test_square(input_value, expected):
    """Test squaring numbers with parameterization"""
    assert input_value ** 2 == expected
