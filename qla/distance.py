"""
Distance functions.
"""
from .matrix import Matrix, distance as __mm_distance, max_distance as __mm_max_distance
from .vector import Vector, distance as __vv_distance, max_distance as __vv_max_distance
from dyn_dispatch import dyn_dispatch_f, dyn_fun


@dyn_fun
def distance(*_) -> float:
    """Compute distance between vectors or matrices by
    returning sqrt(vm1 - vm2) where vm1 and vm2 are
    two vectors or two matrices.
    Args:
        e1 (Vector | Matric): Vector of matrix instance
        e2 (Vector | Matric): Vector of matrix instance
    """
    return -1.0


@dyn_fun
def max_distance(*_) -> float:
    """Compute max distance between elements
    Args:
        e1 (Vector | Matrix): Vector or Matrix instance
        e2 (Vector | Matrix): Vector or Matrix instance
    Returns:
        max distance between elements
    """
    return -1.0


@dyn_dispatch_f("distance", Vector, Vector)
def vv_distance(v1: Vector, v2: Vector) -> float:
    return __vv_distance(v1, v2)


@dyn_dispatch_f("distance", Matrix, Matrix)
def mm_distance(v1: Matrix, v2: Matrix) -> float:
    return __mm_distance(v1, v2)


@dyn_dispatch_f("max_distance", Vector, Vector)
def vv_max_distance(v1: Vector, v2: Vector) -> float:
    return __vv_max_distance(v1, v2)


@dyn_dispatch_f("max_distance", Matrix, Matrix)
def mm_max_distance(v1: Matrix, v2: Matrix) -> float:
    return __mm_max_distance(v1, v2)
