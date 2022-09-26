from PyQt5.QtCore import QRect, Qt, QPointF, QPoint, QRectF
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen

from flower import Flower
from graphics.figures import Cycle
from graphics.matrix import Matrix
from graphics.modifications import affine_to_rect
from graphics.pictures import Picture


class Ventilator(Picture):
    MAIN_PEN_THICKNESS = 3  # Толщина основного пера
    LEG_THICKNESS_IN_PERCENT = 0.025
    PETAL_COUNT = 5

    def __init__(self, draw_rect: QRect):
        super(Ventilator, self).__init__()
        self.__draw_rect = draw_rect
        self.__enabled = False

        self.__init_components()

    def get_flower(self) -> Flower:
        return self.__flower

    def set_draw_rect(self, draw_rect: QRect):
        self.__draw_rect = draw_rect

    def is_enabled(self) -> bool:
        return self.__enabled

    def change_enable_status(self):
        self.__enabled = not self.__enabled

    def animation(self):
        self.__flower.rotate(-15)

    def draw(self, painter: QPainter):
        self.draw_by_rect(self.__draw_rect, painter)

    def draw_with_affine(self, affine_matrix: Matrix, painter: QPainter):
        self.draw_by_rect(affine_to_rect(self.__draw_rect, affine_matrix), painter)

    def draw_by_rect(self, rect: QRect, painter: QPainter):
        start = rect.bottomLeft()
        width = rect.width()
        height = rect.height()
        painter.setPen(QPen(Qt.black))
        self.__update_components_position(start, width, height)
        # Порядок важен
        self.__draw_leg(painter, start, width, height)
        self.__draw_platform(painter, start, width, height)
        super().draw(painter)

    def __init_components(self):
        main_pen = QPen(Qt.black, self.MAIN_PEN_THICKNESS)
        self.__flower = Flower(
            self.PETAL_COUNT,
            Cycle(
                pen=main_pen,
                brush=QBrush(Qt.black)
            ),
            brush=QBrush(QColor("purple"))
        )

        self.components = [self.__flower, ]

    def __update_components_position(self, start: QPointF, width: float, height: float):
        self.__flower.core.center = QPointF(
            start.x() + width * 0.5,
            start.y() - height * 0.65
        )

        radius_coefficient = min(height, width)
        self.__flower.core.radius = radius_coefficient * 0.05
        self.__flower.petal_radius = radius_coefficient * 0.25

    def __draw_leg(self, painter: QPainter, start: QPoint, width: float, height: float):
        painter.setPen(QPen(Qt.black, height * self.LEG_THICKNESS_IN_PERCENT))

        x = start.x() + 0.5 * width
        painter.drawLine(QPointF(x, start.y() - height * 0.1), QPointF(x, start.y() - height * 0.65))

    def __draw_platform(self, painter: QPainter, start: QPointF, width: float, height: float):
        rect = QRectF(
            QPointF(start.x() + 0.3 * width, start.y() - height * 0.1),
            QPointF(start.x() + 0.7 * width, start.y())
        )

        painter.setPen(QPen(Qt.black, self.MAIN_PEN_THICKNESS))
        painter.fillRect(rect, QBrush(Qt.white))
        painter.drawRect(rect)
