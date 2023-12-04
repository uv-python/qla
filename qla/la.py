from __future__ import annotations
from dataclasses import dataclass
from dyn_dispatch import dyn_dispatch, dyn_dispatch_f, dyn_method, dyn_fun
import math

Elem = float  # complex
Array = list[Elem]
Array2D = list[Array]


def is_zero(x: Elem):
    return abs(x) < 1e-9  # works with complex too


# Vector


@dataclass(frozen=True)
class Vector:
    v: Array

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
        return Vector([x + y for x in self.v for y in v.v])

    def __sub__(self, v: Vector) -> Vector:
        return Vector([x - y for x in self.v for y in v.v])

    def abs(self) -> float:
        return math.sqrt(sum([x * x for x in self.v]))


# Vector method implementations


@dyn_dispatch(Vector, "__mul__", Elem)
def vec_scalar_mul(self, x: Elem) -> Vector:
    return Vector([x * e for e in self.v])


@dataclass
class Matrix:
    m: Array2D

    def __getitem__(self, i: tuple[int, int]) -> Elem:
        return self.m[i[0]][i[1]]

    def __setitem__(self, i: tuple[int, int], e: Elem) -> None:
        self.m[i[0]][i[1]] = e

    def num_rows(self) -> int:
        return len(self.m)

    def num_cols(self) -> int:
        return len(self.m[0]) if self.num_rows() else 0

    def place(self, roff: int, coff: int, m: Matrix) -> None:
        for i in range(m.num_rows()):
            for j in range(m.num_cols()):
                self[roff + i, coff + j] = m[i, j]

    @classmethod
    def new(cls, rows: int, cols: int) -> Matrix:
        m: Array2D = []
        for _ in range(rows):
            l: Array = []
            for _ in range(cols):
                l.append(Elem())
            m.append(l)
        return Matrix(m)

    @classmethod
    def identity(cls, rows: int) -> Matrix:
        m = Matrix.new(rows, rows)
        for i in range(rows):
            m[i, i] = Elem(1.0)
        return m

    def __matvec(self: Matrix, v: Vector) -> Vector:
        ret: Array = []
        for r in range(self.num_rows()):
            x = Elem(0.0)
            for c in range(self.num_cols()):
                x += self[r, c] * v[c]
            ret.append(x)
        return Vector(ret)

    def __matmul(self: Matrix, m: Matrix) -> Matrix:
        num_rows = self.num_rows()
        num_cols = self.num_cols()
        mat = Matrix.new(num_rows, num_cols)
        for r in range(num_rows):
            for c in range(num_cols):
                x = 0.0
                for i in range(num_cols):
                    x += self[r, i] * m[i, c]
                mat[r, c] = x
        return mat

    def __matmul__(self, mv: Matrix | Vector) -> Matrix | Vector:
        if isinstance(mv, Matrix):
            return self.__matmul(mv)
        else:
            return self.__matvec(mv)

    def __mul__(self, x: Elem) -> Matrix:
        num_rows = self.num_rows()
        num_cols = self.num_cols()
        m = Matrix.new(num_rows, num_cols)
        for r in range(num_rows):
            for c in range(num_cols):
                m.m[r][c] = self.m[r][c] * x
        return m

    def __sub__(self, m: Matrix) -> Matrix:
        ret: Array2D = []
        for r in range(self.num_rows()):
            row: Array = []
            for c in range(self.num_cols()):
                row.append(self.m[r][c] - m.m[r][c])
            ret.append(row)
        return Matrix(ret)

    def __add__(self, m: Matrix) -> Matrix:
        ret: Array2D = []
        for r in range(self.num_rows()):
            row: Array = []
            for c in range(self.num_cols()):
                row.append(self.m[r][c] + m.m[r][c])
            ret.append(row)
        return Matrix(ret)

    def __rmul__(self: Matrix, x: Elem) -> Matrix:
        return self.__mul__(x)

    def __mod__(self, m: Matrix) -> Matrix:
        num_rows = self.num_rows()
        num_cols = self.num_cols()
        t = Matrix.new(2 * num_rows, 2 * num_cols)
        for i in range(num_rows):
            for j in range(num_cols):
                roff = 2 * i
                coff = 2 * j
                s = m * self.m[i][j]
                t.place(roff, coff, s)
        return t

    def abs(self) -> float:
        return math.sqrt(sum([x * x for r in self.m for x in r]))

    def transpose(self) -> Matrix:
        m = Matrix.new(self.num_rows(), self.num_cols())
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                m.m[j][i] = self.m[i][j]
        return m

    def conj(self) -> Matrix:
        # conjugate, return self for now
        return self

    def dagger(self) -> Matrix:
        return self.transpose().conj()


# Matrix method implementations


@dyn_fun
def max_distance(*_) -> float:
    ...


@dyn_dispatch_f("max_distance", Matrix, Matrix)
def mat_mat_max_dist(m1: Matrix, m2: Matrix):
    e = 0.0
    for r in range(m1.num_rows()):
        for c in range(m1.num_cols()):
            v = abs(m1[r, c] - m2[r, c])
            e = v if v > e else e
    return e


@dyn_dispatch_f("max_distance", Vector, Vector)
def vec_vec_max_dist(v1: Vector, v2: Vector):
    e = 0.0
    for i in range(len(v1)):
        v = abs(v1[i] - v2[i])
        e = v if v > e else e
    return e


@dyn_fun
def distance(*_):
    ...


@dyn_dispatch_f("distance", Matrix, Matrix)
def mat_mat_distance(m1: Matrix, m2: Matrix) -> float:
    return (m1 - m2).abs()


@dyn_dispatch_f("distance", Vector, Vector)
def vec_vec_distance(v1: Vector, v2: Vector) -> float:
    return (v1 - v2).abs()


@dataclass
class UnitaryMatrix(Matrix):
    def __post_init__(self):
        if not is_zero(
            max_distance(self.dagger() @ self, Matrix.identity(self.num_rows()))
        ):
            raise Exception("Non unitary matrix")
