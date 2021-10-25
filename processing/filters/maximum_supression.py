import math

from common.pixel import Pixel
from processing.filters.filter import Pixels
from processing.filters.pixel_filter import PixelFilter

OFFSETS = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1)
)


class MaximumSuppression(PixelFilter):

    def apply_pixel(self, pixels: Pixels, x: int, y: int) -> Pixel:
        pixel = pixels[x, y]
        length = pixel.r
        angle = pixel.g

        # Round angle to 0, 45, 90 or 135 degrees
        angle = round((((angle + math.pi / 8) % math.pi) - math.pi / 8) / (math.pi / 4))
        offset = OFFSETS[round(angle)]

        if length >= pixels[x + offset[0], y + offset[1]].r and length >= pixels[x - offset[0], y - offset[1]].r:
            return Pixel(length, angle, 0)
        else:
            return Pixel(0, 0, 0)
