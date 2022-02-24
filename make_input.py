import sys
import numpy as np


class point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __le__(self, other):
        if self.x == other.x:
            return self.y <= other.y
        return self.x <= other.x

    def __gt__(self, other):
        if self.x == other.x:
            return self.y > other.y
        return self.x > other.x

    def __ge__(self, other):
        if self.x == other.x:
            return self.y >= other.y
        return self.x >= other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


output_file = "input.txt"

f = open(output_file, 'w')
f2 = open("correct.txt", 'w')


size = int(sys.argv[1])
fsize = int(sys.argv[2])
rsize = int(sys.argv[3])
max_value = 1e9
points = []
for i in range(size):
    x = np.random.randint(-max_value, max_value)
    y = np.random.randint(-max_value, max_value)
    points.append(point(x, y))

for p in points:
    f.write("INSERT ({},{})\n".format(p.x, p.y))

for _ in range(fsize):
    x = np.random.randint(-max_value, max_value)
    y = np.random.randint(-max_value, max_value)
    p = point(x, y)
    f.write("FIND {}\n".format(p))
    if (p in points):
        f2.write("YES\n")
    else:
        f2.write("NO\n")


def inside_rect(point, left_bottom, right_top):
    return point.x >= left_bottom.x and point.x <= right_top.x and point.y >= left_bottom.y and point.y <= right_top.y


points = sorted(points)

for _ in range(rsize):
    x = np.random.randint(-max_value, max_value)
    y = np.random.randint(-max_value, max_value)
    p1 = point(x, y)
    x = np.random.randint(-max_value, max_value)
    y = np.random.randint(-max_value, max_value)
    p2 = point(x, y)
    mn = min(p1, p2)
    mx = max(p1, p2)
    f.write("RANGE ({},{},{},{})\n".format(mn.x, mn.y, mx.x, mx.y))
    insiders = []
    for p in points:
        if inside_rect(p, mn, mx):
            insiders.append(p)
    # f2.write(repr(insiders))
    f2.write(str(len(insiders)))
    f2.write("\n")

f.close()
f2.close()
