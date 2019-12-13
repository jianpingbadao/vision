"""
Provide some helper functions
"""
import sys
import math
from typing import List

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_array(self) -> List:
        return [self.x, self.y]

    def as_tuple(self) -> tuple:
        return (self.x, self.y)

    def __str__(self):
        return str(self.as_tuple())


class Line:
    def __init__(self, xy):
        if not xy or len(xy) != 4:
            print("Error: Line.__init__: must have four numbers")
            sys.exit(-1)
        self.point1 = Point(xy[0], xy[1])
        self.point2 = Point(xy[2], xy[3])

    def get_length(self) -> float:
        """
        Get the length of the line

        Returns
        -------
        float
            The length of the line
        """
        return math.sqrt(abs((self.point2.y -  self.point1.y) ** 2
                           + (self.point2.x - self.point1.x) ** 2))

    def as_list_of_points(self):
        return [self.point1.as_array(), self.point2.as_array()]

    def __str__(self):
        return ",".join([str(self.point1), str(self.point2)])

    def intersection(self, target) -> bool:
        # TODO:
        pass


class Triangle:
    def __init__(self, point1: Point, point2: Point, point3: Point):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self._area = None

    def get_area(self) -> float:
        """Get the area of the triangle.

        Returns
        -------
        float
            The area of the triangle.
        """
        if self._area:
            return self._area

        # https://ncalculators.com/geometry/triangle-area-by-3-points.htm
        self._area = abs((self.point1.x * (self.point2.y - self.point3.y)
                    + self.point2.x * (self.point3.y - self.point1.y)
                    + self.point3.x * (self.point1.y - self.point2.y)) / 2)

        return self._area


class Trapezoid:
    def __init__(self, lines: List[List]):
        # TODO: make sure that these two lines (segments) are good, e.g., not cross,
        # not vertical to each other
        # make sure the trapezoid is convex
        self.line_up = Line(lines[0])
        self.line_down = Line(lines[1])
        self._area = None

    def get_area(self) -> float:
        """Get or calculate the area of the Trapezoid

        Returns
        -------
        float
            The area of the Trapezoid
        """
        if self._area:
            return self._area

        top_left_triangle = Triangle(self.line_up.point1, self.line_up.point2, self.line_down.point1)
        bottom_right_triangle = Triangle(self.line_down.point1, self.line_down.point2, self.line_up.point2)
        self._area = top_left_triangle.get_area() + bottom_right_triangle.get_area()
        print(top_left_triangle.get_area())
        print(bottom_right_triangle.get_area())
        return self._area

    def inside(self, target: Point) -> bool:
        """Check if a given point is inside the trapezoid or not

        Parameters
        ----------
        target : Point
            The target point

        Returns
        -------
        bool
            True if the point is inside the Trapezoid; False, otherwise.
        """
        # image that the target is inside the trapezoid
        # the point along with the four edges of the trapezoid will
        # form 4 triangles
        # if the sum of the 4 triangles is the same as that of the trapezoid
        # then the point is inside the trapezoid
        top_area = Triangle(self.line_up.point1, self.line_up.point2, target).get_area()
        right_area = Triangle(self.line_up.point2, self.line_down.point2, target).get_area()
        bottom_area = Triangle(self.line_down.point2, self.line_down.point1, target).get_area()
        left_area = Triangle(self.line_down.point1, self.line_up.point1, target).get_area()
        return sum([top_area, right_area, bottom_area, left_area]) == self.get_area()


class Hexagon:
    def __init__(self, lines: List[List], direction=None):
        self.trapezoid1 = Trapezoid(lines[:2])
        self.trapezoid2 = Trapezoid(lines[1:])
        self.direction = direction
        self.lines = [Line(line) for line in lines]

    def inside(self, target: Point) -> bool:
        """Check if a given point is inside the Hexagon.

        Parameters
        ----------
        target : Point
            The target point

        Returns
        -------
        bool
            True if the target point is inside the Hexagon; False, otherwise.
        """
        return self.trapezoid1.inside(target) or self.trapezoid2.inside(target)

    def __str__(self):
        return "\n".join([str(line) for line in self.lines])
