from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QBrush

from graphics.figures import Drawable, Cycle


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
        self.__draw_petals(painter)
        self.__core.draw(painter)

    def rotate(self, angle_in_degrees: float):
        self.__rotation += angle_in_degrees

        if self.__rotation > 360:
            self.__rotation %= 360
        elif self.__rotation < -360:
            self.__rotation %= -360

    def __draw_petals(self, painter):
        rect = QRect(
            int(self.core.center.x() - self.petal_radius),
            int(self.core.center.y() - self.petal_radius),
            int(self.petal_radius * 2),
            int(self.petal_radius * 2),
        )

        painter.setPen(self.__core.pen)
        painter.setBrush(self.__brush)

        step_angle = int(360 / (self.__petals_count * 2)) * 16
        start = self.__rotation * 16
        for i in range(self.__petals_count):
            painter.drawPie(rect, start, step_angle)
            start += 2 * step_angle
