
'''
   This is my implementation of a WEIGHTED UNDIRECTED complete graph as an adjacency list,
   modified to only store the vertex coordinates and not every single edge connecting them.
   This can work because this is a complete graph, so there is implicitly an edge from each
   vertex to every other vertex, and the "weight" of the edge can be computed as needed from
   the pair of vertex coordinates. Doing this saves memory, and when the number of vertices
   is very large, this is actually needed to not hinder run-time, as simply instantiating
   and saving all of those values in memory takes too much time.
'''


import math


class Graph:
    def __init__(self, num_verts=0):
        self.vertices = [[0., 0.] for _ in range(num_verts)]  # store coords not distances
        self.num_verts = num_verts


    def set_num_verts(self, num_verts=0):
        self.vertices = [[0., 0.] for _ in range(num_verts)]  # store coords not distances
        self.num_verts = num_verts


    def add_vertex(self, vert: int, x: float, y: float):
        self.vertices[vert] = [x, y]


    def min_tour_TSP_nn_heur(self):
        ''' Compute the nearest neighbor heuristic minimum tour to roughly solve the TSP problem '''
        tour_len = 0
        visited = [False for _ in range(self.num_verts)]
        last_visit = 0  # start our tour at the first vertex
        visited[0] = True  # add first vertex to list of visited vertices
        num_visited = 1

        while num_visited < self.num_verts:
            # go to the nearest neighbor of last_visit. we haven't visited every vertex yet bc we are inside
            # the loop, so we are guaranteed to find a new vertex to step to, as we constrain this to be a
            # completely connected graph (i.e. every vertex is connected to every other vertex)
            nn = None
            min_dist = float('inf')

            for neighbor,seen in enumerate(visited):
                if seen: continue

                dx = self.vertices[last_visit][0] - self.vertices[neighbor][0]
                dy = self.vertices[last_visit][1] - self.vertices[neighbor][1]
                dist = dx**2 + dy**2  # squared euclidean distance

                if dist < min_dist:
                    min_dist = dist
                    nn = neighbor
                elif dist == min_dist:  # only update if vertex index is smaller
                    if neighbor < nn:
                        nn = neighbor

            # we found the nearest neighbor, add it to path tour, update last_visit, increment ctr
            visited[nn] = True
            tour_len += math.sqrt(min_dist)  # adding actual euclidean distance to our tour len
            last_visit = nn
            num_visited += 1

            #if num_visited % 5000 == 0:  # print for benchmarking time of algorithm completion
            #    print('adding batch of 5000 vertices to our TSP tour...')

        # our tour is finished, now we need to return from our last vertex back to the first
        dx = self.vertices[0][0] - self.vertices[last_visit][0]
        dy = self.vertices[0][1] - self.vertices[last_visit][1]
        tour_len += math.sqrt(dx**2 + dy**2)

        return int(tour_len // 1)  # round down to nearest int
