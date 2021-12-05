from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple

class Point:
    _x: int
    _y: int

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
    
    def __lt__(self, other: Point) -> bool:
        return self.x < other.x or self.x == other.x and self.y < other.y
    
    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __le__(self, other: Point) -> bool:
        return self < other or self == other

    def __gt__(self, other: Point) -> bool:
        return not (self <= other)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __str__(self) -> str:
        return f'Point({self.x}, {self.y})'
    
    def __sub__(self, other: Point) -> Point:
        return Point(self._x - other._x, self._y - other._y)

    @classmethod
    def from_str(self, point: str) -> Point:
        a, b = map(int, point.strip().split(','))
        return Point(a, b)
    
    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

class Line:
    _start: Point
    _stop: Point
    _dx: int
    _dy: int

    def __init__(self, a: Point, b: Point):
        if a <= b:
            self._start = a
            self._stop = b
        else:
            self._start = b
            self._stop = a
        self._dx = self._stop.x - self._start.x
        self._dy = self._stop.y - self._start.y
        # normalize
        if self._dx != 0:
            self._dx //= abs(self._dx)
        if self._dy != 0:
            self._dy //= abs(self._dy)
    
    @classmethod
    def from_str(self, line: str) -> Line:
        a, b = line.strip().split(' -> ')
        return Line(Point.from_str(a), Point.from_str(b))
    
    def __str__(self) -> str:
        return f'Line({self._start}, {self._stop}, dx={self._dx}, dy={self._dy})'
        
    @property
    def start(self) -> Point:
        return self._start

    @property
    def stop(self) -> Point:
        return self._stop
        
    def points(self) -> List[Point]:
        return [
            Point(self._start.x + i * self._dx, self._start.y + i * self._dy)
            for i in range(max(self._stop.x - self._start.x,
                               self._stop.y - self._start.y) + 1)
        ]

def get_data(input_path: Path) -> List[Line]:
    lines = []
    with input_path.open() as f:
        line: str = f.readline()
        while line:
            lines.append(Line.from_str(line))
            line = f.readline()
    return lines

def diagram_intersections(intersections: Dict[Point,int],
                          bounds: Tuple[Point,Point]):
    print(f'start: {bounds[0]}')
    print(f'stop: {bounds[1]}')
    diff: Point = bounds[1] - bounds[0]
    for row in range(diff.y + 1):
        line = ''
        for col in range(diff.x + 1):
            point = Point(bounds[0].x + col, bounds[0].y + row)
            char = hex(intersections.get(point, 0))[2:]
            if char == '0':
                char = '.'
            line += char
        print(line)
    
def count_intersections(lines: List[Line],
                        print_intersections: bool = False) -> int:
    count = 0
    intersections: Dict[Point,int] = {}
    left: int = 0
    right: int = 0
    up: int = 0
    down: int = 0
    for line in lines:
        if line.start.x < left:
            left = line.start.x
        if line.start.y < down:
            down = line.start.y
        if line.stop.x > right:
            right = line.stop.x
        if line.stop.y > up:
            up = line.stop.y
        for point in line.points():
            if point not in intersections:
                intersections[point] = 0
            intersections[point] += 1
            if intersections[point] == 2:
                count += 1
    if print_intersections:
        diagram_intersections(intersections, (Point(left, down),
                                              Point(right, up)))
    return count

if __name__ == '__main__':
    input_path = Path(__file__).resolve().parent / 'input.txt'
    lines = get_data(input_path)
    count = count_intersections(lines, print_intersections=False)
    print(f'line intersections: {count}')
