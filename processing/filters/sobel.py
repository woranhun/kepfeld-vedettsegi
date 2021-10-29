import math

from common.matrix import Matrix
from common.pixel import Pixel
from common.point import Point
from processing.filters.convolve import convolve_grayscale
from processing.filters.filter import Filter, Pixels
from processing.filters.pixel_filter import PixelFilter


class Sobel(PixelFilter):

    def __init__(self):
        self.matrix_horizontal = Matrix.from_data([
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ])

        self.matrix_vertical = Matrix.from_data([
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ])

    def apply_pixel(self, pixels: Pixels, x: int, y: int):
        horizontal = convolve_grayscale(pixels, Point(x, y), self.matrix_horizontal)
        vertical = convolve_grayscale(pixels, Point(x, y), self.matrix_vertical)
        length = math.hypot(horizontal, vertical)
        angle = math.atan2(vertical, horizontal)
        if length < 0.001:
            angle = 0
        return Pixel(length, angle, 0)
