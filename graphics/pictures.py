import abc
from typing import List

from PyQt5 import sip
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from graphics.figures import Drawable


class Picture(Drawable):
    def __init__(self, components: List[Drawable] = []):
        self.__components = components

    @property
    def components(self) -> List[Drawable]:
        return self.__components

    @components.setter
    def components(self, value: List[Drawable]):
        self.__components = value

    def draw(self, painter: QPainter):
        for component in self.components:
            component.draw(painter)

    def rotate(self, angle_in_degrees: float):
        for component in self.components:
            component.rotate(angle_in_degrees)


# Picture.register(QWidget)
# def metaclass_resolver(*classes):
#     metaclass = tuple(set(type(cls) for cls in classes))
#     metaclass = metaclass[0] if len(metaclass) == 1 \
#         else type("_".join(mcls.__name__ for mcls in metaclass), metaclass, {})  # class M_C
#     return metaclass("_".join(cls.__name__ for cls in classes), classes, {})  # class C

#
class PictureWidget(QWidget, Picture):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        Picture.__init__(self)
