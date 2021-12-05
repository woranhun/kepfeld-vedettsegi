import copy
from typing import Union

from PIL import Image

from common.bounds import Bounds
from common.pixel import Pixel
from common.point import Point
from common.types import Size
from common.vector import Vector


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

    def get_pixel(self, point: Point):
        return self[point.x, point.y]

    def bilinear_sample(self, vec: Vector):
        start = vec.to_point()
        top_left = self.get_pixel(start)
        top_right = self.get_pixel(start + Point(1, 0))
        bottom_left = self.get_pixel(start + Point(0, 1))
        bottom_right = self.get_pixel(start + Point(1, 1))
        x_mix = vec.x % 1
        y_mix = vec.y % 1
        return Pixel.lerp(
            Pixel.lerp(bottom_right, bottom_left, x_mix),
            Pixel.lerp(top_right, top_left, x_mix),
            y_mix
        )

    @property
    def size(self):
        return self.width, self.height

    @property
    def int_data(self):
        return list(map(lambda pixel: (round(pixel.r), round(pixel.g), round(pixel.b)), self.data))

    def sub_region(self, bounds: Bounds):
        result = Pixels((bounds.width, bounds.height), True)
        for x in range(bounds.width):
            for y in range(bounds.height):
                pix = self[bounds.x + x, bounds.y + y]
                result[x, y].set(pix.r, pix.g, pix.b)
        return result

    def to_image(self):
        img = Image.new("RGB", self.size)
        img.putdata(self.int_data)
        return img

    def show(self):
        self.to_image().show()

    def save(self, file: str):
        self.to_image().save(file)
