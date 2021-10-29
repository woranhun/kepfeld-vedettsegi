from PIL import Image

from common.line import Line
from common.vector import Vector


def draw_line_on_image(img: Image, line: Line, color: tuple[int, int, int] = (0, 0, 0)):
    pixels = img.load()
    print(f"point=({line.point.x}, {line.point.y}), dir=({line.direction.x}, {line.direction.y})")

    for x in range(img.width):
        for y in range(img.height):
            dist_to_line = abs(Vector.dot(Vector(-line.direction.y, line.direction.x), Vector(x, y) - line.point))
            if dist_to_line < 0.5:
                pixels[x, y] = color
