from typing import Callable

from PyQt5.QtCore import QRect, Qt, QPoint, QPointF, QRectF, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPaintEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

from graphics.figures import Cycle, Drawable
from graphics.pictures import Picture, PictureWidget


class Flower(Drawable):
    # избежать дублирования

    def __init__(self, petals_count: int, core: Cycle, petal_radius: float = 0, ):
        self.__petal_radius = petal_radius
        self.__petals_count = petals_count
        self.__core = core
        self.__rotation = 0

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
        painter.setBrush(QBrush(QColor("purple")))

        step_angle = int(360 / (self.__petals_count * 2)) * 16
        start = self.__rotation * 16
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
        self.__enabled = False

        self.__init_components()

    def set_draw_rect(self, draw_rect: QRect):
        self.__draw_rect = draw_rect

    def change_enable_status(self):
        self.__enabled = not self.__enabled

    def animation(self):
        if self.__enabled:
            self.__flower.rotate(-15)

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

    def __init__(self, radius=0, center=QPointF(0, 0), pen: QPen = QPen(), on_press_event: Callable = None, *args,
                 **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        Cycle.__init__(self, pen=pen)
        self.radius = radius
        self.center = center
        self.brush = self.DISABLE_BRUSH
        self.__enabled = False
        self.__on_press_event = on_press_event

    @Cycle.center.setter
    def center(self, value: QPointF):
        Cycle.center.fset(self, value)
        self.move(int(self.center.x() - self.radius), int(self.center.y() - self.radius))

    @Cycle.radius.setter
    def radius(self, value: float):
        Cycle.radius.fset(self, value)
        self.resize(int(self.radius * 2), int(self.radius * 2))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.__on_press_event is not None:
            self.__on_press_event()

        if self.__enabled:
            self.__disable()
        else:
            self.__enable()

        self.repaint()

    def __disable(self):
        self.__enabled = False
        self.brush = self.DISABLE_BRUSH

    def __enable(self):
        self.__enabled = True
        self.brush = self.ENABLE_BRUSH


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

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.animation)
        self.__timer.start(50)

    def animation(self):
        self.__ventilator.animation()
        self.repaint()

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
        self.__button = CycleButton(
            parent=self,
            pen=self.__main_pen,
            on_press_event=self.__ventilator.change_enable_status
        )

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
    window = MainWidget('Лабораторная работа №3')

    window.show()
    app.exec_()
