from common.pixel import Pixel


def luminance(color: Pixel):
    return color.r * 0.2125 + color.g * 0.7154 + color.b * 0.0721
