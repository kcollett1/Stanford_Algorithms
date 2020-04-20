
'''
    this is my implementation of a WEIGHTED UNDIRECTED graph as an adjacency
    list representation, from a previous section, with some slight modifications
    made for application to kruskal's MST finding greedy algorithm, in addition
    to single-link k-clustering applications.
'''


from disjoint_set import *
from quick_sort import *


class Graph:
    def __init__(self):
        # list of vertices, with index = vert#, mapped to a set of its incident edges
        self.vertices = []
        # list of edges, with index = edge#, mapped to list of vert endpoints and edge weight
        self.edges = [] 


    def __update_vert__(self, vert):
        '''Helper function to add_edge to add current edge number to vertex dict'''
        for _ in range(len(self.vertices), vert):
            self.vertices.append(set())
        self.vertices[vert - 1].add(len(self.edges) - 1)


    def add_edge(self, vert1: int, vert2: int, weight: int):
        '''Add a new edge to the graph connecting vert1 and vert2 with weight of weight'''
        # add vertex pointers to this edge, add edge num to each verts set
        self.edges.append([vert1, vert2, weight])  # this ind is len(self.edges) - 1
        self.__update_vert__(vert1)
        self.__update_vert__(vert2)


    def compute_minspantree(self):
        '''
           Use Kruskal's algorithm to compute the MST of the graph. This function uses a
           disjoint set data structure to determine if a vertex should be added to the MST
           or not. We go through each edge once after sorting them in increasing order
           (breaking ties arbitrarily), and if it does not create a cycle in the current
           MST (i.e. the two vertices the edge connects are currently in different groups in
           the DisjointSet), it is added to the MST. Sorting during pre-processing runs in
           O(m*log(n)) time, and then the main loop checking each edge is O(m), where the
           body of the loop runs at worst case O(log(n)) (due to the DisjointSet structure
           I implemented), making it at most O(m*log(n)). Therefore, the overall algo runs in
           O(mlog(n)) time. Return simply the sum of all edge costs belonging to the MST.
        '''
        # initialize len of MST and a DisjointSet object to store all vertices and the
        # connected component they currently belong to (initially all are unconnected)
        # we're assuming here that the vertices of this graph are labelled from 1 to n
        MST_len = 0
        verts = DisjointSet(len(self.vertices))

        # first sort by increasing edge cost, breaking ties arbitrarily. then loop over sorted
        # edges. for each edge, extract vertices that edge connects and merge them in
        # DisjointSet. if already in same set, merged var will be None, and we won't add to
        # MST. else, we will add to MST
        for e in quick_sort(self.edges):  # quick_sort O(m*log(n)), main loop O(m)
            merged = verts.union(*e[:2])  # worst case O(log(n))
            if merged != None:
                MST_len += e[2]

        return MST_len

    def maxspacing_kcluster(self, k=2):
        '''
           This function computes the maximum spacing of this graph with specified number
           of clusters k used to separate/classify/cluster data points, using the distance
           as the edge cost between vertices, and utilizing a disjoint set to track clusters.
           This function simply returns the maximum spacing between the clusters once they're
           found.
        '''
        if k > len(self.vertices):  # not a valid number of desired clusters
            raise ValueError('Num clusters must be less than/equal to num of data points.')

        verts = DisjointSet(len(self.vertices))
        sorted_edges = quick_sort(self.edges)

        itr = 0
        while itr < len(sorted_edges) and verts.num_groups > k:
            verts.union(*sorted_edges[itr][:2])
            # either 2 clusters merged into 1, decreasing num_groups var in our DisjointSet
            # or were already in same cluster, nothing happened. either way, go to next edge.
            itr += 1

        if itr == len(sorted_edges):
            raise ValueError('maxspacing algo failed to find {} clusters, not enough edges!'.format(k))

        # find largest edge containing vertices that are in separate clusters
        while itr < len(sorted_edges):
            v1 = sorted_edges[itr][0]
            v2 = sorted_edges[itr][1]
            if verts.find(v1) != verts.find(v2):
                break
            itr += 1

        return sorted_edges[itr][2]
