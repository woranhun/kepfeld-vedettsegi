from common.pixel import Pixel
from processing.filters.pixel_filter import PixelFilter
from processing.pixels import Pixels
from processing.utils import luminance


class Grayscale(PixelFilter):

    def apply_pixel(self, pixels: Pixels, x: int, y: int):
        r = pixels[x, y].r
        brightness = luminance(pixels[x, y])
        return Pixel(r, r, r)
