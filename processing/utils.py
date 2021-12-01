from common.pixel import Pixel


def luminance(color: Pixel):
    return color.r * 0.299 + color.g * 0.587 + color.b * 0.114


def lerp(a: float, b: float, mix: float):
    return a * (1 - mix) + b * mix
