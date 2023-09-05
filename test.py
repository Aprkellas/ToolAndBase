import random
from math import dist

def GeneratePoint(start, end):
    x = random.randrange(start[0], end[0])
    y = random.randrange(start[1], end[1])
    z = random.randrange(start[2], end[2])
    point = (x, y, z)
    return point

def NearestNeighborTSP(listOfPoints):
    current_point = listOfPoints[0]
    ordered_path = [current_point]
    unvisited_points = listOfPoints[1:]

    while unvisited_points:
        nearest_point = min(unvisited_points, key=lambda point: dist(current_point, point))
        ordered_path.append(nearest_point)
        current_point = nearest_point
        unvisited_points.remove(nearest_point)

    ordered_path.append(ordered_path[0])

    return ordered_path

test = [(100, 200, 300), (200, 500, 1231), (123123, 123123, 123), (12312, 1231, 312), (1213,123,2), (12313,7567,567), (5346,5,34)]
shortestPath = NearestNeighborTSP(test)

print(shortestPath)
