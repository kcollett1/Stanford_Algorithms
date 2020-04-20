'''
    this is my implementation of an undirected graph as an adjacency
    list representation. vertices are added to the graph from input
    containing the vertex num and a list of vertices connected to it.
    two vertices can be merged into one, picking one of them to keep
    and moving all edges connected to the other over to the one we
    are keeping (deleting any self-loops). Karger's randomized contraction
    algorithm is also implemented to find a minimum cut of a graph.
'''

from copy import deepcopy as dcopy
from numpy import random as nprand


class Graph:
    def __init__(self):
        # dict of vertices, mapped to a set of edges incident on it
        self.vertices = {}  # vertex #: set(edge i, edge j, ...)
        # dict of edges, mapped to a list of the two endpoints of edge
        self.edges = {}  # edge #: [v1,v2]
        self.num_edges = 0
        self.num_verts = 0


    def copy(self):
        new_graph = Graph()
        new_graph.vertices = dcopy(self.vertices)
        new_graph.edges = dcopy(self.edges)
        new_graph.num_edges = int(self.num_edges)
        new_graph.num_verts = int(self.num_verts)
        return new_graph


    def __add_edge_to_vert__(self, vert: int):
        '''Helper function for add_new_edge to add edge to vert's set.'''
        if vert in self.vertices:
            self.vertices[vert].add(self.num_edges)
        else:
            self.num_verts += 1
            self.vertices[vert] = {self.num_edges}


    def __add_new_edge__(self, vert1: int, vert2: int):
        '''Helper function for add_vertex to add an edge between vert1 and vert2.'''
        self.num_edges += 1
        self.edges[self.num_edges] = [vert1, vert2]
        self.__add_edge_to_vert__(vert1)
        self.__add_edge_to_vert__(vert2)


    def add_vertex(self, vert_num: int, connected_verts: list):
        '''
            Given a vertex and a set of vertices it's connected to, add all
            necessary info  and cross-pointers to add vertex to object.
        '''
        if not connected_verts:  # allow for unconnected vertices in graph
            self.num_verts += 1
            self.vertices[vert_num] = set()  # empty set, no incident edges on this vertex

        for vert in connected_verts:
            if vert not in self.vertices:  # new vertex/edge we haven't seen yet, O(1) lookup
                self.__add_new_edge__(vert, vert_num)
            else:  # already seen vertex, but possibly not edge
                for edge in self.vertices[vert]: # look for vertex in edge tuples
                    if vert_num in self.edges[edge]:
                        # already seen this edge and added all necessary info
                        break
                else:  # no break - didn't find edge, therefore this is a new edge
                    self.__add_new_edge__(vert, vert_num)


    def merge_vertices(self, edge_num: int):
        '''Given an edge, merge the vertices that it connects into one vertex'''
        (v1, v2) = self.edges[edge_num]  # the two vertices we are merging
        self.num_verts -= 1  # each merge, we remove one vertex from the graph
        self.num_edges -= 1  # each merge, we also remove at least one edge

        # first remove edge_num from both vertices and edge list
        self.vertices[v1].remove(edge_num)
        self.vertices[v2].remove(edge_num)
        self.edges.pop(edge_num)

        # get number of edges on each vertex and set source,dest
        v1_edges = len(self.vertices[v1])
        v2_edges = len(self.vertices[v2])
        if v1_edges <= v2_edges:
            source = v1
            dest = v2
        else:
            source = v2
            dest = v1

        # move over edges from source onto dest
        # for every edge we move, we need to update the self.edges[edge] list to dest not source
        for edge in self.vertices[source]:
            if dest in self.edges[edge]:  # this will be a self-loop, let's get rid of it
                self.num_edges -= 1
                self.edges.pop(edge)
                self.vertices[dest].remove(edge)
            else:  # move it from source onto dest
                self.edges[edge] = [v if v != source else dest for v in self.edges[edge]]
                self.vertices[dest].add(edge)

        # finally, remove source vertex!
        self.vertices.pop(source)


    def __find_cut__(self, g) -> int: #(int, (set,set)):
        '''
            Helper function to find_min_cut. This function actually implements
            one iteration of Karger's contraction algorithm.
        '''
        while g.num_verts > 2:
            # pick a uniformally distributed random edge from edges remaining
            rand_edge = list(g.edges)[nprand.randint(0, g.num_edges)]
            # merge the two vertices that this edge connects
            g.merge_vertices(rand_edge)
 
        # return the number of crossing edges by the cut found using this algorithm
        return g.num_edges
 
 
    def find_min_cut(self, sample_size=10) -> int:
        '''
            Use Karger's randomized algorithm to contract vertices on a graph
            until there are only two left to find a cut. This function takes a
            graph as input, and outputs the minimum number of crossing vertices.
            If we use a large enough sample size (~ n^2 * log(n)), it is statistically
            very unlikely that the answer given from this algorithm is wrong.
        '''
        min_cut = float('inf')
 
        for _ in range(sample_size):
            min_cut_sample = self.__find_cut__(g=self.copy())  # run iteration on deep copy of the graph
            #(min_cut_sample, (cut_a, cut_b)) = find_cut(test_graph.copy())
            if min_cut_sample < min_cut:
                min_cut = min_cut_sample
 
        return min_cut


