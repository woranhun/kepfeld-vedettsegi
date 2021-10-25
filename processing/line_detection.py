import math
from typing import Optional

from PIL import Image

from common.line import Line
from common.point import Point
from common.vector import Vector
from processing.filters.double_threshold import DoubleThreshold
from processing.filters.filter import Pixels
from processing.filters.filter_stack import FilterStack
from processing.filters.gaussian import Gaussian
from processing.filters.grayscale import Grayscale
from processing.filters.hough_transform import HoughTransform
from processing.filters.hysteresis import Hysteresis
from processing.filters.maximum_supression import MaximumSuppression
from processing.filters.sobel import Sobel

ANGLE_STEPS = 360
MIN_PARAMETER_DISTANCE = 20

LINE_DETECTION_STACK = FilterStack() \
        .then(Grayscale()) \
        .then(Gaussian(1, 1)) \
        .then(Sobel()) \
        .then(MaximumSuppression()) \
        .then(DoubleThreshold(25, 200)) \
        .then(Hysteresis()) \
        .then(HoughTransform(ANGLE_STEPS))


def hough_transform_distance(p1: Point, p2: Point, width: int, height: int):
    dist_x = abs(p1.x - p2.x)
    dist_y = abs(p1.y - p2.y)
    if p1.y <= height / 2 <= p2.y or p1.y >= height / 2 >= p2.y:
        dist_y -= height
        dist_x = width - p1.x - p2.x
    return math.hypot(dist_x, dist_y)


def draw_line(image: Image, point: tuple[float, float], direction: tuple[float, float], color: tuple[int, int, int]):
    width, height = image.size
    pixels = image.load()
    for i in range(-1000 // 2, 1000 // 2):
        p = (round(point[0] + direction[0] * i), round(point[1] + direction[1] * i))
        if p[0] < 0 or p[0] >= width or p[1] < 0 or p[1] >= height:
            continue
        pixels[p[0], p[1]] = color


def detect_lines(image: Image, max_count: int):
    pixels = LINE_DETECTION_STACK.apply_to_image_pixels(image)

    found_locations = []
    for i in range(max_count):
        max_value = 0
        max_location: Optional[Point] = None

        for x in range(pixels.width):
            for y in range(pixels.height):
                value = pixels[x, y].r
                if max_value < value:
                    if len(found_locations) > 0:
                        closest = min(map(lambda other: hough_transform_distance(Point(x, y), other, pixels.width, pixels.height), found_locations))
                        if closest < MIN_PARAMETER_DISTANCE:
                            continue
                    max_value = value
                    max_location = Point(x, y)
        found_locations.append(max_location)

    print(found_locations)

    lines = []
    for location in found_locations:
        angle = location.y / pixels.height * math.pi
        ro = location.x * 2 - pixels.width
        print(angle / math.pi * ANGLE_STEPS, ro)
        point = Vector(
            -math.sin(angle) * ro,
            math.cos(angle) * ro
        )
        direction = Vector(
            math.cos(angle),
            math.sin(angle)
        )
        lines.append(Line(point, direction))
        draw_line(image, (point.x, point.y), (direction.x, direction.y), (255, 0, 0))
    image.show()

    return lines
