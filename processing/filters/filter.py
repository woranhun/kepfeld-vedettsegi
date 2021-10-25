from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import Union

from PIL import Image

from common.pixel import Pixel
from common.types import Size


class Pixels(object):

    @staticmethod
    def from_data(size: Size, data: list[Pixel]):
        result = Pixels(size, False)
        result.data = data
        return result

    @staticmethod
    def from_image(image: Image):
        pixels = image.load()
        result = Pixels(image.size, False)
        for y in range(result.height):
            for x in range(result.width):
                pixel = pixels[x, y]
                result.data.append(Pixel(float(pixel[0]), float(pixel[1]), float(pixel[2])))

        return result

    @staticmethod
    def filled(size: Size, color: tuple[float, float, float]):
        result = Pixels(size, False)
        result.data = [color] * (size[0] * size[1])
        return result

    def __init__(self, size: Size, initialize_data: bool = True):
        self.width, self.height = size
        self.data: list[Pixel] = []
        if initialize_data:
            self.data = [Pixel(0.0, 0.0, 0.0) for _ in range(self.width * self.height)]

    def copy(self):
        result = Pixels((self.width, self.height), False)
        result.data = copy.copy(self.data)
        return result

    def __getitem__(self, index: tuple[int, int]):
        x, y = index
        if x < 0:
            x = 0
        if x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        if y >= self.height:
            y = self.height - 1

        return self.data[x + y * self.width]

    def __setitem__(self, index: tuple[int, int], value: Union[Pixel, float]):
        if isinstance(value, float):
            self.data[index[0] + index[1] * self.width].set(value, value, value)
        else:
            self.data[index[0] + index[1] * self.width] = value

    @property
    def size(self):
        return self.width, self.height

    @property
    def int_data(self):
        return list(map(lambda pixel: (round(pixel.r), round(pixel.g), round(pixel.b)), self.data))


class Filter(ABC):

    @abstractmethod
    def apply(self, pixels: Pixels) -> Pixels:
        pass
