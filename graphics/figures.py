from abc import abstractmethod
from math import cos, pi, sin
from typing import List

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter, QBrush, QPen

from graphics.matrix import Matrix
from graphics.modifications import connect_points, rotate_point, affine_to_point


class Drawable:

    @abstractmethod
    def draw(self, painter: QPainter):
        pass

    @abstractmethod
    def rotate(self, angle_in_degrees: float):
        pass

    @abstractmethod
    def draw_with_affine(self, affine_matrix: Matrix, painter: QPainter):
        pass


class Figure(Drawable):
    def __init__(self, center: QPointF = QPointF(0, 0), pen: QPen = QPen(), brush: QBrush = QBrush()):
        self.__center = center
        self.__pen = pen
        self.__brush = brush

    @property
    def center(self) -> QPointF:
        return self.__center

    @center.setter
    def center(self, value: QPointF):
        self.__center = value

    @property
    def pen(self) -> QPen:
        return self.__pen

    @pen.setter
    def pen(self, value: QPen):
        self.__pen = value

    @property
    def brush(self) -> QBrush:
        return self.__brush

    @brush.setter
    def brush(self, value: QBrush):
        self.__brush = value

    def draw(self, painter: QPainter):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

    @abstractmethod
    def rotate(self, angle_in_degrees: float):
        pass

    @abstractmethod
    def draw_with_affine(self, affine_matrix: Matrix, painter: QPainter):
        pass


class Cycle(Figure):
    def __init__(self, radius: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__radius = radius

    @property
    def radius(self) -> float:
        return self.__radius

    @radius.setter
    def radius(self, value: float):
        self.__radius = value

    def draw(self, painter: QPainter):
        super(Cycle, self).draw(painter)
        painter.drawEllipse(self.center, self.radius, self.radius)

    def draw_with_affine(self, affine_matrix: Matrix, painter: QPainter):
        super(Cycle, self).draw(painter)
        painter.drawEllipse(affine_to_point(self.center, affine_matrix), self.radius, self.radius)

    def rotate(self, angle_in_degrees: float):
        pass


class Rectangle(Figure):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._points = self._init_points()

    @abstractmethod
    def _init_points(self) -> List[QPointF]:
        pass

    def get_points(self) -> List[QPointF]:
        return self._points

    @Figure.center.setter
    def center(self, value: QPointF):
        Figure.center.fset(self, value)
        self._points = self._init_points()

    def draw(self, painter: QPainter):
        super().draw(painter)
        connect_points(self._points, painter, self.brush)

    def draw_with_affine(self, affine_matrix: Matrix, painter: QPainter):
        super().draw(painter)
        connect_points(list(
            map(lambda point: affine_to_point(point, affine_matrix), self.get_points())
        ), painter, self.brush)

    def rotate(self, angle_in_degrees: float):
        for point in self._points:
            rotate_point(point, self.center, angle_in_degrees)


class RegularPolygon(Rectangle):
    def __init__(self, sides_count: int, center_distance: float = 0, *args, **kwargs):
        self.__sides_count = sides_count
        self.__center_distance = center_distance
        super().__init__(*args, **kwargs)

    def _init_points(self):
        val = 2 * pi / self.sides_count
        self._points = [
            QPointF(
                self.center.x() + self.center_distance * cos(val * i),
                self.center.y() + self.center_distance * sin(val * i),
            ) for i in range(self.sides_count)
        ]

    @property
    def center_distance(self) -> float:
        return self.__center_distance

    @center_distance.setter
    def center_distance(self, value: float):
        self.__center_distance = value
        self._init_points()

    @property
    def sides_count(self) -> int:
        return self.__sides_count


class Star(Rectangle):

    def __init__(self, inner_radius: float, outer_radius: float,
                 points_count: int, *args, **kwargs):
        self.__inner_radius = inner_radius
        self.__outer_radius = outer_radius
        self.__points_count = points_count
        super().__init__(*args, **kwargs)

    @property
    def outer_radius(self) -> float:
        return self.__outer_radius

    @property
    def inner_radius(self) -> float:
        return self.__inner_radius

    def _init_points(self) -> List[QPointF]:
        points = []

        val = pi / self.__points_count

        for i in range(self.__points_count * 2):
            if i % 2 == 0:
                radius = self.__outer_radius
            else:
                radius = self.__inner_radius

            points.append(QPointF(
                self.center.x() + radius * cos(val * i),
                self.center.y() + radius * sin(val * i)
            ))

        return points
