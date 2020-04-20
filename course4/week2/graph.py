
''' this is my implementation of a WEIGHTED UNDIRECTED complete graph as an adjacency list. '''


from itertools import combinations as comb


class Graph:
    def __init__(self):
        # set of vertices
        self.vertices = set()
        # dict of edges, mapped to its weight
        self.edges = {} 
        self.num_edges = 0
        self.num_verts = 0


    def __update_vert__(self, vert):
        ''' Helper function to add_edge to add current edge number to vertex dict. '''
        if vert not in self.vertices:
            self.num_verts += 1
            self.vertices.add(vert)


    def add_edge(self, vert1: int, vert2: int, weight: int):
        ''' Add a new edge to the graph connecting vert1 and vert2 with weight. '''
        # increment number of edges and add vertex pointers to this edge
        self.num_edges += 1
        key = '{0}v{1}'.format(vert1, vert2)  # key is in arbitrary order
        self.edges[key] = weight

        # add both vertices to vertex list/increment number of vertices if needed
        self.__update_vert__(vert1)
        self.__update_vert__(vert2)


    def min_tour_TSP_iter(self):
        '''
           Compute the minimum tour (rounded down to the nearest integer). Assumes vertices are
           labelled from 1...n
        '''
        # initialize sub-solutions dict to store answers to sub-problems as we build up to final answer
        # at each iteration of m, we only need sub-problem answers from the previous value of m, so we save
        # memory by only storing sub-problems of interest and resetting after each iteration. for the key, we
        # need to index both by subset and destination vertex, and we use bit-masking to help us turn these
        # combinations into integers. for vertex size of 25, we need 29 bits for each key: the first 5 bits
        # represent the destination vertex in binary (padded at the beginning with 0's if needed), and the last
        # 24 bits represent each vertex (excluding the first since it is always in every subset by definition of
        # the algorithm), where bit i is 1 if that vertex is included in the subset, else it's 0.
        sub_solns = {}

        # use vertex array to generate subsets via itertools combinations (only choosing verts from 2-num_verts)
        base_subset = ['0' for i in range(self.num_verts - 1)]  # first vertex is always in subset
        dest_bits = len(bin(self.num_verts)[2:])
        # we're using 1-based vertex binary representation
        dest_bin = [bin(j)[2:].zfill(dest_bits) for j in range(self.num_verts + 1)]
        v = [i for i in range(2, self.num_verts + 1)]
        if v == []:  # there's only one (or zero) vertex on this graph, this is trivial
            return 0

        # base cases
        # for m = 1, only subset = {1} is a valid choice with destination vert = 1, all else are inf
        subset = int(dest_bin[1] + ''.join(base_subset), 2)
        sub_solns[subset] = 0  # destination vertex is 1 (shifted to be 0-based)
        # for m = 2
        for j in range(2, self.num_verts + 1):
            # subset with vertex 1 and vertex j, and destination vertex = j. path is simply edge cost from 1 to j
            subset = list(base_subset)
            subset[j - 2] = '1'
            subset = int(dest_bin[j] + ''.join(subset), 2)
            edgekey = '{0}v{1}'.format(1, j)
            if edgekey not in self.edges:
                edgekey = '{0}v{1}'.format(j, 1)
            sub_solns[subset] = self.edges[edgekey]

        # now build up iteratively sub-problems until we get to final answer
        for m in range(3, self.num_verts + 1):  # iterate over sub-problem size, from 3 up to n
            #print('subset size {0} out of {1}'.format(m, self.num_verts))
            prev_solns = dict(sub_solns)
            sub_solns = {}
            for s in comb(v, m - 1):  # iterate over each sub-problem of size m, including 1
                subset_list = list(base_subset)
                for vert in s: # turn on all verts in subset s (shifted by 2 to be 0-based)
                    subset_list[vert - 2] = '1'
                subset_str = ''.join(subset_list)

                for j in s:  # every possible destination using this subset
                    # calculate and set sub_solns[subset] from in this loop
                    subset = int(dest_bin[j] + subset_str, 2)
                    min_path = float('inf')
                    subset_wo_j_list = list(subset_list)
                    subset_wo_j_list[j - 2] = '0'  # turn "off" vertex j, keeping rest of subset the same
                    subset_wo_j_str = ''.join(subset_wo_j_list)

                    # check each subproblem using k in this subset (with k not equal to j) as the
                    # previous hop before reaching j
                    for k in s:
                        if k == j:
                            continue
                        subset_wo_j = int(dest_bin[k] + subset_wo_j_str, 2)

                        if subset_wo_j not in prev_solns:  # path len of this sub-prob doesn't exist
                            continue

                        edgekey = '{0}v{1}'.format(j, k)
                        if edgekey not in self.edges:
                            edgekey = '{0}v{1}'.format(k, j)
                        poss_path = self.edges[edgekey] + prev_solns[subset_wo_j]
                        if poss_path < min_path:
                            min_path = poss_path

                    if min_path != float('inf'):
                        sub_solns[subset] = min_path

        every_vert = '1' * (self.num_verts - 1)
        min_path = float('inf')
        for j in range(2, self.num_verts + 1):
            subset = int(dest_bin[j] + every_vert, 2)
            edgekey = '{0}v{1}'.format(1, j)
            if edgekey not in self.edges:
                edgekey = '{0}v{1}'.format(j, 1)
            poss_path = sub_solns[subset] + self.edges[edgekey]
            if poss_path < min_path:
                min_path = poss_path

        return int(min_path // 1)


    def min_tour_TSP_recurs(self):
        '''
           Compute the minimum tour (rounded down to the nearest integer). Assumes vertices are
           labelled from 1...n. This method uses a recursive approach to solving this problem and
           memoization rather than building the sub-problems up iteratively. We will compare run-times
           among the two methods.
        '''
        # initialize sub-solutions dict to store answers to sub-problems as we recursively compute them.
        # for key, we index by subset and destination vertex, and we use bit-masking to help us turn these
        # combinations into reasonably sized integers. for vert size 25, we need 29 bits for each key: the
        # first 5 bits represent dest vert in binary (padded at the beginning with 0's if needed), and the last
        # 24 bits represent each vert (excluding first since it is in every subset by definition of the algo),
        # where bit i is 1 if that vertex is included in the subset, else it's 0.
        min_path = float('inf')  # initialize final answer
        sub_solns = {}  # dict to contain sub-problem solutions
        one_subset = ['0', '1'] + ['0' for i in range(self.num_verts - 1)]  # only 1 is in subset
        final_subset = ['0'] + ['1' for _ in range(self.num_verts)]  # we visit every vertex exactly once
        dest_bin = [bin(j)[2:].zfill(len(bin(self.num_verts)[2:])) for j in range(self.num_verts + 1)]

        def min_tsp_path(subset_list, dest):  # define recursive function here
            # base cases, dest=1. if subset is {1} answer is 0, else answer is inf
            if dest == 1:
                if subset_list != one_subset:  # dest = 1 but subset is not {1}
                    return float('inf')
                else:  # dest is 1 and only vert in subset is 1, we don't traverse any edges, cost 0
                    return 0

            subset = int(dest_bin[dest] + ''.join(subset_list[2:]), 2)
            if subset in sub_solns:  # already calculated sub-problem answer, just return it
                return sub_solns[subset]

            # loop over all verts in subset as "prev hop" vertex, recursively calc sub-problem answer, adding
            # traversal from prev hop vertex to dest vertex; minimum of these answers is the final answer.
            subset_wo_dest = list(subset_list)  # copy subset list, remove dest from subset for future calls
            subset_wo_dest[dest] = '0'

            sub_min_path = float('inf')
            for k,switch in enumerate(subset_list):  # now all other possible prev hop vertices
                if switch == '0' or k == dest:
                    continue

                edgekey = '{0}v{1}'.format(dest, k)
                if edgekey not in self.edges:
                    edgekey = '{0}v{1}'.format(k, dest)

                poss_path = self.edges[edgekey] + min_tsp_path(subset_wo_dest, k)

                if poss_path < sub_min_path:
                    sub_min_path = poss_path

            sub_solns[subset] = sub_min_path  # may be inf
            return sub_min_path


        for j in range(2, self.num_verts + 1):
            print('checking vertex {0} out of {1}.'.format(j, self.num_verts))

            edgekey = '{0}v{1}'.format(1, j)
            if edgekey not in self.edges:
                edgekey = '{0}v{1}'.format(j, 1)

            poss_path = min_tsp_path(final_subset, j) + self.edges[edgekey]

            if poss_path < min_path:
                min_path = poss_path

        return min_path if min_path == float('inf') else int(min_path // 1)  # round down to nearest int
