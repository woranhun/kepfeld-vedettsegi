from PIL import Image

from processing.filters.filter import Filter
from processing.pixels import Pixels


class Save(Filter):

    def __init__(self, file: str):
        self.file = file

    def apply(self, pixels: Pixels):
        img = Image.new("RGB", pixels.size)
        img.putdata(pixels.int_data)
        img.save(self.file)

        return pixels
