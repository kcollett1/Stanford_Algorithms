'''
    this is my implementation of a WEIGHTED UNDIRECTED graph as an adjacency
    list representation, from a previous section, with some slight modifications
    made for application to kruskal's MST finding greedy algorithm.
'''

from heap import *


class Vert_Edge:
    def __init__(self, vert=None, min_edge=float('inf')):
        self.vert = vert
        self.min_edge = min_edge

    def set_edge_len(self, new_edge_len):
        self.min_edge = new_edge_len

    # make all ordering comparisons based on min_edge
    def __lt__(self, other): return self.min_edge < other.min_edge
    def __le__(self, other): return self.min_edge <= other.min_edge
    def __gt__(self, other): return self.min_edge > other.min_edge
    def __ge__(self, other): return self.min_edge >= other.min_edge
    def __eq__(self, other): return self.min_edge == other.min_edge
    def __ne__(self, other): return self.min_edge != other.min_edge


class Graph:
    def __init__(self):
        # dict of vertices, mapped to a set of its incident edges
        self.vertices = {}  # vertex #: set(edge i, edge j, ...)
        # dict of edges, mapped to a list of the two endpoints and it's weight
        # ex: edge #: [v1,v2,w]; i.e. {3:[2,3,10]} edge3 connects vert2 and vert3 with weight 10
        self.edges = {} 
        self.num_edges = 0
        self.num_verts = 0


    def __update_vert__(self, vert):
        '''Helper function to add_edge to add current edge number to vertex dict'''
        if vert in self.vertices:
            self.vertices[vert].add(self.num_edges)
        else:
            self.num_verts += 1
            self.vertices[vert] = {self.num_edges}

    def add_edge(self, vert1: int, vert2: int, weight: int):
        '''Add a new edge to the graph connecting vert1 and vert2 with weight of weight'''
        # increment number of edges and add vertex pointers to this edge
        self.num_edges += 1
        self.edges[self.num_edges] = [vert1, vert2, weight]

        # add both vertices/edge# to vertex dict (and increment number of vertices if needed)
        self.__update_vert__(vert1)
        self.__update_vert__(vert2)


    def compute_minspantree(self):
        '''
           Use Prim's algorithm to compute the MST of the graph. This function uses a
           min-heap data structure to keep track of next edge to look at, runs in O(m*log(n))
           time. The return value here is simply the sum of all edge costs belonging to the MST.
        '''
        # initialize len of MST and a min heap to store all vertices and the shortest edge
        # len incident on it add all vertices to heap as data structure Vert_Edge, with
        # +inf as initial edge len and set source vertex edge len to be 0
        MST_len = 0
        source = list(self.vertices.keys())[0]  # pick an arbitrary vertex to start with
        remaining_verts = MinHeap()
        for vert in self.vertices:
            remaining_verts.insert(Vert_Edge(vert))
        remaining_verts.delete(source)
        remaining_verts.insert(Vert_Edge(vert=source, min_edge=0))

        while remaining_verts.size != 0:  # O(1)
            # extract min from heap - this vertex gets added to our "conquered" vertices
            # and its shortest qualifying edge len (which is in heap) gets added to MST len
            next_ve = remaining_verts.extract_min()  # this vertex is no longer in our heap, O(log(n))
            vert = next_ve.vert
            edge = next_ve.min_edge
            MST_len += edge

            # go through all edges vert connects to in this graph, if connecting vert
            # is not in heap we don't care. otherwise, find it in the heap, and check
            # if we need to update the shortest edge len
            for edge in self.vertices[vert]:
                # extract the vertex and edge length that this edge contains
                dest_vert = self.edges[edge][0] if self.edges[edge][0] != vert else self.edges[edge][1]
                edge_len = self.edges[edge][2]

                # check if this vertex is in the heap, and if so find it's index
                heap_ind = remaining_verts.find(dest_vert)
                if heap_ind == None:  # this vertex has already been explored, we can skip this
                    continue

                # otherwise we need to update the path len of this vertex in the heap
                # the heap data structure will automatically compare the values and only
                # change it if it is smaller than the current path len, and sift accordingly
                remaining_verts.update_len(vert=dest_vert, new_len=edge_len)

        return MST_len
