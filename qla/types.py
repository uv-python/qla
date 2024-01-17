"""
Type used in Vector and Matrix types.
"""
from typing import List
from typing import TypeVar, Generic

T = TypeVar("T")

Elem = float | complex | int
Array = list[T]
Array2D = list[list[T]]  # [Array]


def default(t) -> float | int | complex:
    """Return default value for type
    Args:
        t (type): float, int or complex
    Returns:
        default value (0, 0.0 or 0 + 0j)
    Raises:
        TypeError if type name not float, int or complex
    """
    if t == int:
        return 0
    elif t == float:
        return 0.0
    elif t == complex:
        return 0 + 0j
    else:
        raise TypeError("Wrong type: Only int, float or complex allowed")


def neutral_element_sum(t) -> float | int | complex:
    """Return neutral element (zero) value for the sum operation
    Args:
        t (type): float, int or complex
    Returns:
        neutral element for sum: 0, 0.0 or 0 + 0j
    Raises:
        TypeError if type name not float, int or complex
    """
    if t == int:
        return 0
    elif t == float:
        return 0.0
    elif t == complex:
        return 0 + 0j
    else:
        raise TypeError("Wrong type: Only int, float or complex allowed")


def neutral_element_mul(t) -> float | int | complex:
    """Return neutral element (zero) value for the multily operation
    Args:
        t (type): float, int or complex
    Returns:
        neutral element for sum: 1, 1.0 or 1. + 0j
    Raises:
        TypeError if type name not float, int or complex
    """
    if t == int:
        return 0
    elif t == float:
        return 0.0
    elif t == complex:
        return 0 + 0j
    else:
        raise TypeError("Wrong type: Only int, float or complex allowed")


def identity(t) -> float | int | complex:
    """Return identiy element (1)
    Args:
        t (type): float, int or complex
    Returns:
        neutral element for sum: 1, 1.0 or 1. + 0j
    Raises:
        TypeError if type name not float, int or complex
    """
    return neutral_element_mul(t)
