import random

from PyQt5.QtCore import QRect, Qt, QPoint, QPointF, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication

from cycle_button import CycleButton
from graphics.figures import Star
from graphics.pictures import Picture, PictureWidget
from ventilator import Ventilator


class PhysicalStar(Star):
    POINTS_COUNT = 4

    def __init__(self, inner_radius: float, outer_radius: float,
                 degree_in_frame_speed: float, *args, **kwargs):
        super().__init__(inner_radius, outer_radius, PhysicalStar.POINTS_COUNT,
                         *args, **kwargs)

        self.__angle_speed = degree_in_frame_speed

    def animation(self):
        self.rotate(self.__angle_speed)

    def is_alive(self) -> bool:
        return True


class MainWidget(PictureWidget):
    MIN_HEIGHT = 400
    MIN_WIDTH = 400
    MARGIN = 10  # размер отступа внутри окна в пикселях
    MAIN_PEN_THICKNESS = 3  # Толщина основного пера
    CHANCE_OF_STAR_CREATING_IN_FRAME = 0.1

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

        if self.__ventilator.is_enabled():
            self.__ventilator.animation()
            if self.CHANCE_OF_STAR_CREATING_IN_FRAME >= random.random():
                self.__create_random_star()

        stars = self.__stars_composite.components

        # анимация звезд
        for star in stars:
            if isinstance(star, PhysicalStar):
                star.animation()

        # удаление потухших звезд
        self.__stars_composite.components = [
            star for star in stars if isinstance(star, PhysicalStar) and star.is_alive()
        ]

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

    def __create_random_star(self):
        star_radius = self.__ventilator.get_flower().core.radius

        # star_center = self.__ventilator.get_flower().core.center
        star_center = QPointF(
            random.random() * self.width(),
            random.random() * self.height()
        )

        star_brush = QBrush(QColor('yellow'))

        self.__stars_composite.components.append(
            PhysicalStar(
                inner_radius=star_radius * 0.25, outer_radius=star_radius,
                degree_in_frame_speed=random.randint(1, 360), center=star_center,
                pen=self.__main_pen, brush=star_brush
            )
        )

    def __init_components(self):
        self.__main_pen = QPen(Qt.black, self.MAIN_PEN_THICKNESS)

        self.__ventilator = Ventilator(QRect())
        self.__button = CycleButton(
            parent=self,
            pen=self.__main_pen,
            on_press_event=self.__ventilator.change_enable_status
        )

        self.__stars_composite = Picture()

        self.components = [self.__ventilator, self.__button, self.__stars_composite]

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
