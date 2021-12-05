from common.matrix import Matrix
from common.pixel import Pixel
from common.point import Point
from processing.pixels import Pixels


def convolve_grayscale(pixels: Pixels, point: Point, matrix: Matrix):
    """Convolve a matrix with a grayscale image at the specified position
    Returns the result of the convolution and the total weight"""
    width, height = matrix.size

    result = 0.0
    for dx in range(width):
        x = point.x + dx - (width // 2)
        for dy in range(height):
            y = point.y + dy - (height // 2)
            result += pixels[x, y].r * matrix[dx, dy]

    return result


def convolve_rgb(pixels: Pixels, point: Point, matrix: Matrix):
    """Convolve a matrix with an image at the specified position
    Returns the result and the total weight of the convolution"""
    width, height = matrix.size

    result = Pixel(0, 0, 0)
    for dx in range(width):
        x = point.x + dx - (width // 2)
        for dy in range(height):
            y = point.y + dy - (height // 2)
            weight = matrix[dx, dy]
            result += pixels[x, y] * weight

    return result
