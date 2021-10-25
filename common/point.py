from __future__ import annotations


class Point(object):

    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Point):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Point):
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Point):
        self.x -= other.x
        self.y -= other.y
        return self

    def __iter__(self):
        return self.x, self.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
