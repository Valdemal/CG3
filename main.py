from PyQt5.QtCore import QRect, Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication

from graphics.figures import Figure, Cycle
from graphics.pictures import Picture, PictureWidget


class Flower(Figure):
    # избежать дублирования

    def __init__(self, petal_count: int, core_radius: float = 0, petal_radius: float = 0, *args, **kwargs):
        Figure.__init__(self, *args, **kwargs)
        self.__petal_radius = petal_radius
        self.__petal_count = petal_count

        self.__core = Cycle(core_radius, *args, **kwargs)

    @property
    def petal_radius(self):
        return self.__petal_radius

    @petal_radius.setter
    def petal_radius(self, value: float):
        self.__petal_radius = value

    @property
    def core_radius(self) -> float:
        return self.__core.radius

    @core_radius.setter
    def core_radius(self, value: float):
        self.__core.radius = value

    @Figure.center.setter
    def center(self, value: QPointF):
        Figure.center.fset(self, value)
        self.__core.center = value

    def draw(self, painter: QPainter):
        super(Flower, self).draw(painter)

        self.__core.draw(painter)

    def rotate(self, angle_in_degrees: float):
        pass


class Ventilator(Picture):
    MAIN_PEN_THICKNESS = 3  # Толщина основного пера
    LEG_THICKNESS_IN_PERCENT = 0.025
    PETAL_COUNT = 5

    def __init__(self, draw_rect: QRect):
        super(Ventilator, self).__init__()
        self.__draw_rect = draw_rect

        self.__init_components()

    def __init_components(self):
        self.__flower = Flower(self.PETAL_COUNT,
                               pen=QPen(Qt.black, self.MAIN_PEN_THICKNESS), brush=QBrush(Qt.black))

        self.components = [self.__flower, ]

    def __update_components_position(self, start: QPointF, width: float, height: float):
        self.__flower.center = QPointF(
            start.x() + width * 0.5,
            start.y() - height * 0.65
        )

    def set_draw_rect(self, draw_rect: QRect):
        self.__draw_rect = draw_rect

        radius_coefficient = min(self.__draw_rect.height(), self.__draw_rect.width())
        self.__flower.core_radius = radius_coefficient * 0.05

    def draw(self, painter: QPainter):
        start = self.__draw_rect.bottomLeft()
        width = self.__draw_rect.width()
        height = self.__draw_rect.height()

        painter.setPen(QPen(Qt.black))

        self.__update_components_position(start, width, height)

        # Порядок важен
        self.__draw_leg(painter, start, width, height)
        self.__draw_platform(painter, start, width, height)

        super().draw(painter)

    def __draw_leg(self, painter: QPainter, start: QPoint, width: float, height: float):
        x = start.x() + 0.5 * width
        p1 = QPointF(x, start.y() - height * 0.1)
        p2 = QPointF(x, start.y() - height * 0.65)

        # зарефакторить, чтобы не создавалось дополнительное перо
        painter.setPen(QPen(Qt.black, height * self.LEG_THICKNESS_IN_PERCENT))
        painter.drawLine(p1, p2)

    def __draw_platform(self, painter: QPainter, start: QPointF, width: float, height: float):
        p1 = QPointF(start.x() + 0.3 * width, start.y() - height * 0.1)
        p2 = QPointF(start.x() + 0.7 * width, start.y())

        rect = QRectF(p1, p2)

        painter.setPen(QPen(Qt.black, self.MAIN_PEN_THICKNESS))
        painter.fillRect(rect, QBrush(Qt.white))
        painter.drawRect(rect)


class MainWidget(PictureWidget):
    MIN_HEIGHT = 400
    MIN_WIDTH = 400
    MARGIN = 10  # размер отступа внутри окна в пикселях
    MAIN_PEN_THICKNESS = 3  # Толщина основного пера

    def __init__(self, title: str):
        PictureWidget.__init__(self)

        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.resize(self.MIN_WIDTH, self.MIN_HEIGHT)

        self.setWindowTitle(title)
        self.__init_components()

    def __init_components(self):
        self.__ventilator = Ventilator(QRect())
        self.components = [self.__ventilator]

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Включение сглаживания

        draw_rect = self.__get_draw_rect(event)
        painter.setPen(QPen(Qt.black, self.MAIN_PEN_THICKNESS))
        painter.drawRect(draw_rect)
        self.__ventilator.set_draw_rect(draw_rect)

        self.draw(painter)

        painter.end()

    def __get_draw_rect(self, event) -> QRect:
        center = QPoint(int(self.width() / 2), int(self.height() / 2))
        half_of_square_hypotenuse = int(min(self.width(), self.height()) / 2)
        offset_coefficient = self.MARGIN - half_of_square_hypotenuse

        draw_rect: QRect = event.rect()
        draw_rect.setCoords(
            center.x() + offset_coefficient, center.y() + offset_coefficient,
            center.x() - offset_coefficient, center.y() - offset_coefficient
        )

        return draw_rect


if __name__ == '__main__':
    app = QApplication([])

    pw = PictureWidget()
    widget = MainWidget('Лабораторная работа №3')

    widget.show()
    app.exec_()
