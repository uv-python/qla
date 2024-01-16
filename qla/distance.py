from .matrix import Matrix, distance as __mm_distance, max_distance as __mm_max_distance
from .vector import Vector, distance as __vv_distance, max_distance as __vv_max_distance
from dyn_dispatch import dyn_dispatch_f, dyn_fun


"""Compute max distance between elements
Args:
    e1 (Vector | Matrix): Vector or Matrix instance
    e2 (Vector | Matrix): Vector or Matrix instance
Returns:
    max distance between elements
"""


@dyn_fun
def distance(*_) -> float:
    ...


@dyn_fun
def max_distance(*_) -> float:
    ...


@dyn_dispatch_f("distance", Vector, Vector)
def vv_distance(v1: Vector, v2: Vector) -> float:
    return __vv_distance(v1, v2)


@dyn_dispatch_f("distance", Matrix, Matrix)
def mm_distance(v1: Vector, v2: Vector) -> float:
    return __mm_distance(v1, v2)


@dyn_dispatch_f("max_distance", Vector, Vector)
def vv_max_distance(v1: Vector, v2: Vector) -> float:
    return __vv_max_distance(v1, v2)


@dyn_dispatch_f("max_distance", Matrix, Matrix)
def mm_max_distance(v1: Vector, v2: Vector) -> float:
    return __mm_max_distance(v1, v2)
