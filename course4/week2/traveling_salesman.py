#!/Users/kcolletti1/opt/anaconda3/bin/python3


'''
   This code ran in ~3762.0 seconds (~1 hour) using the iterative approach and a hash dict
   using bit-masking for the keys and erasing all outdated sub-problems from memory once they
   are not needed anymore. The answer it reported was 26442. This code ran in ~5869.0 seconds
   (~1.5 hours) using the recursive approach. It reported the same answer.
'''


from graph import Graph
import sys
import math
import time


def main():
    if len(sys.argv) < 2:
        fname = 'tsp.txt'  # default input data file
    else:
        fname = sys.argv[1]

    print('Solving the traveling salesman problem for input graph {0}'.format(fname))

    with open(fname) as graph_info:
        num_verts = int(next(graph_info).strip())
        coords = [None for _ in range(num_verts)]
        for i,coord in enumerate(graph_info):
            coords[i] = [float(c) for c in coord.strip().split(' ')]

    test_graph = Graph()
    for i in range(num_verts - 1):
        for j in range(i + 1, num_verts):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dist = math.sqrt(dx**2 + dy**2)
            test_graph.add_edge(i + 1, j + 1, dist)  # 1-based indexing of vertices in this graph

    tsp_min_tour = test_graph.min_tour_TSP_iter()
    #tsp_min_tour = test_graph.min_tour_TSP_recurs()  # this approach took longer to complete

    print('\n The length of the shortest path that visits every vertex in the input graph',
          '\n exactly once and arrives back at the starting point is {0}'.format(tsp_min_tour))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
