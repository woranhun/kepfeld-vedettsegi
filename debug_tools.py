import math

from PIL import Image

from common.line import Line
from common.point import Point
from common.vector import Vector


def draw_line_on_image(img: Image, line: Line, color: tuple[int, int, int] = (0, 0, 0)):
    pixels = img.load()

    normal = line.right_normal
    for x in range(img.width):
        for y in range(img.height):
            dist_to_line = abs(Vector.dot(normal, Vector(x, y) - line.point1))
            if dist_to_line < 0.5:
                pixels[x, y] = color


def draw_point_on_image(img: Image, point: Point, color: tuple[int, int, int] = (0, 0, 0), radius: int = 3):
    pixels = img.load()

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if math.hypot(x, y) <= radius and 0 <= point.x + x < img.width and 0 <= point.y + y < img.height:
                pixels[point.x + x, point.y + y] = color
