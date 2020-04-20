#!/Users/kcolletti1/opt/anaconda3/bin/python3


'''
   In this driver code, we take as input a graph with vertices specified by x- and y-coordinates,
   with a total of 33,708 vertices. This is a complete graph, so each vertex is connected to
   each otehr vertex, with an edge weight determined by the euclidean distance between them.
   On this graph, we apply the nearest neighbor heuristic algorithm to get a solution to the
   traveling salesman problem, which would be pretty much impossible to solve with our previous
   algorithm, as the run-time for that was non-trivial for only 25 vertices! However, this code
   ran in ~385.285728 seconds!
'''


from graph import Graph
import sys
import time


def main():
    if len(sys.argv) < 2:
        fname = 'nn.txt'  # default test file
    else:
        fname = sys.argv[1]

    print('\n Solving the traveling salesman problem using the nearest neighbor heuristic',
          '\n for the input graph', fname)

    t0 = time.time()
    test_graph = Graph()

    with open(fname) as graph_info:
        num_verts = int(next(graph_info).strip())

        # set num_verts on the graph
        test_graph.set_num_verts(num_verts)

        # go through rest of data to add all vertex coordinate info to graph
        for i,vert_info in enumerate(graph_info):
            vert_info = vert_info.strip().split(' ')
            x = float(vert_info[1])
            y = float(vert_info[2])
            test_graph.add_vertex(i, x, y)

    t1 = time.time()

    print('\n Done recording all vertices in our graph. This step took {0:.2f} seconds.'.format(t1 - t0))
    print('\n Now calculating minimum TSP tour using nearest neighbor heurisitic.')

    tsp_min_tour = test_graph.min_tour_TSP_nn_heur()  # nearest-neighbor heuristic
    t2 = time.time()

    print('\n The length of the shortest path that visits every vertex in the input graph',
          '\n exactly once and arrives back at the starting point calculated with this heuristic',
          '\n algorithm is', tsp_min_tour)
    print('\n This step took {0:.2f} seconds'.format(t2 - t1))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
