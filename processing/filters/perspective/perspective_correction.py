from common.pixel import Pixel
from common.types import Size
from common.vector import Vector
from processing.filters.pixel_filter import PixelFilter
from processing.pixels import Pixels
from processing.utils import lerp


class PerspectiveCorrection(PixelFilter):

    @staticmethod
    def __get_corner_z_coordinates(quad: list[Vector]) -> tuple[float, float, float, float]:
        # Calculate side lengths
        p1, p2, p3, p4 = quad

        side1 = Vector.dist(p1, p2)
        side2 = Vector.dist(p2, p3)
        side3 = Vector.dist(p3, p4)
        side4 = Vector.dist(p4, p1)

        # We'll assume that the center of the polygon has a z coordinate of 1
        # First we calculate the z coordinates of the centers of the shape
        z_side1_mid = 2 / (1 + side1 / side3)
        z_side3_mid = z_side1_mid * side1 / side3
        z_side2_mid = 2 / (1 + side2 / side4)
        z_side4_mid = z_side2_mid * side2 / side4

        z_p1 = 1 / (z_side1_mid + z_side4_mid - 1)
        z_p2 = 1 / (z_side2_mid + z_side1_mid - 1)
        z_p3 = 1 / (z_side3_mid + z_side2_mid - 1)
        z_p4 = 1 / (z_side4_mid + z_side3_mid - 1)

        return z_p1, z_p2, z_p3, z_p4

    def __init__(self, points: list[Vector], result_size: Size):
        super().__init__(result_size)
        p1, p2, p3, p4 = points

        # Orient points so they are in the correct order
        if abs(Vector.dot(p1 - p4, Vector(1, 0))) > 0.7:
            if p1.y > p2.y:
                p1, p2, p3, p4 = p3, p4, p1, p2
        else:
            if p1.y > p4.y:
                p1, p2, p3, p4 = p4, p1, p2, p3
            else:
                p1, p2, p3, p4 = p2, p3, p4, p1

        self.z1, self.z2, self.z3, self.z4 = PerspectiveCorrection.__get_corner_z_coordinates(points)

        self.p1_unprojected = p1 * self.z1
        self.p2_unprojected = p2 * self.z2
        self.p3_unprojected = p3 * self.z3
        self.p4_unprojected = p4 * self.z4

    def apply_pixel(self, pixels: Pixels, x: int, y: int) -> Pixel:
        x_percentage = x / self.result_size[0]
        y_percentage = y / self.result_size[1]

        p_unprojected = Vector.lerp(
            Vector.lerp(self.p1_unprojected, self.p4_unprojected, x_percentage),
            Vector.lerp(self.p2_unprojected, self.p3_unprojected, x_percentage),
            y_percentage
        )
        z = lerp(
            lerp(self.z1, self.z4, x_percentage),
            lerp(self.z2, self.z3, x_percentage),
            y_percentage
        )

        p = p_unprojected / z
        return pixels.bilinear_sample(p)
