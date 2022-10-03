from math import radians, cos, sin, sqrt
from typing import List

from PyQt5.QtCore import QPointF, QRect
from PyQt5.QtGui import QPainterPath, QBrush, QPainter

from graphics.matrix import Matrix, Vector


def connect_points(points: List[QPointF], painter: QPainter, brush: QBrush):
    path = QPainterPath()
    path.moveTo(points[0])
    for i in range(1, len(points)):
        path.lineTo(points[i])
        painter.drawLine(points[i - 1], points[i])

    painter.drawLine(points[len(points) - 1], points[0])
    path.lineTo(points[0])
    painter.fillPath(path, brush)


def rotate_point(pivot: QPointF, center: QPointF, angle_in_degrees: float):
    x_diff = pivot.x() - center.x()
    y_diff = pivot.y() - center.y()
    cos_fi = cos(radians(angle_in_degrees))
    sin_fi = sin(radians(angle_in_degrees))

    pivot.setX(center.x() + x_diff * cos_fi - y_diff * sin_fi)
    pivot.setY(center.y() + x_diff * sin_fi + y_diff * cos_fi)


def increase_angle(angle: float, increase_in_degrees: float) -> float:
    angle += increase_in_degrees

    if angle > 360:
        angle %= 360
    elif angle < -360:
        angle %= -360

    return angle


def affine_to_point(point: QPointF, affine_matrix: Matrix) -> QPointF:
    vector = Vector.create_by_point(point)
    return affine_matrix.mul_on_vector(vector).to_point()


def affine_to_rect(rect: QRect, affine_matrix: Matrix) -> QRect:
    coords = rect.getCoords()

    return QRect(
        affine_to_point(QPointF(coords[0], coords[1]), affine_matrix).toPoint(),
        affine_to_point(QPointF(coords[2], coords[3]), affine_matrix).toPoint()
    )


def distance_between_points(p1: QPointF, p2: QPointF) -> float:
    return sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)
