from common.pixel import Pixel
from processing.filters.pixel_filter import PixelFilter
from processing.pixels import Pixels


class DoubleThreshold(PixelFilter):

    def __init__(self, lower: float, upper: float):
        super().__init__()
        self.lower = lower
        self.upper = upper

    def apply_pixel(self, pixels: Pixels, x: int, y: int):
        pixel = pixels[x, y]
        if pixel.r < self.lower:
            return Pixel(0, 0, 0)
        elif pixel.r > self.upper:
            return Pixel(255, 255, 255)
        else:
            return Pixel(128, 128, 128)
