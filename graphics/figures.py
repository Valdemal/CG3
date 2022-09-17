from abc import ABC, abstractmethod
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


class RegularPolygon(Figure):
    def __init__(self, sides_count: int, center_distance: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__sides_count = sides_count
        self.__center_distance = center_distance
        self.__init_points()

    def __init_points(self):
        val = 2 * pi / self.sides_count
        self.__points = [
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
        self.__init_points()

    @property
    def sides_count(self) -> int:
        return self.__sides_count

    def get_points(self) -> List[QPointF]:
        return self.__points

    def draw(self, painter: QPainter):
        super().draw(painter)

        path = QPainterPath()
        path.moveTo(self.__points[0])
        for i in range(1, len(self.__points)):
            path.lineTo(self.__points[i])
            painter.drawLine(self.__points[i - 1], self.__points[i])

        painter.drawLine(self.__points[len(self.__points) - 1], self.__points[0])
        path.lineTo(self.__points[0])
        painter.fillPath(path, self.brush)

    def rotate(self, angle_in_degrees: float):
        for point in self.__points:
            x_diff = point.x() - self.center.x()
            y_diff = point.y() - self.center.y()
            cos_fi = cos(radians(angle_in_degrees))
            sin_fi = sin(radians(angle_in_degrees))

            point.setX(self.center.x() + x_diff * cos_fi - y_diff * sin_fi)

            point.setY(self.center.y() + x_diff * sin_fi + y_diff * cos_fi)

    @Figure.center.setter
    def center(self, value: QPointF):
        Figure.center.fset(self, value)
        self.__init_points()
