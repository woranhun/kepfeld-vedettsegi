from common.pixel import Pixel
from processing.filters.filter import Pixels
from processing.filters.pixel_filter import PixelFilter
from processing.utils import luminance


class Grayscale(PixelFilter):

    def apply_pixel(self, pixels: Pixels, x: int, y: int):
        brightness = luminance(pixels[x, y])
        return Pixel(brightness, brightness, brightness)
