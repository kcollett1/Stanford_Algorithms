'''
    this is my implementation of a WEIGHTED UNDIRECTED graph as an adjacency
    list representation. vertices are added to the graph from input
    containing the vertex num and a list of vertices connected to it.
'''

from copy import deepcopy as dcopy
from stack import Stack
from queue import Queue
from heap import *


class Vert_Path:
    def __init__(self, vert=None, path_len=float('inf')):
        self.vert = vert
        self.path_len = path_len

    def set_path_len(self, new_path_len):
        self.path_len = new_path_len

    # make all ordering comparisons based on path_len
    def __lt__(self, other): return self.path_len < other.path_len
    def __le__(self, other): return self.path_len <= other.path_len
    def __gt__(self, other): return self.path_len > other.path_len
    def __ge__(self, other): return self.path_len >= other.path_len
    def __eq__(self, other): return self.path_len == other.path_len
    def __ne__(self, other): return self.path_len != other.path_len


class Graph:
    def __init__(self):
        # dict of vertices, mapped to a set of its incident edges
        self.vertices = {}  # vertex #: set(edge i, edge j, ...)
        # dict of edges, mapped to a list of the two endpoints and it's weight
        # ex: edge #: [v1,v2,w]; i.e. {3:[2,3,10]} edge3 connects vert2 and vert3 with weight 10
        self.edges = {} 
        self.num_edges = 0
        self.num_verts = 0


    def copy(self):
        new_graph = Graph()
        new_graph.vertices = dcopy(self.vertices)
        new_graph.edges = dcopy(self.edges)
        new_graph.num_edges = int(self.num_edges)
        new_graph.num_verts = int(self.num_verts)
        return new_graph


    def __update_vert__(self, vert):
        '''Helper function to add_edge to add current edge number to vertex dict'''
        if vert in self.vertices:
            self.vertices[vert].add(self.num_edges)
        else:
            self.num_verts += 1
            self.vertices[vert] = {self.num_edges}

    def add_edge(self, vert1: int, vert2: int, weight: int):
        '''Add a new edge to the graph connecting vert1 to vert2 with weight of weight'''
        # increment number of edges and add vertex pointers to this edge
        self.num_edges += 1
        self.edges[self.num_edges] = [vert1, vert2, weight]

        # add both vertices/edge# to vertex dict (and increment number of vertices if needed)
        self.__update_vert__(vert1)
        self.__update_vert__(vert2)


    def compute_shortest_paths_naive(self, source: int):
        '''
           Use Dijkstra's algorithm to compute the shortest path from source vertex to
           all other vertices in the graph. If no path exists, set shortest path = None.
           This function uses a naive/straight forward implementation to keep track of
           next edge to add, runs in O(m*n) time.
        '''
        # initialize shortest path dict of {dest vertex: path len}
        shortest_paths = {v: None for v in self.vertices}
        shortest_paths[source] = 0  # shortest path from source to itself is always 0
        last_added = source
        explored = {source}
        # initialize possible edges to bring in on next iteration
        # will be a dict of dest_vert#: path_len, will only keep min path_len seen so far
        # connecting to dest_vert
        poss_edges = {}
        keep_checking = True

        # main loop to calculate shortest path to a new vertex each iteration
        # therefore this requires at most self.num_verts - 1 iterations because source is already explored
        # but if there are unconnected vertices, our loop will stop before that
        while keep_checking:
            # add all new possible edges to pick from based on the last added vertex (may not add any)
            curr_path_len = shortest_paths[last_added]
            for edge in self.vertices[last_added]:
                dest_vert = self.edges[edge][0] if self.edges[edge][0] != last_added else self.edges[edge][1]
                # if it's a self-looping edge or already explored, not interested
                if dest_vert == last_added or dest_vert in explored:
                    continue
                path_len = curr_path_len + self.edges[edge][2]
                # if already have an edge connecting to this vertex, only keep minimum length
                # we don't use this edge if path_len is EQUAL to one already seen
                # though it's ambiguous and doesn't matter to the algorithms results if we do
                if dest_vert in poss_edges:
                    if path_len < poss_edges[dest_vert]:
                        poss_edges[dest_vert] = path_len
                else:
                    poss_edges[dest_vert] = path_len

            # find the min path len currently in poss_edges
            # this is the bottleneck where storing these values in a min heap will improve time efficiency
            # because then we can just extract_min instead of looking through all values again every time
            min_path = float('inf')
            min_vert = None
            for vert, path_len in poss_edges.items():
                if path_len < min_path:
                    min_path = path_len
                    min_vert = vert
            if not min_vert:  # this could arise if source vertex is unconnected to every other vertex
                break

            # this min_vert found will be the one added to our explored vertices, add to shortest_paths
            # remove from poss_edges, update last_added, explored, and the looping condition
            # after last iteration of this loop, poss_edges will be empty
            # and explored should contain all connected vertices from source
            shortest_paths[min_vert] = min_path
            poss_edges.pop(min_vert)
            last_added = min_vert
            explored.add(min_vert)
            keep_checking = len(poss_edges) > 0

        return shortest_paths


    def compute_shortest_paths_heap(self, source: int):
        '''
           Use Dijkstra's algorithm to compute the shortest path from source vertex to all
           other vertices in the graph. If no path exists, set shortest path = None.
           This function uses a min-heap data structure to keep track of next edge to look at,
           runs O(m*log(n)) time
        '''
        # initialize shortest path dict of {dest vertex: path len}
        shortest_paths = {v: None for v in self.vertices}

        # initialize a min heap to store all vertices and their shortest path lengths
        # add all vertices to heap as data structure Vert_Path, with +inf as initial path len
        # and set source vertex path len to be 0
        poss_edges_heap = MinHeap()
        for vert in self.vertices:
            poss_edges_heap.insert(Vert_Path(vert))
        poss_edges_heap.delete(source)
        poss_edges_heap.insert(Vert_Path(vert=source, path_len=0))

        while poss_edges_heap.size != 0:  # O(1)
            # extract min from heap - this vertex gets added to our "conquered" vertices
            # and its shortest path gets set
            next_vp = poss_edges_heap.extract_min()  # this vertex is no longer in our heap, O(log(n))
            vert = next_vp.vert
            path = next_vp.path_len
            shortest_paths[vert] = path

            # go through all edges vert points to in this graph, if connecting vert
            # is not in heap we don't care. otherwise, find it in the heap, and check
            # if we need to update the path len to a shorter one
            for edge in self.vertices[vert]:
                # extract the vertex and edge length that this edge contains
                dest_vert = self.edges[edge][0] if self.edges[edge][0] != vert else self.edges[edge][1]
                edge_len = self.edges[edge][2]

                # check if this vertex is in the heap, and if so find it's index
                heap_ind = poss_edges_heap.find(dest_vert)
                if heap_ind == None:  # this vertex has already been explored, we can skip this
                    continue

                # otherwise we need to update the path len of this vertex in the heap
                # the heap data structure will automatically compare the values and only
                # change it if it is smaller than the current path len, and sift accordingly
                poss_edges_heap.update_len(vert=dest_vert, new_len=path+edge_len)

        return shortest_paths


    def BFS(self, start: int, forwards=True):
        '''Breadth first search from start vertex. Can search reverse graph with forwards=False'''
        # initialize all vertices as unexplored except for start vertex
        explored = {v: False for v in list(self.vertices)}  # allow for vertices not labelled from 1..n
        explored[start] = True

        # initialize queue to track next vertices to explore, enqueue start vertex
        verts = Queue()
        verts.enqueue(start)

        # while queue is not empty, keep exploring vertices
        while not verts.is_empty():
            # dequeue next vertex and try to explore any incident edges it has
            vert = verts.dequeue()

            # go through all incident edges of this vertex
            for edge in self.vertices[vert]:
                # get vertex corresponding to this edge
                # if going through G, current vert will be 1st, so next_vert is in pos 1 (True)
                # if going through G_rev, current vert will be 2nd, so next_vert is in pos 0 (False)
                next_vert = self.edges[edge][forwards]

                # only interested in unexplored vertices and edges pointing AWAY from this vertex
                if next_vert == vert or explored[next_vert]:
                    continue

                # this is a vertex of interest, mark as explored and add to queue
                explored[next_vert] = True
                verts.enqeue(next_vert)


    def DFS(self, start: int, forwards=True):
        '''Depth first search (DFS) from start vertex. Can search reverse graph with forwards=False'''
        # initialize all vertices as unexplored except for start vertex
        explored = {v: False for v in list(self.vertices)}  # allow for vertices not labelled from 1..n
        explored[start] = True

        # initialize stack to track next vertices to explore, push start vertex onto stack
        verts = Stack()
        verts.push(start)

        # while stack is not empty, keep exploring vertices
        while not verts.is_empty():
            # pop next vertex off
            vert = verts.pop()

            # go through all incident edges of this vertex
            for edge in self.vertices[vert]:
                # get vertex corresponding to this edge
                # if going through G, current vert will be 1st, so next_vert is in pos 1 (True)
                # if going through G_rev, current vert will be 2nd, so next_vert is in pos 0 (False)
                next_vert = self.edges[edge][forwards]

                # only interested in unexplored vertices and edges pointing AWAY from this vertex
                if next_vert == vert or explored[next_vert]:
                    continue

                # this is a vertex of interest, mark as explored and push to stack
                explored[next_vert] = True
                verts.push(next_vert)


    def __DFS_finishtime__(self, start: int, forwards=True):
        '''depth first search from start vertex, tracking finishing times, helper for compute_scc'''
        global label, label_ctr, explored

        explored[start] = True
        verts = Stack()
        verts.push(start)

        while not verts.is_empty():
            vert = verts.top()  # which vertex is currently first in the stack
            for edge in self.vertices[vert]:
                next_vert = self.edges[edge][forwards]

                # if edge points IN towards current vertex or we've seen it already, not interested
                if next_vert == vert or explored[next_vert]:
                    continue

                # it is a vertex we're interested in, so mark as explored and add to stack
                explored[next_vert] = True
                verts.push(next_vert)

            # done looping over all possible new vertices
            if vert == verts.top():  # didn't put new vertices on stack, so we're done with top vertex
                verts.pop()
                # we've completely finished exploring this node, mark it's finishing time
                label_ctr += 1
                label[label_ctr] = vert


    def __DFS_leaders__(self, start: int, forwards=True):
        '''depth first search from start vertex, tracking leader vertex, helper for compute_scc'''
        global leader_trckr, leaders, explored

        explored[start] = True
        verts = Stack()
        verts.push(start)

        while not verts.is_empty():
            vert = verts.top()  # which vertex is currently first in the stack
            for edge in self.vertices[vert]:
                next_vert = self.edges[edge][forwards]

                # if edge points IN towards current vertex or we've seen it already, not interested
                if next_vert == vert or explored[next_vert]:
                    continue

                # it is a vertex we're interested in: mark explored, track it's leader, add to stack
                explored[next_vert] = True
                leaders[leader_trckr].add(next_vert)
                verts.push(next_vert)

            # done looping over all possible new vertices
            if vert == verts.top():  # didn't put new vertices on stack, so we're done with top vertex
                verts.pop()


    def compute_scc(self):
        '''
           This function computes the strongly connected components of this graph
           using Kosarju's algorithm. Return the dict of each components vertices.
        '''
        global label, label_ctr, leaders, leader_trckr, explored

        label = {}
        label_ctr = 0
        leaders = {}
        leader_trckr = None
        explored = {v: False for v in list(self.vertices)}  # allow for vertices not labelled from 1..n

        # DFS on reverse of graph first from all nodes until all have been explored
        for vert in self.vertices:
            if not explored[vert]:
                self.__DFS_finishtime__(start=vert, forwards=False)

        # reset explored vertices to all being unexplored
        explored = {v: False for v in list(self.vertices)}

        # DFS on original (non-reversed) graph checking all vertices from largest finish time to smallest
        for finish_time in range(self.num_verts, 0, -1):
            # want the vertex corresponding to this finish time as calculated in previous step
            vert = label[finish_time]
            if not explored[vert]:
                leader_trckr = vert
                leaders[leader_trckr] = {vert}
                self.__DFS_leaders__(start=vert)

        # the SCC's are now contained in the leaders dict
        return leaders
