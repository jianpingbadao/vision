import sys

sys.path.append('.')

def test_point_tuple():
    from utils import Point
    point = Point(1, 2)
    assert point.as_tuple() == (1, 2)

def test_line_length():
    from utils import Line
    points = [0, 0, 3, 4]
    line = Line(points)
    length = line.get_length()
    assert length == 5.0

def test_triangle_area():
    from utils import Triangle, Point
    p1 = Point(1, 1)
    p2 = Point(2, 1)
    p3 = Point(0, 0)
    tri = Triangle(p1, p2, p3)
    area = tri.get_area()
    assert area == 0.5

def test_trapezoid_area():
    from utils import Trapezoid
    lines = [[1, 1, 2, 1], [0, 0, 2, 0]]
    trapez = Trapezoid(lines)
    area = trapez.get_area()
    assert area == 1.5

def test_trapezoid_inside():
    from utils import Trapezoid, Point
    lines = [[1, 1, 2, 1], [0, 0, 2, 0]]
    trapez = Trapezoid(lines)
    targets = [Point(1, 1), Point(0.5, 0.5)]
    res = []
    for target in targets:
        res.append(trapez.inside(target))
    assert all(res) == True

def test_trapezoid_outside():
    from utils import Trapezoid, Point
    lines = [[1, 1, 2, 1], [0, 0, 2, 0]]
    trapez = Trapezoid(lines)
    targets = [Point(2, 3), Point(-1, 0.5)]
    res = []
    for target in targets:
        res.append(trapez.inside(target))
    assert res == [False] * len(res)
