from typing import Callable

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QMouseEvent, QPen, QBrush
from PyQt5.QtWidgets import QWidget

from graphics.figures import Cycle


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