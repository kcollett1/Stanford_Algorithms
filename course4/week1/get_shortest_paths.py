#!/Users/kcolletti1/opt/anaconda3/bin/python3


from graph import Graph
import sys
import time


def main():
    '''
       This driver code builds a directed weighted graph from input data and calls the
       Bellman-Ford dynamic programming algorithm to compute the shortest paths to all vertices
       on the graph from a given source vertex. The iterative approach is better in this case
       than the recursive approach as it saves on memory and run-time. With the input data given,
       g1 and g2 both contain negative cost cycles. Therefore, we don't care about them to solve
       our problem of finding the "shortest shortest" path, but g3 does not contain any negative
       cost cycles that are reachable from source vertex 1 (this does not however mean that there
       are NO negative cost cycles present in the graph). It also suceeds at finding all shortest
       paths from source vertex 1 on the large.txt graph in ~33 seconds. The Bellman-Ford running
       time is O(m*n) which is slower than Dijkstra's algorithm, but can be used for graphs with
       negative edge costs, whereas Dijkstra can only be used on non-negtative edge cost graphs only.
       Before testing with the data input sets from this week's assignment, I test to compare
       against the Dijkstra data set from Course 2 week 2, as it was solving the same problem, and
       we know the solution we are expecting to get. We indeed get the same answers with this
       algorithm! Recursive code ran in ~0.762519 seconds, while the iterative implementation ran
       in ~0.026482 seconds (and saves a lot of memory, too!)!
    '''
    if len(sys.argv) < 2:
        fname = 'g1.txt'  # default test file
    else:
        fname = sys.argv[1]

    print('\n Calculating shortest paths from vertex 1 to all other vertices in the input graph',
          '\n {0} using an iterative algorithm approach'.format(fname))

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

    # find all shortest paths from source vertex, result will be dict of dest_vert: path length
    source_vert = 1  # to test/check
    dest_verts = [7, 27, 59, 82, 99, 115, 133, 165, 188, 197]  # to test/check

    # both implementations give same result, but iterative method uses O(n) space and completes faster
    # while the recursive method uses O(n^2) space. both can recreate the actual shortest paths
    shortest_paths = test_graph.compute_shortest_paths_BF_iter(source_vert)
    #shortest_paths = test_graph.compute_shortest_paths_BF_recurs(source_vert)

    if shortest_paths == None:
        print('\n There are negative cycles present in this graph reachable from the source vertex!')
    else:
        print('\n The lengths of shortest paths from vert 1 to verts\n {0}\n are:\n'.format(dest_verts))
        print('\n {0}\n'.format(','.join([str(shortest_paths[dest]) for dest in dest_verts])))


if __name__ == "__main__":

    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
