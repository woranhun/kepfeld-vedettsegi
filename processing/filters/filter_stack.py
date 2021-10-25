from __future__ import annotations

from PIL import Image

from processing.filters.filter import Filter, Pixels


class FilterStack(Filter):

    def __init__(self):
        self.stack: list[Filter] = []

    def then(self, next_filter: Filter):
        self.stack.append(next_filter)
        return self

    def apply_to_image(self, image: Image):
        pixels = self.apply_to_image_pixels(image)
        result = Image.new("RGB", pixels.size)
        result.putdata(pixels.int_data)
        return result

    def apply_to_image_pixels(self, image: Image):
        pixels = Pixels.from_image(image)
        return self.apply(pixels)

    def apply(self, pixels: Pixels) -> Pixels:
        for next_filter in self.stack:
            pixels = next_filter.apply(pixels)

        return pixels
