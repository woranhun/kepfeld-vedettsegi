from processing.filters.filter import Filter
from processing.pixels import Pixels

NEIGHBOR_OFFSETS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


class Hysteresis(Filter):

    def apply(self, pixels: Pixels):
        checked_points = [[False] * pixels.height for _ in range(pixels.width)]

        # Collect strong edges
        unchecked_strong_edges: list[tuple[int, int]] = []
        for x in range(pixels.width):
            for y in range(pixels.height):
                if pixels[x, y].r > 200:
                    # Strong edge
                    unchecked_strong_edges.append((x, y))
                    checked_points[x][y] = True

        while len(unchecked_strong_edges) > 0:
            new_unchecked_edges: list[tuple[int, int]] = []

            for x, y in unchecked_strong_edges:
                for off_x, off_y in NEIGHBOR_OFFSETS:
                    if x + off_x < 0 or x + off_x >= pixels.width or y + off_y < 0 or y + off_y >= pixels.height:
                        continue
                    if not checked_points[x + off_x][y + off_y] and pixels[x + off_x, y + off_y].r > 100:
                        pixels[x + off_x, y + off_y].set(255, 255, 255)
                        new_unchecked_edges.append((x + off_x, y + off_y))
                        checked_points[x + off_x][y + off_y] = True

            unchecked_strong_edges = new_unchecked_edges

        # Set unchecked pixels to black
        for x in range(pixels.width):
            for y in range(pixels.height):
                if not checked_points[x][y]:
                    pixels[x, y].set(0, 0, 0)

        return pixels
