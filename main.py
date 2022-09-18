from PyQt5.QtCore import QRect, Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic.properties import QtGui

from graphics.figures import Cycle, Drawable
from graphics.pictures import Picture, PictureWidget


class Flower(Drawable):
    # избежать дублирования

    def __init__(self, petals_count: int, core: Cycle, petal_radius: float = 0, ):
        self.__petal_radius = petal_radius
        self.__petals_count = petals_count
        self.__core = core

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
        pass

    def __draw_petals(self, painter):

        rect = QRect(
            int(self.core.center.x() - self.petal_radius),
            int(self.core.center.y() - self.petal_radius),
            int(self.petal_radius*2),
            int(self.petal_radius*2),
        )

        painter.setPen(self.__core.pen)
        painter.setBrush(QBrush(QColor("purple")))

        step_angle = int(360 / (self.__petals_count * 2)) * 16
        start = 0
        for i in range(self.__petals_count):
            painter.drawPie(rect, start, step_angle)
            start += 2 * step_angle


class Ventilator(Picture):
    MAIN_PEN_THICKNESS = 3  # Толщина основного пера
    LEG_THICKNESS_IN_PERCENT = 0.025
    PETAL_COUNT = 5

    def __init__(self, draw_rect: QRect):
        super(Ventilator, self).__init__()
        self.__draw_rect = draw_rect

        self.__init_components()

    def __init_components(self):
        main_pen = QPen(Qt.black, self.MAIN_PEN_THICKNESS)
        self.__flower = Flower(
            self.PETAL_COUNT,
            Cycle(
                pen=main_pen,
                brush=QBrush(Qt.black)
            )
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

    def set_draw_rect(self, draw_rect: QRect):
        self.__draw_rect = draw_rect

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
        # зарефакторить, чтобы не создавалось дополнительное перо
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


class CycleButton(QWidget, Cycle):
    ENABLE_BRUSH = QBrush(Qt.green)
    DISABLE_BRUSH = QBrush(Qt.red)

    def __init__(self, radius: float = 0, center: QPointF = QPointF(0, 0), pen: QPen = QPen(), *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        Cycle.__init__(self, pen=pen)
        print(self.parent())
        self.radius = radius
        self.center = center
        self.brush = self.DISABLE_BRUSH
        self.__enabled = False

    @Cycle.center.setter
    def center(self, value: QPointF):
        Cycle.center.fset(self, value)
        self.move(int(self.center.x()-self.radius), int(self.center.y()-self.radius))

    @Cycle.radius.setter
    def radius(self, value: float):
        Cycle.radius.fset(self, value)
        self.resize(int(self.radius*2), int(self.radius*2))

    def draw(self, painter: QPainter):
        Cycle.draw(self, painter)

        # painter.drawRect(int(self.center.x()), int(self.center.y()), int(self.radius*2), int(self.radius*2))
        painter.drawRect(self.rect())

    def disable(self):
        self.__enabled = False
        self.brush = self.DISABLE_BRUSH

    def enable(self):
        self.__enabled = True
        self.brush = self.ENABLE_BRUSH

    def is_enabled(self) -> bool:
        return self.__enabled

    # def paintEvent(self, event: QtGui.QPaintEvent) -> None:
    #     self.draw()
    #
    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if self.is_enabled():
    #         print('Выключение')
    #         self.disable()
    #     else:
    #         print('Включение')
    #         self.enable()
    #
    #     self.repaint()


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

        self.__draw_rect: QRect = QRect()
        self.__init_components()

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Включение сглаживания

        self.__update_components(event)

        self.draw(painter)

        painter.end()

    def draw(self, painter):
        painter.setPen(self.__main_pen)
        painter.drawRect(self.__draw_rect)
        PictureWidget.draw(self, painter)

    def show(self) -> None:
        PictureWidget.show(self)
        self.__button.show()

    def __init_components(self):
        self.__main_pen = QPen(Qt.black, self.MAIN_PEN_THICKNESS)

        self.__ventilator = Ventilator(QRect())
        self.__button = CycleButton(parent=self, pen=self.__main_pen)

        self.components = [self.__ventilator, self.__button]

    def __update_components(self, event):
        self.__draw_rect = self.__get_draw_rect(event)
        self.__ventilator.set_draw_rect(self.__draw_rect)

        start = self.__draw_rect.bottomLeft()

        self.__button.center = QPointF(
            start.x() + self.__draw_rect.width() * 0.6,
            start.y() - self.__draw_rect.height() * 0.05
        )

        self.__button.radius = min(self.__draw_rect.width(), self.__draw_rect.height()) * 0.025

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
