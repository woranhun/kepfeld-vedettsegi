from __future__ import annotations

import math
from dataclasses import dataclass

from common.point import Point


@dataclass
class Vector:
    x: float
    y: float

    @staticmethod
    def dot(v1: Vector, v2: Vector):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def dist(v1: Vector, v2: Vector):
        return math.hypot(v1.x - v2.x, v1.y - v2.y)

    @staticmethod
    def lerp(v1: Vector, v2: Vector, mix: float):
        return v1 * (1 - mix) + v2 * mix

    def __add__(self, other: Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vector):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vector):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vector):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other)

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def __repr__(self):
        return f"Vector({self.x:.2f}, {self.y:.2f})"

    def mag(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        mag = self.mag()
        if mag < 0.001:
            self.x = 0
            self.y = 0
            return self
        self.x /= mag
        self.y /= mag
        return self

    def to_point(self):
        return Point(round(self.x), round(self.y))
