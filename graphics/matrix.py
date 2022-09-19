from math import radians, cos, sin
from typing import List, Literal, Tuple

from PyQt5.QtCore import QPointF


class Matrix:
    N = 3

    def __init__(self, array: List[List[float]] = None):
        """Do not use externally"""

        if array is not None:
            self.__array = array
        else:
            self.__array = [[0 for _ in range(self.N)] for _ in range(self.N)]

    @staticmethod
    def create_transfer(delta_x: float, delta_y: float) -> 'Matrix':
        return Matrix([
            [1, 0, delta_x],
            [0, 1, delta_y],
            [0, 0, 1]
        ])

    @staticmethod
    def create_rotate(angle_in_degrees: float) -> 'Matrix':
        angle_in_radians = radians(angle_in_degrees)
        return Matrix([
            [cos(angle_in_radians), sin(angle_in_radians), 0],
            [sin(angle_in_radians), cos(angle_in_radians), 0],
            [0, 0, 1]
        ])

    @staticmethod
    def create_scaling(kx: float, ky: float) -> 'Matrix':
        return Matrix([
            [kx, 0, 0],
            [0, ky, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def create_reflection(axis: Literal['x', 'y', 'xy']) -> 'Matrix':
        x = y = 1
        if axis == 'xy':
            x = y = -1
        elif axis == 'x':
            x = -1
        elif axis == 'y':
            y = -1

        return Matrix([
            [x, 0, 0],
            [0, y, 0],
            [0, 0, 1]
        ])

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        result = Matrix()

        for i in range(self.N):
            for j in range(self.N):
                for k in range(self.N):
                    result.__array[i][j] += self.__array[i][k] * other.__array[k][j]

        return result

    def mul_on_vector(self, vector: 'Vector') -> 'Vector':
        col = []

        for i in range(self.N):
            s = 0
            for j in range(self.N):
                s += self.__array[i][j] * vector[j]

            col.append(s)

        return Vector(col)


class Vector(Tuple[float, float, float]):

    def __new__(cls, value: Tuple[float, float, float]):
        return tuple.__new__(cls, value)

    @staticmethod
    def create_by_point(point: QPointF) -> 'Vector':
        return Vector((point.x(), point.y(), 1))

    def to_point(self) -> QPointF:
        return QPointF(self[0], self[1])
