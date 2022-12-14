from typing import List

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from graphics.figures import Drawable
from graphics.matrix import Matrix


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

    def draw_with_affine(self, affine_matrix: Matrix, painter: QPainter):
        for component in self.components:
            component.draw_with_affine(affine_matrix, painter)


class PictureWidget(QWidget, Picture):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        Picture.__init__(self)
