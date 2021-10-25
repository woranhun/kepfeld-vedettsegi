from __future__ import annotations


class Pixel(object):

    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b

    def saturate(self):
        self.r = max(min(self.r, 255), 0)
        self.g = max(min(self.g, 255), 0)
        self.b = max(min(self.b, 255), 0)
        return self

    def clone(self):
        return Pixel(
            self.r,
            self.g,
            self.b
        )

    def set(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other: Pixel):
        return Pixel(self.r + other.r, self.g + other.g, self.b + other.b)

    def __iadd__(self, other: Pixel):
        self.r += other.r
        self.g += other.g
        self.b += other.b
        return self

    def __sub__(self, other: Pixel):
        return Pixel(self.r - other.r, self.g - other.g, self.b - other.b)

    def __isub__(self, other: Pixel):
        self.r -= other.r
        self.g -= other.g
        self.b -= other.b
        return self

    def __mul__(self, other: float):
        return Pixel(self.r * other, self.g * other, self.b * other)

    def __imul__(self, other: float):
        self.r *= other
        self.g *= other
        self.b *= other
        return self

    def __div__(self, other: float):
        return Pixel(self.r / other, self.g / other, self.b / other)

    def __idiv__(self, other: float):
        self.r /= other
        self.g /= other
        self.b /= other
        return self

    def __iter__(self):
        return self.r, self.g, self.b
