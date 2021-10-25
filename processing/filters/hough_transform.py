import math

from processing.filters.filter import Filter, Pixels


class HoughTransform(Filter):

    def __init__(self, angle_steps: int = 180):
        self.angle_steps = angle_steps
        angle_step_size = math.pi / self.angle_steps
        self.cos_lookup = [0.0] * angle_steps
        self.sin_lookup = [0.0] * angle_steps
        for i in range(angle_steps):
            self.cos_lookup[i] = math.cos(i * angle_step_size)
            self.sin_lookup[i] = math.sin(i * angle_step_size)

    def apply(self, pixels: Pixels):
        image_width = round(math.hypot(pixels.width, pixels.height))
        result = Pixels((image_width, self.angle_steps), True)

        for x in range(pixels.width):
            for y in range(pixels.height):
                pixel = pixels[x, y]
                if pixel.r < 128:
                    continue

                for angle_index in range(self.angle_steps):
                    # From x * sin(theta) - y * cos(theta) + ro = 0
                    ro = round(-x * self.sin_lookup[angle_index] + y * self.cos_lookup[angle_index] + image_width) // 2
                    result[ro, angle_index].r += 1

        return result
