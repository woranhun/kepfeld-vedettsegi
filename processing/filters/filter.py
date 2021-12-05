from __future__ import annotations

from abc import ABC, abstractmethod

from PIL import Image

from processing.pixels import Pixels


class Filter(ABC):

    def apply_to_image(self, image: Image):
        pixels = Pixels.from_image(image)
        pixels = self.apply(pixels)
        return pixels

    @abstractmethod
    def apply(self, pixels: Pixels) -> Pixels:
        pass
