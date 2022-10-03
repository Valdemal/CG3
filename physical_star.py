from PyQt5.QtCore import QPointF, QRect, QLine

from graphics.figures import Star, rotate_point
from graphics.matrix import Matrix
from graphics.modifications import increase_angle, affine_to_point, distance_between_points


class PhysicalStar(Star):
    POINTS_COUNT = 4

    def __init__(self, inner_radius: float, outer_radius: float,
                 inner_angle_speed: float, outer_angle_speed: float,
                 distance_speed: float,
                 *args, **kwargs):
        super().__init__(inner_radius, outer_radius, PhysicalStar.POINTS_COUNT,
                         *args, **kwargs)

        self.__inner_angle_speed = inner_angle_speed
        self.__outer_angle_speed = outer_angle_speed

        self.__inner_rotation = self.__outer_rotation = 0
        self.__distance_speed = distance_speed
        self.__distance_coeff = 0.1 * self.__distance_speed
        self.__counter = 1

    def animation(self, center_of_rotation: QPointF, draw_rect: QRect):
        self.__update_color(draw_rect)
        self.__update_characteristics()
        self.__affine_transformations(center_of_rotation)

        self._init_points()
        for point in self.get_points():
            rotate_point(point, self.center, self.__inner_rotation)

    def is_alive(self, draw_rect: QRect) -> bool:
        """Возвращает True, если звезда находится внутри draw_rect"""

        return all(draw_rect.contains(point.toPoint()) for point in self.get_points())

    def __update_characteristics(self):
        self.__inner_rotation = increase_angle(self.__inner_rotation, self.__inner_angle_speed)
        self.__distance_coeff *= 0.9
        self.__distance_speed += self.__distance_coeff
        self.__outer_angle_speed *= 0.99
        # self.__distance_speed *= 0.9999
        # self.__counter -= 0.0001 * self.__outer_angle_speed

    def __affine_transformations(self, center_of_rotation: QPointF):

        distance_vector = \
            (
                    self.center +
                    QPointF(self.__distance_speed, self.__distance_speed) -
                    center_of_rotation
            ) / 30

        outer_rotate_matrix = \
            Matrix.transfer(
                center_of_rotation.x() + distance_vector.x(),
                center_of_rotation.y() + distance_vector.y()
            ) * \
            Matrix.rotate(self.__outer_angle_speed) * \
            Matrix.transfer(-center_of_rotation.x(), -center_of_rotation.y())

        self.center = affine_to_point(self.center, outer_rotate_matrix)

    def __update_color(self, draw_rect: QRect):
        distance = min(
            self.center.x() - draw_rect.x(),
            draw_rect.x() + draw_rect.width() - self.center.x(),
            self.center.y() - draw_rect.y(),
            draw_rect.y() + draw_rect.height() - self.center.y()
        )

        if distance > min(draw_rect.width(), draw_rect.height()) / 3:
            return

        # чем меньше distance тем меньше alpha_value
        alpha_value = int(distance - 15)
        pen_color = self.pen.color()
        pen_color.setAlpha(alpha_value)
        brush_color = self.brush.color()
        brush_color.setAlpha(alpha_value)
        self.pen.setColor(pen_color)
        self.brush.setColor(brush_color)
