#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   This code takes an input file specifying edges/vertices of a
   graph, and applies Kruskal's greedy algorithm to find the minimum
   spanning tree of given graph. For this algorithm, we use a disjoint
   set data structure, which has also been implemented in this folder.
   To test this, we reuse the data set from the previous week's
   assignment, as we know what result we should get from that data.
   The result we seek is simply the sum of all edges in the MST.
   This code ran in ~0.035406 seconds (compare to Prim's algo runtime of
   ~0.024284 seconds). Both returned same result!
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

    # compute the minimum spanning tree using Kruskal's algorithm
    # Return sum of all edges in the minimum spanning tree
    min_spantree_len = test_graph.compute_minspantree()

    print('\n The sum of all the lengths of the edges in the MST is',
            min_spantree_len, '\n')


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('This code ran in {0:6f} seconds.'.format(t1 - t0))

    raise SystemExit
