from __future__ import annotations

from dataclasses import dataclass

from common.vector import Vector


@dataclass
class Line:
    point1: Vector
    point2: Vector

    @staticmethod
    def from_point_and_direction(point: Vector, direction: Vector):
        return Line(point, point + direction)

    @staticmethod
    def intersection(line1: Line, line2: Line):
        if Vector.dot(line1.direction, line2.direction) > 0.999:
            # Parallel lines
            return None

        p11 = line1.point1
        p12 = line1.point1 + line1.direction

        p21 = line2.point1
        p22 = line2.point1 + line2.direction

        numerator = (p11.x - p21.x) * (p21.y - p22.y) - (p11.y - p21.y) * (p21.x - p22.x)
        denominator = (p11.x - p12.x) * (p21.y - p22.y) - (p11.y - p12.y) * (p21.x - p22.x)
        return line1.point1 + line1.direction * (numerator / denominator)

    def scale(self, factor: float):
        self.point1 *= factor
        self.point2 *= factor

    def distance_to_point(self, point: Vector):
        return abs(Vector.dot(point - self.point1, self.left_normal))

    def closest_point_to_point(self, point: Vector):
        norm = self.left_normal
        return point - norm * Vector.dot(point - self.point1, self.left_normal)

    @property
    def direction(self):
        return (self.point2 - self.point1).normalize()

    @property
    def left_normal(self):
        return Vector(self.direction.y, -self.direction.x).normalize()

    @property
    def right_normal(self):
        return Vector(-self.direction.y, self.direction.x).normalize()
