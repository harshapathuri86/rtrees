import numpy as np
np.random.seed(0)
output_file = "input.txt"
f = open(output_file, 'w')
f2 = open("correct.txt", 'w')
sz = 100
X = 100
Y = 100
x = np.random.randint(-X, X, size=50)
y = np.random.randint(-Y, Y, size=50)
points = np.array([x, y]).T
for point in points:
    f.write("INSERT ({},{})\n".format(point[0], point[1]))


def inside_points(x, y):
    for point in points:
        if point[0] == x and point[1] == y:
            return True
    return False


# find
for point in points:
    f.write("FIND ({},{})\n".format(point[0], point[1]))
    f2.write("True\n")


for _ in range(sz):
    x, y = np.random.randint(-X, X), np.random.randint(-Y, Y)
    f.write("FIND ({},{})\n".format(x, y))
    f2.write(str(inside_points(x, y)) + "\n")


def inside_rect(point, left_bottom, right_top):
    return point[0] >= left_bottom[0] and point[0] <= right_top[0] and point[1] >= left_bottom[1] and point[1] <= right_top[1]


# range

points = sorted(points, key=lambda x: (x[0], x[1]))

for i in range(len(points)):
    for j in range(i+1, len(points)):
        f.write("RANGE ({},{},{},{})\n".format(
            points[i][0], points[i][1], points[j][0], points[j][1]))
        insiders = []
        for point in points:
            if inside_rect(point, points[i], points[j]) or inside_rect(point, points[j], points[i]):
                insiders.append(point)
        # insiders = sorted(insiders, key=lambda x: (x[0], x[1]))
        f2.write("[ ")
        for insider in insiders:
            f2.write("({},{}),".format(insider[0], insider[1]))
        f2.write("]\n")


f.close()
f2.close()
