from PIL import Image

from common.line import Line
from common.vector import Vector
from debug_tools import draw_line_on_image, draw_point_on_image
from processing.filters.filter_stack import FilterStack
from processing.filters.perspective.perspective_correction import PerspectiveCorrection
from processing.line_detection import detect_lines
from utils.convex_hull import find_convex_hull

HEIGHT = 400

CARD_WIDTH = 85.6
CARD_HEIGHT = 53.98
SCALE = 100


def main():
    original = Image.open("test2.png")
    img = original.resize((round(HEIGHT / original.height * original.width), HEIGHT))
    lines = detect_lines(img, 5)

    for line in lines:
        draw_line_on_image(img, line, (0, 255, 0))

    points: list[Vector] = []

    for line1 in lines:
        for line2 in lines:
            if line1 is line2:
                continue

            intersection = Line.intersection(line1, line2)
            if intersection is None or intersection.x < 0 or intersection.x >= img.width or intersection.y < 0 \
                    or intersection.y >= img.height:
                continue

            for other in points:
                if Vector.dist(intersection, other) < 2:
                    break
            else:
                points.append(intersection)

    convex_hull = find_convex_hull(points)

    while len(convex_hull) > 4:
        for i in range(len(convex_hull)):
            line1 = convex_hull[i]
            line2 = convex_hull[(i + 1) % len(convex_hull)]
            if abs(Vector.dot(line1.direction.normalize(), line2.direction.normalize())) > 0.95:
                convex_hull = convex_hull[:i] + [Line(line1.point1, line2.point2)] + convex_hull[i + 2:]
                break

    for line in convex_hull:
        draw_line_on_image(img, line, (255, 0, 255))
    for line in convex_hull:
        draw_point_on_image(img, line.point2, (0, 0, 255))

    img.show()

    points = list(map(lambda l: l.point1, convex_hull))
    points = list(map(lambda p: p * original.height / img.height, points))
    stack = FilterStack().then(PerspectiveCorrection(points, (round(CARD_WIDTH * SCALE), round(CARD_HEIGHT * SCALE))))
    img = stack.apply_to_image(original)

    img.save("lines.png")


if __name__ == '__main__':
    main()
