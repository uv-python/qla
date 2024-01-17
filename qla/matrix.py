from __future__ import annotations
from dataclasses import dataclass

# from dyn_dispatch import dyn_dispatch, dyn_dispatch_f, dyn_method, dyn_fun
import math
from .vector import Vector
from .types import Elem, Array, Array2D, default, identity, neutral_element_sum
from .precision import is_zero


@dataclass
class Matrix:
    m: Array2D
    type: type

    def __init__(self, a: Array2D, t: type = None):
        if len(a) == 0:
            raise ValueError("Empty array")
        if t == None:
            self.type = type(a[0][0])
        else:
            self.type = t
        self.m = a

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
    def new(cls, rows: int, cols: int, t: type = float) -> Matrix:
        m: Array2D[t] = []
        for _ in range(rows):
            l: Array[t] = []
            for _ in range(cols):
                l.append(default(t))
            m.append(l)
        return Matrix(m, t)

    @classmethod
    def identity(cls, rows: int, t: type = float) -> Matrix:
        m = Matrix.new(rows, rows, t)
        for i in range(rows):
            m[i, i] = identity(t)
        return m

    def __matvec(self: Matrix, v: Vector) -> Vector:
        """Left matrix vector multiply"""
        ret: Array[self.type] = []
        for r in range(self.num_rows()):
            x = neutral_element_sum(self.type)
            for c in range(self.num_cols()):
                x += self[r, c] * v[c]
            ret.append(x)
        return Vector(ret)

    def __matmul(self: Matrix, m: Matrix) -> Matrix:
        num_rows = self.num_rows()
        num_cols = self.num_cols()
        mat = Matrix.new(num_rows, num_cols, self.type)
        for r in range(num_rows):
            for c in range(num_cols):
                x = neutral_element_sum(self.type)
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
        m = Matrix.new(num_rows, num_cols, self.type)
        for r in range(num_rows):
            for c in range(num_cols):
                m.m[r][c] = self.m[r][c] * x
        return m

    def __sub__(self, m: Matrix) -> Matrix:
        ret: Array2D[self.type] = []
        for r in range(self.num_rows()):
            row: Array = []
            for c in range(self.num_cols()):
                row.append(self.m[r][c] - m.m[r][c])
            ret.append(row)
        return Matrix(ret, self.type)

    def __add__(self, m: Matrix) -> Matrix:
        ret: Array2D[self.type] = []
        for r in range(self.num_rows()):
            row: Array = []
            for c in range(self.num_cols()):
                row.append(self.m[r][c] + m.m[r][c])
            ret.append(row)
        return Matrix(ret, self.type)

    def __rmul__(self: Matrix, x: Elem) -> Matrix:
        return self.__mul__(x)

    def __mod__(self, m: Matrix) -> Matrix:
        num_rows = self.num_rows()
        num_cols = self.num_cols()
        t = Matrix.new(2 * num_rows, 2 * num_cols, self.type)
        for i in range(num_rows):
            for j in range(num_cols):
                roff = 2 * i
                coff = 2 * j
                s = m * self.m[i][j]
                t.place(roff, coff, s)
        return t

    def __len__(self):
        return self.num_rows() * self.num_cols()

    def abs(self) -> float:
        return math.sqrt(sum([x * x for r in self.m for x in r]))

    def transpose(self) -> Matrix:
        m = Matrix.new(self.num_rows(), self.num_cols(), self.type)
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                m.m[j][i] = self.m[i][j]
        return m

    def conj(self) -> Matrix:
        m = Matrix.new(self.num_rows(), self.num_cols(), self.type)
        for r in range(self.num_rows()):
            for c in range(self.num_cols()):
                m = self.m[r][c].conjugate()
        return m

    def dagger(self) -> Matrix:
        return self.transpose().conj()

    def shape(self) -> tuple[int, int]:
        return (self.num_rows(), self.num_cols())


def max_distance(m1: Matrix, m2: Matrix):
    e = 0.0
    for r in range(m1.num_rows()):
        for c in range(m1.num_cols()):
            v = abs(m1[r, c] - m2[r, c])
            e = v if v > e else e
    return e


def distance(m1: Matrix, m2: Matrix) -> float:
    return (m1 - m2).abs()


@dataclass
class UnitaryMatrix(Matrix):
    def __post_init__(self):
        if not is_zero(
            max_distance(self.dagger() @ self, Matrix.identity(self.num_rows()))
        ):
            raise Exception("Non unitary matrix")
