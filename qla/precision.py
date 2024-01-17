from .types import Elem


EPSILON = 1e-15


def is_zero(x: Elem) -> bool:
    """Returns true
    if elem is less than epsilon
    default is 1E-15
    Args:
        x (float | comples): number
    Returns:
        true if number is zero false otherwise"""
    return abs(x) < EPSILON  # works with complex too


def get_epsilon() -> float:
    """Get current threshold under which numbers are considered zeroes"""
    return EPSILON


def set_epsilon(eps: float):
    """Set number under which numbers are considered zeroes"""
    global EPSILON
    EPSILON = eps
