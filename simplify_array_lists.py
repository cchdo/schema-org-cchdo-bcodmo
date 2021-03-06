# https://github.com/omarestrella/simplify.py/blob/master/simplify.py

# Written for when points defined as An array of dictionaries, containing x, y coordinates: {'x': int/float, 'y': int/float}

# modified for lon/lat list where points are an array of lists containing lon at array index 0 and lat at array index 1

def getSquareDistance(p1, p2):
    """
    Square distance between two points
    """
    #dx = p1['x'] - p2['x']
    #dy = p1['y'] - p2['y']

    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return dx * dx + dy * dy


def getSquareSegmentDistance(p, p1, p2):
    """
    Square distance between point and a segment
    """
    # x = p1['x']
    # y = p1['y']

    # dx = p2['x'] - x
    # dy = p2['y'] - y

    x = p1[0]
    y = p1[1]

    dx = p2[0] - x
    dy = p2[1] - y

    if dx != 0 or dy != 0:
        #t = ((p['x'] - x) * dx + (p['y'] - y) * dy) / (dx * dx + dy * dy)
        t = ((p[0] - x) * dx + (p[1] - y) * dy) / (dx * dx + dy * dy)

        if t > 1:
            # x = p2['x']
            # y = p2['y']
            x = p2[0]
            y = p2[1]

        elif t > 0:
            x += dx * t
            y += dy * t

    # dx = p['x'] - x
    # dy = p['y'] - y

    dx = p[0] - x
    dy = p[1] - y

    return dx * dx + dy * dy


def simplifyRadialDistance(points, tolerance):
    length = len(points)
    prev_point = points[0]
    new_points = [prev_point]

    for i in range(length):
        point = points[i]

        if getSquareDistance(point, prev_point) > tolerance:
            new_points.append(point)
            prev_point = point

    if prev_point != point:
        new_points.append(point)

    return new_points


def simplifyDouglasPeucker(points, tolerance):
    length = len(points)
    markers = [0] * length  # Maybe not the most efficent way?

    first = 0
    last = length - 1

    first_stack = []
    last_stack = []

    new_points = []

    markers[first] = 1
    markers[last] = 1

    while last:
        max_sqdist = 0

        for i in range(first, last):
            sqdist = getSquareSegmentDistance(points[i], points[first], points[last])

            if sqdist > max_sqdist:
                index = i
                max_sqdist = sqdist

        if max_sqdist > tolerance:
            markers[index] = 1

            first_stack.append(first)
            last_stack.append(index)

            first_stack.append(index)
            last_stack.append(last)

        # Can pop an empty array in Javascript, but not Python, so check
        # the length of the list first
        if len(first_stack) == 0:
            first = None
        else:
            first = first_stack.pop()

        if len(last_stack) == 0:
            last = None
        else:
            last = last_stack.pop()

    for i in range(length):
        if markers[i]:
            new_points.append(points[i])

    return new_points


def simplify(points, tolerance=0.1, highestQuality=True):
    sqtolerance = tolerance * tolerance

    if not highestQuality:
        points = simplifyRadialDistance(points, sqtolerance)

    points = simplifyDouglasPeucker(points, sqtolerance)

    return points
