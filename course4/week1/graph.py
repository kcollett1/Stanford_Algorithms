
''' this is my implementation of a WEIGHTED DIRECTED graph as an adjacency list. '''


from heap import *


class Vert_Path:
    '''
       This class is used to instantiate objects to insert to a Min Heap, representing verts
       while also tracking their current shortest path calculated, and comparing values
       based on current shortest path length instead of vert number.
    '''
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
        # dict of vertices, mapped to a list of sets of edges pointing OUT of/IN to vert
        # ex: vert#:[set(edge i,...), set(edge j,...)]; edge i points AWAY/j points TO vert
        # dict of edges, mapped to a list of its head and tail and it's cost. ex: edge #: [v1,v2,w]
        self.vertices = {}
        self.edges = {} 
        self.num_edges = 0
        self.num_verts = 0


    def __update_vert__(self, vert, ind):
        ''' Helper function to add_edge to add current edge number to vertex dict '''
        if vert not in self.vertices:
            self.num_verts += 1
            self.vertices[vert] = [set(), set()]
        self.vertices[vert][ind].add(self.num_edges)


    def add_edge(self, source: int, dest: int, cost: int):
        '''Add a new edge to the graph pointing from vert1 to vert2 weighing cost '''
        # increment number of edges and add vertex pointers to this edge
        self.num_edges += 1
        self.edges[self.num_edges] = [source, dest, cost]

        # add both vertices/edge# to vertex dict (and increment number of vertices if needed)
        self.__update_vert__(source, 0)
        self.__update_vert__(dest, 1)


    def delete_vertex(self, vert: int):
        removed_vert = self.vertices.pop(vert)  # try to remove vertex from dict

        if removed_vert == None:  # vert is not in graph, nothing to delete
            return None

        # decrement number of vertices
        self.num_verts -= 1

        # finally we need to remove all edges that were connected to this vertex
        outgoing, incoming = removed_vert
        for edge in outgoing:  # remove edges pointing away from deleted vertex
            removed_edge = self.edges.pop(edge)
            self.num_edges -= 1
            # need to remove this edge from the vertex it points INTO
            in_vert = removed_edge[1]
            self.vertices[in_vert][1].remove(edge)

        for edge in incoming:  # for deleting our dummy vertex, this should be empty
            rmeoved_edge = self.edges.pop(edge)
            self.num_edges -= 1
            # need to remove this edge from the vertex it points OUT OF
            from_vert = removed_edge[0]
            self.vertices[from_vert][0].remove(edge)


    def compute_shortest_paths_BF_recurs(self, source: int):
        '''
           Use the Bellman-Ford dynamic programming algorithm to compute the shortest path from
           source vertex to all other vertices in the graph. If no path exists, shortest path = +inf.
           This implementation uses a recursive method to calculate all necessary sub-solutions.
           To check for negative cycles in graph, could update to calculate get_shortest_path with
           num_verts instead of num_verts - 1, and compare the results of num_verts and num_verts-1,
           if any differ, there are negative cycles present (that are reachable from source)!
        '''
        # initialize shortest hash dict, which will contain the solutions to all necessary sub-problems
        shortest = {}
        def get_shortest_path(edge_budget, vert):
            key = 'i{0}v{1}'.format(edge_budget, vert)
            if key in shortest:  # already solved this problem, just return answer
                return shortest[key]

            # base cases, edge_budget is 0
            if edge_budget == 0:
                if vert == source:
                    shortest[key] = 0
                else:
                    shortest[key] = float('inf')
                return shortest[key]

            prev_path_key = 'i{0}v{1}'.format(edge_budget - 1, vert)
            if prev_path_key in shortest:  # already solved this problem, just set var
                prev_path = shortest[prev_path_key]
            else:  # haven't solved this problem yet, recursively solve it
                prev_path = get_shortest_path(edge_budget - 1, vert)

            # now paths with edge_budget-1 for all edges pointing INTO vert, get min
            new_path_min = float('inf')
            for in_edge in self.vertices[vert][1]:
                new_path = self.edges[in_edge][2]  # the cost of traversing this edge to arrive at vert
                prev_vert = self.edges[in_edge][0]
                new_path_key = 'i{0}v{1}'.format(edge_budget - 1, prev_vert)
                if new_path_key in shortest:  # already solved, just add to new_path var
                    new_path += shortest[new_path_key]
                else:  # haven't solved yet, recursively solve it
                    new_path += get_shortest_path(edge_budget - 1, prev_vert)
                if new_path < new_path_min:
                    new_path_min = new_path

            # now set shortest[key] = min(prev_path, new_path) and return answer
            shortest[key] = min(prev_path, new_path_min)
            return min(prev_path, new_path_min)

        # initialize shortest path dict of {dest vertex: path len} which will be the final answer
        shortest_paths = {}
        for v in self.vertices:  # get shortest path from source to all vertices
            shortest_paths[v] = get_shortest_path(self.num_verts - 1, v)

        # checking how much space is used remembering all sub-solutions
        #print('num of sub-solutions saved in memory:', len(shortest))
        #print('n =', self.num_verts, 'n^2 = ', self.num_verts**2)
        # we actually use O(n^2) space when using the recursive version of this algorithm!
        # we can actually do much better iteratively in this case, using only O(n) space
        # while also saving the actual paths

        return shortest_paths


    def compute_shortest_paths_BF_iter(self, source: int):
        '''
           Use the Bellman-Ford dynamic programming algorithm to compute the shortest path from
           source vertex to all other vertices in the graph. If no path exists, shortest path = +inf.
           In this implementation, we use the iterative method, as we can save a lot of space using
           this method, as all sub-solns will in fact be necessary, so using iteration doesn't cause
           any unneccesary sub-soln computation, and when we build solns up rather than top-down,
           we can throw out old results that we will no longer use in the future. We also save shortest
           paths with an additional O(n) space requirement, saving the predecessor verts, leading to
           ~3*n O(n) space, whereas with recursion we use ~n^2 space (O(n^2)).
        '''
        # initialize shortest path dict (final answer) and shortest_prev of {dest vertex: path len}
        # also maintain predecessor verts to recreate actual shortest paths rather than just lengths
        shortest_prev = {v: float('inf') for v in self.vertices}
        shortest_paths = {v: float('inf') for v in self.vertices}
        pred_verts = {v: None for v in self.vertices}
        shortest_prev[source] = 0
        shortest_paths[source] = 0
        updates = True

        for _ in range(self.num_verts - 1):  # loop over edge budget, allowing more and more edges
            if updates == False:  # no verts had paths changed last iteration, found all shortest paths!
                break

            updates = False
            for v in self.vertices:
                # calc paths with additional edge in budget for all edges going INTO vert, get min
                new_path_min = float('inf')
                new_path_vert = None
                for in_edge in self.vertices[v][1]:
                    prev_vert = self.edges[in_edge][0]
                    new_path = self.edges[in_edge][2] + shortest_prev[prev_vert]
                    if new_path < new_path_min:
                        new_path_min = new_path
                        new_path_vert = prev_vert

                # only need to update if we found a different shorter path
                if new_path_min < shortest_prev[v]:
                    shortest_paths[v] = new_path_min
                    pred_verts[v] = new_path_vert
                    updates = True

                shortest_prev = dict(shortest_paths)  # update prev paths for next iteration

            # before we go on to next iteration adding an edge to edge length budget
            # we'll check the predecessor pointers for any cycles
            for v_check in self.vertices:
                checked = {v_num: False for v_num in self.vertices}
                vert = v_check
                while vert != None and checked[vert] == False:
                    checked[vert] = True
                    vert = pred_verts[vert]
                if vert != None:  # we've found a negative cost cycle, uh oh
                    return None

        return shortest_paths


    def compute_shortest_paths_Dijkstra(self, source: int, edge_lens: dict):
        '''
           This method uses Dijkstra's algorithm to compute the shortest path from source vertex
           to all other vertices in the graph. If no path exists, set shortest path = None.
           This function uses a min-heap data structure to keep track of next edge to look at,
           runs O(m*log(n)) time, and is slightly modified to use edge lengths passed into the
           method rather than the edge lengths defined in the actual graph variables (for application
           to Johnson's all pair shortest paths algo (see below)).
        '''
        # initialize shortest path dict of {dest vertex: path len}
        shortest_paths = {'s{0}d{1}'.format(source, v): None for v in self.vertices}

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
            shortest_paths['s{0}d{1}'.format(source, vert)] = path

            # go through all edges vert points to in this graph, if connecting vert
            # is not in heap we don't care. otherwise, find it in the heap, and check
            # if we need to update the path len to a shorter one
            for edge in self.vertices[vert][0]:
                # extract the vertex and edge length that this edge contains
                dest_vert = self.edges[edge][1]

                # check if this vertex is in the heap, and if so find it's index
                heap_ind = poss_edges_heap.find(dest_vert)
                if heap_ind == None:  # this vertex has already been explored, we can skip this
                    continue

                # otherwise we need to update the path len of this vertex in the heap
                # the heap data structure will automatically compare the values and only
                # change it if it is smaller than the current path len, and sift accordingly
                poss_edges_heap.update_len(vert=dest_vert, new_len=path+edge_lens[edge])

        return shortest_paths


    def compute_APSP_FW(self):
        '''
           This method implements the Floyd-Warshall algo to compute all pairs shortest paths
           on this graph. The vertices are labelled from 1...n (if not already labelled this
           way, uncomment the vert_map lines of code below), and we iterate over the vertices in
           increasing order, each time allowing only vertices up to (and including) the current
           vertex to be used in internal paths from one vertex to another. Either this vertex
           will not change the current shortest path found between two vertices, and the path
           length will simply be the one calculated in the previous iteration, or the addition
           of this vertex will allow for a shorter path, in which case the path length can be
           calculated as the path length from the source vertex to the current vertex in the
           iteration, plus, the path length from the current vertex in the iteration to the
           destination vertex - both of which are quantities calculated in the previous iteration
           as well (this is because the path from source to current vertex and the path from
           current vertex to destination can not contain any vertices that are higher than the
           current vertex, and we are assuming there are no negative cycles so the current vertex
           can only be present in the path once). So within each iteration over the allowed internal
           vertices, we iterate over ALL PAIRS of vertices. If at any point we find there is a
           shorter path to go from one vertex to itself, we know there is a negative cycle somewhere
           in the graph, so we halt and report this finding. To reconstruct the actual paths, we
           also track the maximum internal vertex used in a path from one vertex to another, and
           with this information we can recursively reconstruct sub-paths until we reach 0 as the
           maximum internal vertex, meaning there are no internal vertices and the source and dest
           vertices are directly connected by their edge. Because of three nested loops over all
           vertices, this is an O(n^3) run-time algorithm. We only keep track of the previous
           iterations answers, the current iterations answers, and the max internal node for each
           pair, so this only uses O(n^2) memory.
        '''
        # if vertices not already labelled from 1..n, use this vertex mapping (and in loops also)
        #vert_map = {i: v for i,v in enumerate(self.vertices, start=1)}

        # initialize shortest path dict (will be final answer) and shortest_prev {source_dest: pahtlen}
        shortest_paths = {}
        max_internal = {}
        for v in range(1, self.num_verts + 1):
            for w in range(1, self.num_verts + 1):
                #v = vert_map[v]
                #w = vert_map[w]
                key = 's{0}d{1}'.format(v,w)
                if v == w:
                    shortest_paths[key] = 0
                    max_internal[key] = None
                else:
                    # intersection of sets of edges outgoing from v and incoming to w, if an edge
                    # connects these verts, the set will contain edge num, else it will be empty
                    common_edge = self.vertices[v][0] & self.vertices[w][1]
                    if len(common_edge) == 0:
                        shortest_paths[key] = float('inf')
                        max_internal[key] = None
                    else:
                        shortest_paths[key] = self.edges[common_edge.pop()][2]
                        max_internal[key] = 0

        for k in range(1, self.num_verts + 1):
            shortest_prev = dict(shortest_paths)
            for v in range(1, self.num_verts + 1):
                for w in range(1, self.num_verts + 1):
                    #v = vert_map[v]
                    #w = vert_map[w]
                    #k = vert_map[k]
                    key = 's{0}d{1}'.format(v, w)
                    key1 = 's{0}d{1}'.format(v, k)
                    key2 = 's{0}d{1}'.format(k, w)

                    diff_path = shortest_prev[key1] + shortest_prev[key2]

                    if diff_path < shortest_prev[key]:
                        if v == w:  # there is a negative cycle in this graph!!
                            return (None, None)
                        shortest_paths[key] = diff_path
                        max_internal[key] = k

        return (max_internal, shortest_paths)


    def compute_APSP_Johnson(self):
        '''
           This method implements Johnson's algorithm to solve the all pairs shortest paths problem.
           This algorithm first adds a "dummy invisible" vertex to the graph (we have less strictness
           with the labelling of the vertices in this algo compared with the F-W algo, but we do
           need no vertex to be labelled by '0' as this will be the dummy vertex's label) that points
           to every other vertex with an edge cost of 0 (This does not introduce any new paths among
           vertices in the original graph as no vertices have an edge pointing INTO the dummy vertex).
           We then run the Bellman-Ford algorithm to find all shortest paths from the dummy vertex to
           all other vertices in the graph. These shortest paths will become the reweighting factors
           for each vertex. We can now delete the dummy vertex from the graph (this is not strictly
           necessary as the outcome of the algo will be the same regardless, but to maintain the
           original graph we undo the dummy vertex we added). With the reweighting factors we found,
           we calculate new edge costs for each edge, adding the reweighting factor from the source
           vertex and subtracting the factor from the destination vertex. This ensures all edge costs
           will now be non-negative, and all path lengths from a given source to destination remain
           comparatively the same (i.e. all are only *shifted* by some constant number). Now all edge
           costs are non-negative, we can just run the fast Dijkstra algo using each vertex as the
           source vertex, thereby calculating the shortest path from each source vertex to each
           possible destination vertex. This step is the main run-time bottleneck, but is still only
           O(n*m*log(n)), as we call n instances of the O(m*log(n)) dijkstra's algo. After this step,
           we are basically done, but we just need to reconstruct the *actual* shortest path lengths,
           which just amounts to an addition and subtraction using the reweighting factors we computed
           earlier for each source-dest pair.
        '''
        # verts labelled from 1 to n, so create dummy vert labelled 0 pointing to all other verts
        # with edge cost 0. NOTE: if a vert is labelled 0, it needs to be changed first! O(n)
        n = self.num_verts
        for v in range(1, n + 1):
            self.add_edge(0, v, 0)

        # run bellman-ford with source vertex 0 (the dummy vert we created) to get the
        # reweighting factors to use with dijkstra's algo later. O(nm)
        reweights = self.compute_shortest_paths_BF_iter(0)
        if reweights == None:  # there is a negative cost cycle present in the graph somewhere
            return None

        self.delete_vertex(0)  # now we can remove the dummy vertex we added to the graph. O(n)
        shortest_paths = {}  # initialize shortest paths dict to contain final answers

        # calculate/set the reweighted edge costs to use with dijkstra's algo. O(m)
        new_edge_costs = {}
        for edge in self.edges:
            v,w,c = self.edges[edge]
            new_edge_costs[edge] = c + reweights[v] - reweights[w]

        # run dijsktra's algo using every vertex as source. O(nmlog(n)) - this is domainating runtime
        for source in range(1, self.num_verts + 1):
            shortest_paths.update(self.compute_shortest_paths_Dijkstra(source, new_edge_costs))

        # finally, re-adjust the shortest path lens to actual path length values. O(n^2)
        for v in range(1, self.num_verts + 1):
            for w in range(1, self.num_verts + 1):
                key = 's{0}d{1}'.format(v, w)
                shortest_paths[key] = shortest_paths[key] - reweights[v] + reweights[w]

        return shortest_paths

