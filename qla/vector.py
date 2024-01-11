from __future__ import annotations
from dataclasses import dataclass
from dyn_dispatch import dyn_dispatch, dyn_dispatch_f, dyn_method, dyn_fun
import math
from .types import Elem, Array, is_zero
from .precision import is_zero


@dataclass
class Vector:
    v: Array

    def __init__(self, l: Array):
        self.v = l

    @dyn_method
    def __mul__(self, *_) -> Vector:
        ...

    def __len__(self) -> int:
        return len(self.v)

    def __getitem__(self, i: int) -> Elem:
        return self.v[i]

    def __matmul__(self, w: Vector) -> Vector:
        N = len(self.v)
        v: Vector = Vector([])
        for other in range(N):
            for this in range(N):
                v.v.append(self.v[this] * w.v[other])
        return v

    def __rmul__(self, x: Elem) -> Vector:
        return self.__mul__(x)

    def __add__(self, v: Vector) -> Vector:
        return Vector([x + y for (x, y) in zip(self.v, v.v)])

    def __sub__(self, v: Vector) -> Vector:
        return Vector([x - y for (x, y) in zip(self.v, v.v)])

    def abs(self) -> float:
        return math.sqrt(sum([x * x for x in self.v]))


@dyn_dispatch(Vector, "__mul__", Elem)
def vec_scalar_mul(self, x: Elem) -> Vector:
    return Vector([x * e for e in self.v])


def distance(v1: Vector, v2: Vector):
    return (v1 - v2).abs()


def max_distance(v1: Vector, v2: Vector):
    return max([abs(e1 - e2) for (e1, e2) in zip(v1, v2)])


def abs(v: Vector) -> float:
    return v.abs()
