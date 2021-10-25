from __future__ import annotations

from abc import ABC, abstractmethod

from common.pixel import Pixel
from processing.filters.filter import Filter, Pixels


class PixelFilter(Filter, ABC):

    def apply(self, pixels: Pixels):
        temp_pixels = Pixels(pixels.size)
        for x in range(pixels.width):
            for y in range(pixels.height):
                temp_pixels[x, y] = self.apply_pixel(pixels, x, y)
        return temp_pixels

    @abstractmethod
    def apply_pixel(self, pixels: Pixels, x: int, y: int) -> Pixel:
        pass
