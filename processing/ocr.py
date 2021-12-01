import math

from PIL import Image

from common.bounds import Bounds
from processing.pixels import Pixels
from processing.utils import luminance

OCR_LETTER_SIZE = (16, 23)
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class OCR(object):

    def __init__(self):
        self.ocr_image = Image.open("OCR.png").load()

    def check_for_character(self, pixels: Pixels, char_bounds: Bounds, is_letter: bool):
        print(char_bounds)
        step_x = char_bounds.width / OCR_LETTER_SIZE[0]
        step_y = char_bounds.height / OCR_LETTER_SIZE[1]
        max_weight = None
        curr_char = None

        chars = CHARACTERS[0:26] if is_letter else CHARACTERS[26:36]

        new_pixels = Pixels((16, 23), True)

        i = 0 if is_letter else 26
        for character in chars:
            x = char_bounds.x
            y = char_bounds.y
            char_x = (i % 6) * OCR_LETTER_SIZE[0]
            char_y = (i // 6) * OCR_LETTER_SIZE[1]
            weight = 0
            for dx in range(OCR_LETTER_SIZE[0]):
                for dy in range(OCR_LETTER_SIZE[1]):
                    ocr_brightness = self.ocr_image[char_x + dx, char_y + dy][0]
                    pixel_brightness = 255 - pixels[math.floor(x), math.floor(y)].r
                    pixel_weight = ocr_brightness / 255 if ocr_brightness > 0 else -1
                    pixel_value = pixel_brightness / 255 if pixel_brightness > 0 else -1
                    weight += pixel_weight * pixel_value
                    new_pixels[dx, dy].set(pixel_brightness, pixel_brightness, pixel_brightness)
                    y += step_y
                y = char_bounds.y
                x += step_x
            if max_weight is None or weight > max_weight:
                max_weight = weight
                curr_char = character
            i += 1
        new_pixels.show()
        return curr_char

    @staticmethod
    def find_extreme_black_pixels(pixels: Pixels, bounds: Bounds):
        min_x = bounds.x + bounds.width
        max_x = bounds.x
        min_y = bounds.y + bounds.height
        max_y = bounds.y
        for dx in range(bounds.width):
            for dy in range(bounds.height):
                if pixels[bounds.x + dx, bounds.y + dy].r < 128:
                    min_x = min(min_x, bounds.x + dx)
                    max_x = max(max_x, bounds.x + dx)
                    min_y = min(min_y, bounds.y + dy)
                    max_y = max(max_y, bounds.y + dy)
        return Bounds(min_x, min_y, max_x - min_x, max_y - min_y)

    def read_text(self, pixels: Pixels, bounds: Bounds):

        # Get max and min brightness
        min_brightness = float("inf")
        max_brightness = float("-inf")
        for dx in range(bounds.width):
            for dy in range(bounds.height):
                brightness = luminance(pixels[bounds.x + dx, bounds.y + dy])
                min_brightness = min(min_brightness, brightness)
                max_brightness = max(max_brightness, brightness)

        edge = min_brightness + (max_brightness - min_brightness) * 0.5
        for dx in range(bounds.width):
            for dy in range(bounds.height):
                brightness = luminance(pixels[bounds.x + dx, bounds.y + dy])
                if brightness > edge:
                    pixels[bounds.x + dx, bounds.y + dy].set(255, 255, 255)
                else:
                    pixels[bounds.x + dx, bounds.y + dy].set(0, 0, 0)

        text_bounds = OCR.find_extreme_black_pixels(pixels, bounds)

        text_width = text_bounds.width + 1
        character_width = text_width / 8

        result = ""
        for i in range(8):
            start_x = round(text_bounds.x + character_width * i)
            end_x = round(start_x + character_width)
            char_bounds = OCR.find_extreme_black_pixels(pixels,
                                                        Bounds(start_x, text_bounds.y, end_x - start_x,
                                                               text_bounds.height))
            result += self.check_for_character(pixels, Bounds(char_bounds.x, text_bounds.y, char_bounds.width,
                                                              text_bounds.height), i >= 6)

        return result
