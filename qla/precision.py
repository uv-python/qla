from .types import Elem


def is_zero(x: Elem):
    return abs(x) < 1e-9  # works with complex too
