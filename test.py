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
    print("Printing ordered path")
    print(ordered_path) 
    return ordered_path

# test = [(100, 200, 300), (200, 500, 1231), (123123, 123123, 123), (12312, 1231, 312), (1213,123,2), (12313,7567,567), (5346,5,34)]
# shortestPath = NearestNeighborTSP(test)

# print(shortestPath)

def funct(startX, startY, startZ, xTravel, yTravel, zTravel):

    p1 = (startX, startY, startZ)
    p2 = ((startX + xTravel), (startY + yTravel), (startZ + zTravel))

    index = 0

    point_count = 0
    point_list = []
    selected_points = []

    minDist = 50
    while len(selected_points) <= 14:
        point = GeneratePoint(p1, p2)
        point_list.append(point)

        for p in point_list:
            if dist(p, point) > minDist:
                if point not in selected_points:
                    selected_points.append(point)
                    point_count += 1

            else:
                break

        # if dist(previousPoint, point) > minDist:
        #     selected_points.append(point)
        #     point_count += 1
        #     previousPoint = point

    path = NearestNeighborTSP(selected_points)
    # print(path)

    print("printing points...")
    for points in path:
        index += 1
        print(f"p{index} {points}")

funct(100,100,100,500,500,5000)