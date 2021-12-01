import math
from typing import Optional

from PIL import Image

from common.line import Line
from common.point import Point
from common.vector import Vector
from processing.filters.filter_stack import FilterStack
from processing.filters.gaussian import Gaussian
from processing.filters.grayscale import Grayscale
from processing.filters.line_detection.double_threshold import DoubleThreshold
from processing.filters.line_detection.hough_transform import HoughTransform
from processing.filters.line_detection.hysteresis import Hysteresis
from processing.filters.line_detection.maximum_supression import MaximumSuppression
from processing.filters.line_detection.sobel import Sobel

ANGLE_STEPS = 360
MIN_PARAMETER_DISTANCE = 20

LINE_DETECTION_STACK = FilterStack() \
        .then(Grayscale()) \
        .then(Gaussian(2, 1)) \
        .then(Sobel()) \
        .then(MaximumSuppression()) \
        .then(DoubleThreshold(25, 50)) \
        .then(Hysteresis()) \
        .then(HoughTransform(ANGLE_STEPS))


def hough_transform_distance(p1: Point, p2: Point, width: int, height: int):
    dist_x = abs(p1.x - p2.x)
    dist_y = abs(p1.y - p2.y)
    if p1.y <= height / 2 <= p2.y or p1.y >= height / 2 >= p2.y:
        dist_y -= height
        dist_x = width - p1.x - p2.x
    return math.hypot(dist_x, dist_y)


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

    lines = []
    for location in found_locations:
        angle = location.y / pixels.height * math.pi
        ro = location.x * 2 - pixels.width
        point = Vector(
            -math.sin(angle) * ro,
            math.cos(angle) * ro
        )
        direction = Vector(
            math.cos(angle),
            math.sin(angle)
        )

        lines.append(Line.from_point_and_direction(point, direction))

    return lines
