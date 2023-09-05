import random
from math import dist
import heapq

def GeneratePoint(start, end):

    x = random.randrange(start[0], end[0])
    y = random.randrange(start[1], end[1])
    z = random.randrange(start[2], end[2])

    point = (x, y, z)
    return point

def FindShortestPath(listOfPoints):
   
    # listOfPoints.sort(key=lambda point: dist((0, 0, 0), point))
    listOfPoints = sorted(listOfPoints)
    
    # Create a graph representation with distances between points.
    graph = {}
    count = 1
    for i in listOfPoints:
        graph[count] = i
        count += 1
    
    # Dijkstra's algorithm
    source = 0
    destination = len(listOfPoints) - 1
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    priority_queue = [(0, source)]  # (distance, node)
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node == destination:
            break
        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    shortest_path = []
    current_node = destination
    while current_node is not None:
        shortest_path.append(listOfPoints[current_node])
        current_node = min((neighbor for neighbor in graph[current_node] if neighbor in visited),
                           key=lambda neighbor: distances[neighbor], default=None)
    shortest_path.reverse()
    
    return shortest_path
            

test = ((100,200,300), (200,500,1231), (123123,123123,123), (12312,1231,312))
shortestPath = FindShortestPath(test)

print(shortestPath)