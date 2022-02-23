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


class Rectangle:
    def __init__(self, p1, p2):
        self.ll = min(p1, p2)
        self.ru = max(p1, p2)

    def contains_point(self, p):
        return (self.ll.x <= p.x <= self.ru.x) and (self.ll.y <= p.y <= self.ru.y)

    def contains_Rectangle(self, rect):
        return self.ll.x <= rect.ll.x and self.ll.y <= rect.ll.y and self.ru.x >= rect.ru.x and self.ru.y >= rect.ru.y

    def updated_Rectangle(self, p):
        return Rectangle(point(min(self.ll.x, p.x), min(self.ll.y, p.y)), point(max(self.ru.x, p.x), max(self.ru.y, p.y)))

    def area(self):
        return (self.ru.x - self.ll.x) * (self.ru.y - self.ll.y)

    def distance(self, p):
        return abs(self.area() - self.updated_Rectangle(p).area())

    def overlap(self, other):
        return not (self.ll.x > other.ru.x or self.ru.x < other.ll.x or self.ru.y < other.ll.y or self.ll.y > other.ru.y)

    def __repr__(self):
        return "[{}, {}]".format(repr(self.ll), repr(self.ru))


class Node:

    max_children = 2
    max_points = 12
    maximum = 1e9+1
    minimum = -1e9-1

    def __init__(self, is_leaf=False, children=[],) -> None:
        self.is_leaf = is_leaf
        self.children = children
        self.rectangle = Rectangle(
            point(Node.maximum, Node.maximum), point(Node.minimum, Node.minimum))
        self.update_rectangle()

    def update_rectangle(self):
        self.rectangle.ll = point(Node.maximum, Node.maximum)
        self.rectangle.ru = point(Node.minimum, Node.minimum)
        if self.is_leaf:
            for child in self.children:
                self.rectangle.ll.x = min(
                    self.rectangle.ll.x, child.x)
                self.rectangle.ll.y = min(
                    self.rectangle.ll.y, child.y)
                self.rectangle.ru.x = max(
                    self.rectangle.ru.x, child.x)
                self.rectangle.ru.y = max(
                    self.rectangle.ru.y, child.y)
        else:
            for child in self.children:
                self.rectangle.ll.x = min(
                    self.rectangle.ll.x, child.rectangle.ll.x)
                self.rectangle.ll.y = min(
                    self.rectangle.ll.y, child.rectangle.ll.y)
                self.rectangle.ru.x = max(
                    self.rectangle.ru.x, child.rectangle.ru.x)
                self.rectangle.ru.y = max(
                    self.rectangle.ru.y, child.rectangle.ru.y)

    def leaf_insert(self, point):
        assert self.is_leaf, "Cannot insert into non-leaf node"
        # return is_split, new_node
        if len(self.children) < self.max_points:
            self.children.append(point)
            self.children = sorted(self.children)
            self.update_rectangle()
            return False, None
        else:
            self.children.append(point)
            import math
            split_pos = math.ceil(len(self.children)/2)
            new_node_children = self.children[split_pos:]
            self.children = self.children[:split_pos]
            self.update_rectangle()
            new_node = Node(is_leaf=True, children=new_node_children)

            return True, new_node

    def inter_insert(self, node):
        assert not self.is_leaf, "Cannot insert into leaf node"
        if len(self.children) < self.max_children:
            self.children.append(node)
            self.update_rectangle()
            return False, None
        self.children.append(node)
        import math
        split_pos = math.ceil(len(self.children)/2)
        new_node_children = self.children[split_pos:]
        self.children = self.children[:split_pos]
        self.update_rectangle()
        new_node = Node(is_leaf=False, children=new_node_children)
        return True, new_node

    def find(self, p):
        if self.is_leaf:
            return (p in self.children)
        is_found = False
        for child in self.children:
            is_found = is_found or child.find(p)
        return is_found

    def range(self, rect):
        if self.is_leaf:
            # print("reached leaf", rect, "children: ", self.children)
            return [p for p in self.children if rect.contains_point(p)]
        arr = []
        for child in self.children:
            if child.rectangle.overlap(rect):
                arr.extend(child.range(rect))
        return arr

    def contains_point(self, p):
        return self.rectangle.contains_point(p)

    def distance(self, p):
        return self.rectangle.distance(p)

    def __repr__(self):
        return "N[\n  rectangle: {}\n  children: {}\n  leaf: {}\n]".format(repr(self.rectangle), repr(self.children), self.is_leaf)

    def print_depth(self, depth=0):
        if self.is_leaf:
            print(depth, end=' ')
        else:
            for child in self.children:
                child.print_depth(depth+1)


class Rtree:

    def __init__(self) -> None:
        self.root = Node(is_leaf=True)

    def recursive_insert(self, node: Node, point):
        if node.is_leaf:
            return node.leaf_insert(point)
        for child in node.children:
            if child.contains_point(point):
                is_split, new_node = self.recursive_insert(child, point)
                if new_node is not None:
                    return is_split, Node(is_leaf=False, children=[new_node])
                return is_split, new_node
        closest_rect = None
        closest_distance = True
        closest_distance = float('inf')
        for child in node.children:
            distance = child.distance(point)
            if distance < closest_distance:
                closest_distance = distance
                closest_rect = child
        is_split, new_node = self.recursive_insert(
            closest_rect, point)
        closest_rect.update_rectangle()
        if is_split:
            return node.inter_insert(new_node)
        return False, None

    def update_root(self, is_split, node):
        if is_split:
            self.root = Node(is_leaf=False, children=[self.root, node])

    def insert(self, p):
        self.update_root(*self.recursive_insert(self.root, p))

    def find(self, p):
        return self.root.find(p)

    def range(self, rect):
        return sorted(self.root.range(rect))

    def __repr__(self):
        return repr(self.root)

    def print_depth(self):
        return self.root.print_depth()


if __name__ == '__main__':
    import sys
    import os
    assert len(sys.argv) == 2, "Usage: python3 rtree.py <input_file>"
    assert os.path.isfile(sys.argv[1]), "{} not found".format(sys.argv[1])
    tree = Rtree()
    with open(sys.argv[1]) as f:
        line = f.readline()
        while line:
            line = line.strip().split(' ')
            if line[0] == 'INSERT':
                tree.insert(point(*line[1].lstrip('(').rstrip(')').split(',')))
            elif line[0] == 'FIND':
                print(
                    tree.find(point(*line[1].lstrip('(').rstrip(')').split(','))))
            elif line[0] == 'RANGE':
                points = line[1].lstrip('(').rstrip(')').split(',')
                print(tree.range(
                    Rectangle(point(points[0], points[1]), point(points[2], points[3]))))
                # print("tree:\n", tree)
            line = f.readline()
