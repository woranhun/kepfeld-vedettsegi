from __future__ import annotations
from dataclasses import dataclass

from common.vector import Vector


@dataclass
class Line:
    point: Vector
    direction: Vector

    @staticmethod
    def intersection(line1: Line, line2: Line):
        if Vector.dot(line1.direction, line2.direction) > 0.999:
            # Parallel lines
            return None

        p11 = line1.point
        p12 = line1.point + line1.direction

        p21 = line2.point
        p22 = line2.point + line2.direction

        numerator = (p11.x - p21.x) * (p21.y - p22.y) - (p11.y - p21.y) * (p21.x - p22.x)
        denominator = (p11.x - p12.x) * (p21.y - p22.y) - (p11.y - p12.y) * (p21.x - p22.x)
        return line1.point + line1.direction * (numerator / denominator)

