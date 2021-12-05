from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from common.pixel import Pixel
from common.types import Size
from processing.filters.filter import Filter
from processing.pixels import Pixels


class PixelFilter(Filter, ABC):

    def __init__(self, result_size: Optional[Size] = None):
        self.result_size = result_size

    def apply(self, pixels: Pixels):
        size = self.result_size or pixels.size
        temp_pixels = Pixels(size)
        for x in range(size[0]):
            for y in range(size[1]):
                temp_pixels[x, y] = self.apply_pixel(pixels, x, y)
        return temp_pixels

    @abstractmethod
    def apply_pixel(self, pixels: Pixels, x: int, y: int) -> Pixel:
        pass
