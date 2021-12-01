from typing import Optional

from common.line import Line
from common.vector import Vector


def get_points_on_right(line: Line, points: list[Vector]):
    normal = line.right_normal

    return list(filter(lambda point: Vector.dot(point - line.point1, normal) > 0, points))


def quickhull_step(points: list[Vector], curr_edge: Line):
    normal = curr_edge.right_normal

    max_dist = float("-inf")
    farthest_point: Optional[Vector] = None
    for point in points:
        dist_to_line = Vector.dot(point - curr_edge.point1, normal)
        if dist_to_line > max_dist:
            max_dist = dist_to_line
            farthest_point = point

    if max_dist < 0:
        return [curr_edge]

    new_line1 = Line(curr_edge.point1, farthest_point)
    new_line2 = Line(farthest_point, curr_edge.point2)
    new_line1_right_points = get_points_on_right(new_line1, points)
    new_line2_right_points = get_points_on_right(new_line2, points)

    lines: list[Line] = []

    if len(new_line1_right_points) == 0:
        lines.append(new_line1)
    else:
        lines += quickhull_step(new_line1_right_points, new_line1)

    if len(new_line2_right_points) == 0:
        lines.append(new_line2)
    else:
        lines += quickhull_step(new_line1_right_points, new_line2)

    return lines


def find_convex_hull(points: list[Vector]):
    # Find extreme points
    min_x_point = points[0]
    max_x_point = points[0]

    for point in points:
        if point.x < min_x_point.x:
            min_x_point = point

        if point.x > max_x_point.x:
            max_x_point = point

    initial_edge_1 = Line(max_x_point, min_x_point)
    initial_edge_2 = Line(min_x_point, max_x_point)
    # Above the initial line
    lines = quickhull_step(get_points_on_right(initial_edge_1, points), initial_edge_1)
    # Below the initial line
    lines += quickhull_step(get_points_on_right(initial_edge_2, points), initial_edge_2)

    return lines
