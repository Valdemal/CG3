from abc import abstractmethod
from math import cos, pi, sin, radians
from typing import List

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath


class Drawable:

    @abstractmethod
    def draw(self, painter: QPainter):
        pass

    @abstractmethod
    def rotate(self, angle_in_degrees: float):
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

    def rotate(self, angle_in_degrees: float):
        pass


def connect_points(points: List[QPointF], painter: QPainter, brush: QBrush):
    path = QPainterPath()
    path.moveTo(points[0])
    for i in range(1, len(points)):
        path.lineTo(points[i])
        painter.drawLine(points[i - 1], points[i])

    painter.drawLine(points[len(points) - 1], points[0])
    path.lineTo(points[0])
    painter.fillPath(path, brush)


def rotate_point(pivot: QPointF, center: QPointF, angle_in_degrees: float):
    x_diff = pivot.x() - center.x()
    y_diff = pivot.y() - center.y()
    cos_fi = cos(radians(angle_in_degrees))
    sin_fi = sin(radians(angle_in_degrees))

    pivot.setX(center.x() + x_diff * cos_fi - y_diff * sin_fi)
    pivot.setY(center.y() + x_diff * sin_fi + y_diff * cos_fi)


def increase_angle(angle: float, increace_in_degrees: float) -> float:
    angle += increace_in_degrees

    if angle > 360:
        angle %= 360
    elif angle < -360:
        angle %= -360

    return angle


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
