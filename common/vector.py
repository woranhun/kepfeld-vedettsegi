from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Vector:
    x: float
    y: float

    @staticmethod
    def dot(v1: Vector, v2: Vector):
        return v1.x * v2.x + v1.y * v2.y

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