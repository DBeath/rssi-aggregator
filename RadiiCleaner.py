from collections import Counter

# def clean_circles(circles):
#     radius = 0

#     for i in circles:
#         radius += i.r

#     num = len(circles)
#     if num > 0:
#         clean = radius / num

#     return clean


def clean_circles_old(circles):
    rads = []
    for i in circles:
        rads.append(i.r)

    counts = Counter(rads).most_common(3)

    numRads = len(rads)

    if (counts[0][1] / numRads) > 0.7:
        return counts[0][1]

    elif ((counts[0][1] + counts[1][1]) / numRads) > 0.8:
        topOne = counts[0][1] * counts[0][0]
        topTwo = counts[1][1] * counts[1][0]
        base = counts[0][0] + counts[1][0]
        return (topOne + topTwo) / base

    elif ((counts[0][1] + counts[1][1] + counts[2][1]) / numRads) > 0.9:
        topOne = counts[0][1] * counts[0][0]
        topTwo = counts[1][1] * counts[1][0]
        topThree = counts[2][1] * counts[2][0]
        base = counts[0][0] + counts[1][0] + counts[2][0]
        return (topOne + topTwo + topThree) / base

    else:
        radius = 0

        for i in circles:
            radius += i.r

        num = len(circles)
        if num > 0:
            clean = radius / num

        return clean


def clean_circles(circles):
    """Finds the weighted average of the ten most common radii.

    Takes and input of a list of circles.
    Outputs a singe radius value.
    """
    rads = []
    for i in circles:
        rads.append(i.r)

    counts = Counter(rads).most_common(10)
    # counts[0][0] is the radius value, counts[0][1] is the number of times
    # that value occurs.

    top = 0
    base = 0

    for i in counts:
        top += i[1] * i[0]
        base += i[1]

    return top / base


def CleanCircles(circleList):

    circleBucket = Array.CreateInstance(int, 100)
    largestCounts = Array.CreateInstance(int, 3)
    count = 0
    enumerator = circleList.GetEnumerator()

    while enumerator.MoveNext():
        circle = enumerator.Current
        circleBucket[circle.Radius] += 1
        count += 1
    i = 0

    while i < 100:
        if circleBucket[i] > circleBucket[largestCounts[0]]:
            largestCounts[2] = largestCounts[1]
            largestCounts[1] = largestCounts[0]
            largestCounts[0] = i

        elif circleBucket[i] > circleBucket[largestCounts[1]]:
            largestCounts[2] = largestCounts[1]
            largestCounts[1] = i

        elif circleBucket[i] > circleBucket[largestCounts[2]]:
            largestCounts[2] = i
        i += 1

    test1 = circleBucket[largestCounts[0]] / count
    test2 = (circleBucket[largestCounts[0]] + circleBucket[largestCounts[1]]) / count
    test3 = (circleBucket[largestCounts[0]] + circleBucket[largestCounts[1]] + circleBucket[largestCounts[2]]) / count

    if test1 > 0.7:
        return Circles(circleList[0].Position, largestCounts[0])

    elif test2 > 0.8:
        radius = 0
        topOne = largestCounts[0] * circleBucket[largestCounts[0]]
        topTwo = largestCounts[1] * circleBucket[largestCounts[1]]
        baseOne = circleBucket[largestCounts[0]] + circleBucket[largestCounts[1]]
        radius = (topOne + topTwo) / baseOne
        return Circles(circleList[0].Position, radius)

    elif test3 > 0.9:
        radius = 0
        topOne = largestCounts[0] * circleBucket[largestCounts[0]]
        topTwo = largestCounts[1] * circleBucket[largestCounts[1]]
        topThree = largestCounts[2] * circleBucket[largestCounts[2]]
        baseOne = circleBucket[largestCounts[0]] + circleBucket[largestCounts[1]] + circleBucket[largestCounts[2]]
        radius = (topOne + topTwo + topThree) / baseOne
        return Circles(circleList[0].Position, radius)

    else:
        raise InconclusiveException("Not enough valid Points")

CleanCircles = staticmethod(CleanCircles)
