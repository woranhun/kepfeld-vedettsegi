from __future__ import annotations

from abc import ABC, abstractmethod

from processing.pixels import Pixels


class Filter(ABC):

    @abstractmethod
    def apply(self, pixels: Pixels) -> Pixels:
        pass
