#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   run from command line with either
   $ python get_scc.py [datafile]
   $ ./get_scc.py [datafile]
   if no data file is provided, scc.txt is used by default

   This code takes as input a data file containing a directed unweighted graph. The graph is
   stored in a Graph object and the strongly connected components are calculated and saved as
   a dict containing the sets of SCC's - the key being an arbitrary "leader" of the group, and
   the item being a set of all vertices contained in that SCC. For the homework problem we were
   trying to solve, we only were interested in the *sizes* of the *five largest* SCC's.
   For scc.txt, containing 875714 vertices and 5105042 edges, this code ran in ~44.19194 seconds.
'''

from graph import Graph
import numpy as np
import sys
import time


def main():
    if len(sys.argv) < 2:
        fname = 'scc.txt'  # default test file
    else:
        fname = sys.argv[1]

    test_graph = Graph()

    with open(fname) as graph_info:
        for graph_line in graph_info:
            graph_line = [int(v) for v in graph_line.strip().split(' ')]
            test_graph.add_edge(*graph_line)

    # assume verts labelled 1..n, go through and check if each vert exists in graph, if not add to graph
    # this avoids missing any vertices that are not connected to any other parts of the graph, which
    # thus make up their own SCC of size 1
    for v in range(1, test_graph.max_vert + 1):
        if v not in test_graph.vertices:
            test_graph.add_vert(v)

    scc_groups = test_graph.compute_scc()  # find the strongly connected components
    scc_sizes = sorted([len(scc_groups[scc]) for scc in scc_groups], reverse=True)
    if len(scc_sizes) < 5:
        scc_sizes += [0 for _ in range(5 - len(scc_sizes))]

    print('\n The 5 largest sizes of strongly connected components found by this algorithm are',
          '\n', ','.join([str(i) for i in scc_sizes[:5]]))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.5f} seconds.\n'.format(t1 - t0))

    raise SystemExit
