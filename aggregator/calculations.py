import math


class Point():

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


class CleanedCircle():

    def __init__(self, x, y, radius, tag, bs):
        self.x = float(x)
        self.y = float(y)
        self.r = radius
        self.tag = tag
        self.bs = bs


class Circle:

    def __init__(self, x, y, rssi, tag, bs):
        self.x = float(x)
        self.y = float(y)
        self.r = self.rssi_to_distance(rssi)
        self.tag = tag
        self.bs = bs

    def rssi_to_distance(self, rssi):
        A = 63
        nAi = 1.76

        power = (rssi - A) / (10 * nAi)
        d = (10 ** power)

        return d


def find_position(circles):
    """Finds the common intersection of a list of circles."""

    intersections = []

    for i in circles:
        for j in circles:
            if i.bs == j.bs:
                pass
            elif does_intersect(i, j):
                intersections.extend(find_intersections(i, j))
            else:
                pass

    if len(intersections) > 2:
        centroid = find_multi_centroid(intersections)
        return centroid
    else:
        return False


def find_distance(p1, p2):
    """Finds the distance between two points.

    Takes an input of two points.
    Outputs a distance value.
    """
    px = (p1.x - p2.x) ** 2
    py = (p1.y - p2.y) ** 2
    p = px + py
    d = math.sqrt(p)

    return d


def find_centroid(p1, p2):
    """Finds the center of two points.

    Takes an input of two points.
    Outputs a point.
    """

    x = (p1.x + p2.x) / 2
    y = (p1.y + p2.y) / 2
    avg = Point(x, y)

    return avg


def find_multi_centroid(points):
    """Finds the center of a list of intersection points.

    Takes an input of a list of points.
    Outputs a point.
    """

    centroid = find_centroid(points[0], points[1])
    for x in points[1:]:
        centroid = find_centroid(centroid, x)

    return centroid


def does_intersect(c1, c2):
    """Finds if two circles intersect.

    Takes an input of two cirlces.

    Will return True if they intersect, False if they do not,
    and 'pass' if one is inside the other.
    """

    if c1.r <= c2.r:
        pass
    else:
        temp = c1
        c1 = c2
        c2 = temp

    c1Point = Point(c1.x, c1.y)
    c2Point = Point(c2.x, c2.y)
    d = find_distance(c1Point, c2Point)

    if d > (c2.r + c1.r):
        val = False
        return val
    elif d < (c2.r - c1.r):
        val = 'pass'
        return val
    else:
        val = True
        return val


def find_intersections(c1, c2):
    """Finds the intersections between two circles.

    Takes an imput of two circles.

    Outputs the intersection points between the circles as two points in
    a list.
    """

    c1Point = Point(c1.x, c1.y)
    c2Point = Point(c2.x, c2.y)
    d = find_distance(c1Point, c2Point)

    deltaX = c2.x - c1.x
    deltaY = c2.y - c1.y

    s = ((d ** 2) + (c1.r ** 2) - (c2.r ** 2)) / (2 * d)

    cX = c1.x + (deltaX * s) / d
    cY = c1.y + (deltaY * s) / d

    u = math.sqrt(math.fabs((c1.r ** 2) - (s ** 2)))

    dX = cX - (deltaY * u) / d
    dY = cY + (deltaX * u) / d
    eX = cX + (deltaY * u) / d
    eY = cY + (deltaX * u) / d

    pointD = Point(dX, dY)
    pointE = Point(eX, eY)

    points = [pointD, pointE]

    return points


def find_closest_pair(points):
    """Finds the two closest points.

    Takes an input of a list of points.

    Outputs a pair of points in a list.
    """

    distance = 999999

    for i in points[:-1]:
        for j in points[1:]:
            if find_distance(i, j) < distance:
                pair = (i, j)
                distance = find_distance(i, j)

    return pair


def find_closest_to(point, points):
    """From a list, finds the closest point to the specified point.

    Takes an input of a single point, and
    a list of points.

    Outputs the point that was closest.
    """

    distance = find_distance(point, points[0])
    found = points[0]

    for i in points[1:]:
        if find_distance(point, i) < distance:
            found = i
            distance = find_distance(point, i)

    return found
