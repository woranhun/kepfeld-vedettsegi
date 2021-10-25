from dataclasses import dataclass

from common.vector import Vector


@dataclass
class Line:
    point: Vector
    direction: Vector
