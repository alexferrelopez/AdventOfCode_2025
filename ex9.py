def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.start = point1
        self.end = point2

        if point1.x == point2.x:
            self.orientation = "vertical"
            if self.start.y > self.end.y:
                self.start, self.end = self.end, self.start
        elif point1.y == point2.y:
            self.orientation = "horizontal"
            if self.start.x > self.end.x:
                self.start, self.end = self.end, self.start

    def point_on_line(self, p):
        if self.orientation == "vertical":
            return p.x == self.start.x and self.start.y <= p.y <= self.end.y
        elif self.orientation == "horizontal":
            return p.y == self.start.y and self.start.x <= p.x <= self.end.x
        return False


valid_points = {}


class Rectangle:
    def __init__(self, point1, point2):
        self.lower_left_point = Point(min(point1.x, point2.x), min(point1.y, point2.y))
        self.lower_right_point = Point(max(point1.x, point2.x), min(point1.y, point2.y))
        self.upper_left_point = Point(min(point1.x, point2.x), max(point1.y, point2.y))
        self.upper_right_point = Point(max(point1.x, point2.x), max(point1.y, point2.y))
        self.area = self.calc_area()

    def calc_area(self):
        return (abs(self.lower_left_point.x - self.upper_right_point.x) + 1) * (
                abs(self.lower_left_point.y - self.upper_right_point.y) + 1)

    def is_inside_polygon(self, valid_points):
        vertices = [self.lower_left_point, self.lower_right_point, self.upper_left_point, self.upper_right_point]

        for vertex in vertices:
            if point_is_in_valid_range(vertex, valid_points):
                continue
            else:
                return False

        for y in [self.lower_left_point.y, self.upper_left_point.y]:
            if range_is_in_valid_range([self.lower_left_point.x + 1, self.lower_right_point.x], valid_points, y):
                continue
            else:
                return False

        for y in range(self.lower_left_point.y + 1, self.upper_left_point.y):
            for x in [self.lower_left_point.x, self.lower_right_point.x]:
                if point_is_in_valid_range(Point(x, y), valid_points):
                    continue
                else:
                    return False

        return True


def point_on_any_line(p, lines):
    for line in lines:
        if line.point_on_line(p):
            return True

    return False


def get_edges(vertices):
    edges = []
    for i in range(len(vertices)):
        edges.append(Line(vertices[i - 1], vertices[i]))

    return edges


def point_is_in_valid_range(p, valid_points):
    x_ranges = valid_points[p.y]
    for i in range(0, len(x_ranges), 2):
        if x_ranges[i] <= p.x <= x_ranges[i + 1]:
            return True
    return False


def range_is_in_valid_range(x_range, valid_points, y):
    x_ranges = valid_points[y]
    for i in range(0, len(x_ranges), 2):
        if x_range[0] >= x_ranges[i] and x_range[1] <= x_ranges[i + 1]:
            return True
    return False


def point_is_inside_polygon(p, vertical_lines, horizontal_start_points):
    intersect_count = 0
    for i in range(len(vertical_lines)):
        line = vertical_lines[i]
        if line.start.x <= p.x:
            continue

        elif line.start.y < p.y < line.end.y:
            intersect_count += 1

        elif line.start.y == p.y or line.end.y == p.y:
            if f"{line.start.x},{line.start.y}" in horizontal_start_points or f"{line.end.x},{line.end.y}" in horizontal_start_points:
                # point intersects vertically with the starting or ending point of a vertical line
                next_vert_line: Line = vertical_lines[(i + 1) % len(vertical_lines)]
                prev_vert_line: Line = vertical_lines[(i - 1)]

                vert_line_to_the_right = next_vert_line

                if next_vert_line.start.x < prev_vert_line.start.x:
                    vert_line_to_the_right = prev_vert_line

                if line.start.y == vert_line_to_the_right.end.y or line.end.y == vert_line_to_the_right.start.y:
                    intersect_count += 1

    return intersect_count % 2 == 1


def calculate_valid_point_ranges(maxy, miny, sorted_edges: list):
    valid_points = {i: [] for i in range(miny, maxy + 1)}

    for i in range(miny, maxy + 1):
        # filter edges that are in the current y
        filtered_edges = list(filter(lambda e: e.start.y <= i <= e.end.y, sorted_edges))
        possible_wall = False
        last_direction = None

        for j, edge in enumerate(filtered_edges):
            match edge.orientation:
                case "vertical":
                    if i == edge.start.y or i == edge.end.y:
                        if j < len(filtered_edges) - 1 and filtered_edges[j + 1].orientation == "horizontal":
                            valid_points[i].append(edge.start.x)
                            possible_wall = True
                            if edge.start.y == i:
                                last_direction = "upwards"
                            else:
                                last_direction = "downwards"
                            continue

                        if possible_wall:
                            if ((edge.start.y == i and last_direction == "upwards") or
                                    (edge.end.y == i and last_direction == "downwards")):
                                valid_points[i].append(edge.start.x)

                            possible_wall = False
                    else:
                        valid_points[i].append(edge.start.x)

    return valid_points


def run_ex(file):
    lines = [line.split(",") for line in read_file(file)]

    vertices = [Point(int(line[0]), int(line[1])) for line in lines]

    edges = get_edges(vertices)

    # vertical_lines = [e for e in edges if e.orientation == "vertical"]
    # horizontal_lines = [e for e in edges if e.orientation == "horizontal"]

    # horizontal_start_points = {f"{h.start.x},{h.start.y}" for h in horizontal_lines}

    sorted_edges = sorted(edges, key=lambda e: e.orientation, reverse=True)
    sorted_edges.sort(key=lambda e: e.start.x)

    miny = min([v.y for v in vertices])
    maxy = max([v.y for v in vertices])
    minx = min([v.x for v in vertices])
    maxx = max([v.x for v in vertices])

    valid_points = calculate_valid_point_ranges(maxy, miny, sorted_edges)

    '''
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            vertex = Point(x, y)
            if point_is_in_valid_range(vertex, valid_points):
                pass
                print("#", end="")
            else:
                pass
                print(".", end="")

        print()
    '''

    max_area = 0
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            r = Rectangle(vertices[i], vertices[j])
            if r.area > max_area and r.is_inside_polygon(valid_points):
                max_area = r.area

    print(max_area)

    return max_area


if __name__ == '__main__':
    # 2,5 and 9,7
    r = Rectangle(Point(2, 5), Point(9, 7))
    assert r.area == 24

    a = run_ex('ex9_1_input_example')
    if a == 24:
        print("Example test passed")

    run_ex('ex9_1_input')
