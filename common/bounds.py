from dataclasses import dataclass
from typing import Callable


@dataclass
class Bounds(object):
    x: int
    y: int
    width: int
    height: int

    def for_each(self, func: Callable[[int, int], None]):
        for x in range(self.width):
            for y in range(self.height):
                func(x + self.x, y + self.y)
