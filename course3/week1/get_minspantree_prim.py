#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   This code takes an input file specifying edges/vertices of a graph, and applies Prim's
   greedy algorithm to find the minimum spanning tree of given graph. The result we seek is
   simply the sum of all edges in the minimum spanning tree. This code ran in ~0.025 seconds.
'''


from graph import Graph
import time


def main():
    test_graph = Graph()

    with open('edges.txt') as graph_info:
        _ = next(graph_info)  # don't need the first line of data file
        for graph_line in graph_info:
            data = [int(n) for n in graph_line.strip().split(' ')]
            test_graph.add_edge(*data)

    # compute MST using Prim's algorithm, return sum of all edges in it
    min_spantree_len = test_graph.compute_minspantree()

    print('\n The sum of all the lengths of the edges in the MST is {0}.'.format(min_spantree_len))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:6f} seconds.'.format(t1 - t0))

    raise SystemExit
