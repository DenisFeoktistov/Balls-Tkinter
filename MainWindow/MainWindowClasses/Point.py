from math import sqrt


class Point:
    def __init__(self, x, y):
        # x: real, y: real
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, float):
            return Point(self.x * other, self.y * other)
        elif isinstance(other, Point):
            return self.x * other.x + self.y + other.y

    def __rmul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return f"({self.x}, {self.y})"
