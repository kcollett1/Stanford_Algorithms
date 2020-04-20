#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   Run from command line with either
   $ ./get_allpair_shortpaths.py [data_file alg_choice]
   or
   $ python get_aallpair_shortpaths.py [data_file alg_choice]
   where alg_choice = either FW or J (for floyd-warshall or johnson respectively). if no options
   specified, default values will be used
   This driver code builds a directed weighted graph from input data and computes
   All Pairs Shortest Paths (that is, for every possible pair of points in the graph,
   it finds the length of the shortest path connecting them). We implement two algorithms
   to solve this problem, the Floyd-Warshall algorithm, and Johnson's algorithm. We again
   test them both on the dijkstra data first to ensure correctness. Both algorithms detect
   negative cycles if they are present and halt and report this to us if this is the case.
   Otherwise, they return to us a dict of all pairs of points in the graph mapped to their
   shortest path length. From the Floyd-Warshall algorithm, we can actually also reconstruct
   the paths from any source to any destination if we wish. Both algorithms output the same
   answer for our test graphs of g1.txt, g2.txt, and g3.txt (g1 and g2 contain negative cycles,
   while the shortest shortest path on g3 is -19), but their running time is significantly
   different. Floyd-Warshall completes in ~2275.9 seconds, whereas Johnson completes in
   ~71.29 seconds!
   For 'large.txt' input graph - based on the smaller graphs runtime and input size compared
   to the large graph, I expect the Johnson algorithm to finish in ~13-14 hours :O
   I am not running the algorithm to test it out though.
'''

from graph import Graph
import sys
import time


def main():
    if len(sys.argv) < 2:
        fname = 'g1.txt'  # default test file
        alg = 'J'  # default algorithm to run
    else:
        fname = sys.argv[1]
        alg = sys.argv[2]
        if alg != 'FW' and alg != 'J':
            raise ValueError('Warning: algorithm option needs to be specified as either FW or J')

    print('\n Calculating shortest paths between all pairs of nodes in the input graph',
          '\n {0} using the {1} algorithm'.format(fname, {'J':'Johnson', 'FW':'Floyd-Warshall'}[alg]))

    test_graph = Graph()
    if fname == 'dijkstraData.txt':
        with open(fname) as graph_info:
            for graph_line in graph_info:
                data = graph_line.strip().split('\t')
                source = int(data[0])
                for dest_data in data[1:]:
                    dest, cost = [int(d) for d in dest_data.split(',')]
                    test_graph.add_edge(source, dest, cost)
    else:
        with open(fname) as graph_info:  # test with g1.txt, g2.txt, g3.txt, or large.txt
            _ = next(graph_info)  # don't need the info in the first line of data file
            for graph_line in graph_info:
                source, dest, cost = [int(d) for d in graph_line.strip().split(' ')]
                test_graph.add_edge(source, dest, cost)

    # find all shortest paths from all vertices as source vertex (all pair shortest paths: APSP)
    # result will be dict of 's{0}d{1}'.format(source, dest): path length
    source_vert = 1  # to test/check
    dest_verts = [7, 27, 59, 82, 99, 115, 133, 165, 188, 197]  # to test/check
    if alg == 'FW':  # floyd-warshall algorithm
        max_internal, shortest_paths = test_graph.compute_APSP_FW()
    else:  # johnson's algorithm
        shortest_paths = test_graph.compute_APSP_Johnson()

    if shortest_paths == None:
        print('\n There are negative cycles present in this graph reachable',
              'from the source vertex!')
    else:
        print('\n The lengths of shortest paths from vert 1 to verts\n {0}\n are:'.format(dest_verts))
        print('\n {0}\n'.format(','.join([str(shortest_paths['s1d{0}'.format(dest)]) for dest in \
                                                                              dest_verts])))
        if alg == 'FW':
            def recon_path(s, d):  # can use this reconstruction algorithm on floyd-warshall results
                def recurs(i, j):
                    key = 's{0}d{1}'.format(i, j)
                    mid = max_internal[key]
                    if mid == 0:
                        return [i]
                    else:
                        return recurs(i, mid) + recurs(mid, j)
                return recurs(s, d) + [d]
            s, d = 1, 7
            print('\n The path from {0} to {1} is retraced as'.format(s, d), recon_path(s, d))

        shortest_short = float('inf')
        shortest_s = None
        shortest_d = None
        for v in test_graph.vertices:
            for w in test_graph.vertices:
                key = 's{0}d{1}'.format(v, w)
                if shortest_paths[key] < shortest_short:
                    shortest_short = shortest_paths[key]
                    shortest_s = v
                    shortest_d = w
        print('\n The shortest shortest path in this graph goes from {0} to'.format(shortest_s),
              '{0} and has length {1}'.format(shortest_d, shortest_short))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
