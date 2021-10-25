from PIL import Image

from processing.filters.filter import Filter, Pixels


class Show(Filter):
    def apply(self, pixels: Pixels) -> Pixels:
        image = Image.new("RGB", pixels.size)
        image.putdata(pixels.int_data)
        image.show()
        return pixels