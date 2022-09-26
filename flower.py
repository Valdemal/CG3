from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QBrush

from graphics.figures import Drawable, Cycle
from graphics.matrix import Matrix
from graphics.modifications import increase_angle, affine_to_rect


class Flower(Drawable):
    # избежать дублирования

    def __init__(self, petals_count: int, core: Cycle, petal_radius: float = 0, brush: QBrush = QBrush()):
        self.__petal_radius = petal_radius
        self.__petals_count = petals_count
        self.__core = core
        self.__rotation = 0
        self.__brush = brush

    @property
    def core(self) -> Cycle:
        return self.__core

    @property
    def petal_radius(self):
        return self.__petal_radius

    @petal_radius.setter
    def petal_radius(self, value: float):
        self.__petal_radius = value

    def draw(self, painter: QPainter):
        rect = self.__get_petals_rect()
        self.__draw_petals_by_rect(painter, rect)
        self.__core.draw(painter)

    def draw_with_affine(self, affine_matrix: Matrix, painter: QPainter):
        rect = self.__get_petals_rect()
        self.__draw_petals_by_rect(painter, affine_to_rect(rect, affine_matrix))
        self.__core.draw_with_affine(affine_matrix, painter)

    def rotate(self, angle_in_degrees: float):
        self.__rotation = increase_angle(self.__rotation, angle_in_degrees)

    def __get_petals_rect(self) -> QRect:
        return QRect(
            int(self.core.center.x() - self.petal_radius),
            int(self.core.center.y() - self.petal_radius),
            int(self.petal_radius * 2),
            int(self.petal_radius * 2),
        )

    def __draw_petals_by_rect(self, painter, rect):
        painter.setPen(self.__core.pen)
        painter.setBrush(self.__brush)

        step_angle = int(360 / (self.__petals_count * 2)) * 16

        # Лютейшие костыли для работы отражения
        sign = 1 if rect.topRight().x() > rect.topLeft().x() else -1
        start = self.__rotation * 16 + (step_angle if sign == -1 else 0)

        for i in range(self.__petals_count):
            painter.drawPie(rect, sign * start, sign * step_angle)
            start += 2 * step_angle
