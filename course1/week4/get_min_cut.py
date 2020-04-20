#!/Users/kcolletti1/opt/anaconda3/bin/python3


from graph import Graph
import numpy as np
from numpy import random as nprand
import time


def main():
    randseed = nprand.randint(1,10000)
    nprand.seed(randseed)

    test_graph = Graph()
    with open('kargerMinCut.txt') as graph_info:
        for graph_line in graph_info:
            graph_line = [int(v) for v in graph_line.strip().split('\t')]
            test_graph.add_vertex(graph_line[0], graph_line[1:])

    sample_size_ideal = int(test_graph.num_verts**2 * np.log2(test_graph.num_verts))
    sample_size = 2200

    t0 = time.time()
    min_cut = test_graph.find_min_cut(sample_size)  # find the min cut
    total = time.time() - t0

    time_ideal = (total/sample_size) * sample_size_ideal
    acceptable_time = 1 * 60  # 1 minute
    acceptable_sample = int(acceptable_time / (total/sample_size))

    print('\n The running time using the ideal sample size would be ~',
          round(time_ideal, 2), 'seconds (', round(time_ideal / 3600, 2), 'hours )')
    print('\n For this program to run for ~60 seconds, use a sample size of ~',
          acceptable_sample)

    print('\n The min cut found by this algorithm is:', min_cut,
          'from a sample size of', sample_size)
    #print('\nvertices in min cut groups:\n', cut_a, '\nand\n', cut_b, '\n')  # not yet implemented


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.5f} seconds.'.format(t1 - t0))

    raise SystemExit
