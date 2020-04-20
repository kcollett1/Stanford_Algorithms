
'''
    this is my implementation of a DIRECTED unweighted graph as an adjacency list.
    note there are many different types of graphs and thus I have implemented throughout
    the courses and weeks different Graph class objects; this is only one representation
    with some base functionalities. For further examples of Graph structures with other
    functionalities, see the specific graph.py files in some course*/week*/ folders.
'''

from copy import deepcopy as dcopy
from stack import Stack
from queue import Queue


class Graph:
    def __init__(self):
        # dict of vertices, mapped to a list of sets of its outgoing/incoming edges
        self.vertices = {}
        # dict of edges, mapped to a list of the two endpoints of edge, in order of direction
        self.edges = {}  # edge #: [v1,v2]; i.e. {3:[3,2]} edge# 3 points FROM vert 3 TO vert 2
        self.num_edges = 0
        self.num_verts = 0
        self.max_vert = 0  # track verts that exist on graph without incident edges


    def copy(self):
        new_graph = Graph()
        new_graph.vertices = dcopy(self.vertices)
        new_graph.edges = dcopy(self.edges)
        new_graph.num_edges = int(self.num_edges)
        new_graph.num_verts = int(self.num_verts)
        return new_graph


    def __update_vert__(self, vert, ind):
        '''Helper function to add_edge to add current edge number to vertex dict'''
        if vert not in self.vertices:
            self.num_verts += 1
            if vert > self.max_vert:
                self.max_vert = vert
            self.vertices[vert] = [set(), set()]
        self.vertices[vert][ind].add(self.num_edges)


    def add_edge(self, vert1: int, vert2: int):
        '''Add a new edge to the graph pointing from vert1 to vert2'''
        # increment number of edges and add vertex pointers to this edge
        self.num_edges += 1
        self.edges[self.num_edges] = [vert1, vert2]

        # add both vertices/edge# to vertex dict (and increment number of vertices if needed)
        self.__update_vert__(vert1, 0)
        self.__update_vert__(vert2, 1)


    def add_vert(self, vert):
        ''' Add a vertex to the graph not connected to any edges '''
        if vert not in self.vertices:
            self.num_verts += 1
            if vert > self.max_vert:
                self.max_vert = vert
            self.vertices[vert] = [set(), set()]


    def BFS(self, start: int, forwards=True):
        ''' Breadth first search from start vertex. Can search reverse graph with forwards=False '''
        # initialize all vertices as unexplored except for start vertex
        explored = set()
        explored.add(start)

        # initialize queue to track next vertices to explore, enqueue start vertex
        verts = Queue()
        verts.enqueue(start)

        # while queue is not empty, keep exploring vertices
        while not verts.is_empty():
            # dequeue next vertex and try to explore any incident edges it has
            vert = verts.dequeue()

            # go through all edges outgoing from this vertex
            for edge in self.vertices[vert][0]:
                # get vertex corresponding to this edge
                # if going through G, current vert will be 1st; next_vert is in pos 1 (True)
                # if going through G_rev, current vert will be 2nd; next_vert is in pos 0 (False)
                next_vert = self.edges[edge][forwards]

                # only interested in unexplored vertices
                if next_vert in explored:
                    continue

                # this is a vertex of interest, mark as explored and add to queue
                explored.add(next_vert)
                verts.enqeue(next_vert)


    def DFS(self, start, forwards=True):
        '''
           Depth first search from start vertex, helper method for compute_scc. Can search reverse graph
           with forwards=False. This DFS method uses an iterative search rather than a recursive search
           as this is more memory efficient for large graphs, though tracking the finishing time bcomes
           slightly more tricky. Instead of tracking just if a node is explored or not, we also need to
           track a third status, "explored but not finished". This is particularly important in cases
           where we take a vertex from the top of the stack, and see that all of it's neighbors have
           already been explored - are all of it's neighbors actually finished being explored or are
           they possibly still in the stack waiting to be assigned a finish time?
        '''
        global leaders, leader, finish_times, finish_time, explored

        verts = Stack()
        verts.push(start)
        if forwards:  # we only care about tracking leaders in forwards pass through graph
            leaders[leader] = {start}

        while not verts.is_empty():
            vert = verts.top()  # which vertex is currently first in the stack
            if vert not in explored:
                # haven't "explored" yet - add all neighbors to stack if they haven't been explored yet
                # note here we may be double adding vertices to the stack, but when we get to it again
                # we will check if it's already been explored and if so we mark it's finish time if needed
                explored.add(vert)
                for edge in self.vertices[vert][(int(forwards)+1)%2]:
                    next_vert = self.edges[edge][int(forwards)]
                    if next_vert not in explored:
                        if forwards:  # we only care about tracking leaders in forwards pass
                            leaders[leader].add(next_vert)
                        verts.push(next_vert)
            else:
                # completely finished exploring this node, remove from stack, set finishing time if needed
                # on first pass through, we set every nodes finish time, so on forward pass through graph
                # we will never set any finishing times
                verts.pop()
                if vert not in finish_times:
                    finish_time += 1
                    finish_times[vert] = finish_time


    def compute_scc(self):
        '''
           This function computes the strongly connected components of this graph using Kosarju's 2-pass
           algorithm. Return the dict of each components vertices (each with an arbitrary leader as key).
        '''
        global leaders, leader, finish_times, finish_time, explored

        leaders = {}
        leader = 0
        finish_times = {}
        finish_time = 0
        explored = set()

        # DFS on reverse of graph first from all nodes until all have been explored
        for vert in self.vertices:
            if vert not in explored:
                fin = self.DFS(start=vert, forwards=False)

        # reset explored verts to all being unexplored initially
        explored = set()

        # DFS on original graph checking all verts from largest finish time to smallest
        for vert in sorted([[t,v] for v,t in finish_times.items()], reverse=True):
            if vert[1] not in explored:
                leader = vert[1]
                self.DFS(start=vert[1])  # passing through graph forwards, we will track leaders

        # the SCC's are now contained in the leaders dict
        return leaders
