#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   This code takes an input file specifying a completely connected undirected
   weighted graph, with 500 nodes. Our goal in this code is to find the maximal
   spacing we can achieve by separating the nodes into 4 clusters. We use the
   greedy k-clustering (single-link clustering) to solve this problem. We initialize
   our graph, and compute the max spacing on our graph with k=4 clusters. The
   algorithm first sorts all edges in non-decreasing order of weight, and then
   greedily takes the closest/smallest weight edge and merges the two nodes it
   connects, doing this repeatedly until we are left with k clusters. Sometimes
   in this process the minimal edge may already be within a cluster (due to previous
   merges), and in that case nothing happens and we do not decrease the number of
   clusters on our graph. Therefore, it is not simply a matter of merging the
   n-k smallest edges, since the number of edges can be (and is in this specific case)
   much larger than the number of nodes on the graph and we might wind up merging
   many nodes that are already in the same group. But it is just a matter of looping
   this process until the number of desired clusters is reached. The disjoint-set
   data structure is beautifully relevant for handling these needs, and makes this
   process very simple. This code ran in ~1.791575 seconds.
'''


from graph import Graph
import time


def main():
    test_graph = Graph()

    with open('clustering1.txt') as graph_info:
        _ = next(graph_info)  # don't need the first line of data file
        for graph_line in graph_info:
            data = [int(n) for n in graph_line.strip().split(' ')]
            test_graph.add_edge(*data)

    # compute the maximum spacing using the greedy algorithm from lecture for k=4 clusters
    max_spacing = test_graph.maxspacing_kcluster(4)

    print('\n The maximum spacing with 4 clusters of the given data is', max_spacing, '\n')


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('This code ran in {0:6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
