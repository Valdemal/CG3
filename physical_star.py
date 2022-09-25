from PyQt5.QtCore import QPointF, QRect

from graphics.figures import Star, increase_angle, rotate_point
from graphics.matrix import Matrix, Vector


class PhysicalStar(Star):
    POINTS_COUNT = 4

    def __init__(self, inner_radius: float, outer_radius: float,
                 inner_angle_speed: float, outer_angle_speed: float,
                 distance_from_center_speed: float, *args, **kwargs):
        super().__init__(inner_radius, outer_radius, PhysicalStar.POINTS_COUNT,
                         *args, **kwargs)

        self.__inner_angle_speed = inner_angle_speed
        self.__outer_angle_speed = outer_angle_speed
        self.__distance_speed = distance_from_center_speed

        self.__inner_rotation = self.__outer_rotation = 0

    def animation(self, center_of_rotation: QPointF, draw_rect: QRect):
        self.__update_color(draw_rect)

        self.__update_characteristics()

        self.__affine_transformations(center_of_rotation)

        self._init_points()
        for point in self.get_points():
            rotate_point(point, self.center, self.__inner_rotation)

    def is_alive(self, draw_rect: QRect) -> bool:
        """Возвращает True, если звезда находится внутри draw_rect"""

        def is_in_rect(point: QPointF) -> bool:
            return draw_rect.x() <= point.x() <= (draw_rect.x() + draw_rect.width()) \
                   and draw_rect.y() <= point.y() <= (draw_rect.y() + draw_rect.height())

        return all(is_in_rect(point) for point in self.get_points())

    def __update_characteristics(self):
        self.__inner_rotation = increase_angle(self.__inner_rotation, self.__inner_angle_speed)
        self.__outer_rotation = increase_angle(self.__outer_rotation, self.__outer_angle_speed)
        self.__distance_speed -= self.__distance_speed * 0.005

    def __affine_transformations(self, center_of_rotation):
        distance_matrix = Matrix.transfer(self.__distance_speed, self.__distance_speed)

        outer_rotate_matrix = Matrix.transfer(-center_of_rotation.x(), -center_of_rotation.y()) * \
                              Matrix.rotate(self.__outer_rotation) * \
                              Matrix.transfer(center_of_rotation.x(), center_of_rotation.y())

        affine_matrix = distance_matrix * outer_rotate_matrix
        vector = Vector.create_by_point(self.center)
        self.center = affine_matrix.mul_on_vector(vector).to_point()

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
