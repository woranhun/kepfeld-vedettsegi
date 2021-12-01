from PIL import Image

from processing.filters.filter import Filter
from processing.pixels import Pixels


class Show(Filter):
    def apply(self, pixels: Pixels):
        image = Image.new("RGB", pixels.size)
        image.putdata(pixels.int_data)
        image.show()
        return pixels
