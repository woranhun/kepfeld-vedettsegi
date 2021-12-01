import math

from common.matrix import Matrix
from common.point import Point
from processing.filters.convolve import convolve_rgb
from processing.filters.filter_stack import FilterStack
from processing.filters.pixel_filter import PixelFilter
from processing.pixels import Pixels


class Gaussian1D(PixelFilter):

    def __init__(self, radius: int, kernel: Matrix):
        super().__init__()
        self.radius = radius
        self.kernel = kernel

    def apply_pixel(self, pixels: Pixels, x: int, y: int):
        return convolve_rgb(pixels, Point(x, y), self.kernel)


class Gaussian(FilterStack):

    @staticmethod
    def __erf(x):
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        t = 1.0 / (1.0 + p * abs(x))
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)

        return (-1 if x < 0 else 1 if x > 0 else 0) * y

    @staticmethod
    def __calculate_kernel_element(x: float, deviation: float = 1):
        return 0.5 * Gaussian.__erf(x / (math.sqrt(2) * deviation))

    def __init__(self, radius: int, deviation: float = 1):
        super().__init__()
        horizontal_kernel = Matrix(radius * 2 + 1, 1)
        vertical_kernel = Matrix(1, radius * 2 + 1)

        radius = radius

        x = -radius - 0.5
        last_value = Gaussian.__calculate_kernel_element(x, deviation)
        kernel_sum = 0.0

        for i in range(radius * 2 + 1):
            x += 1
            new_value = Gaussian.__calculate_kernel_element(x, deviation)
            value = new_value - last_value
            horizontal_kernel[i, 0] = value
            vertical_kernel[0, i] = value
            kernel_sum += value
            last_value = new_value

        horizontal_kernel.normalize()
        vertical_kernel.normalize()
        self.then(Gaussian1D(radius, horizontal_kernel)) \
            .then(Gaussian1D(radius, vertical_kernel.copy().transpose()))
