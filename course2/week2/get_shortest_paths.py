#!/Users/kcolletti1/opt/anaconda3/bin/python3


from graph import Graph
import time


def main():
    test_graph = Graph()
    with open('dijkstraData.txt') as graph_info:
        for graph_line in graph_info:
            data = [v for v in graph_line.strip().split('\t')]
            source_vert = int(data[0])
            for dest in data[1:]:
                (dest_vert, weight) = (int(i) for i in dest.split(','))
                # to avoid double counting, only add edge when dest is larger than/equal to source
                if dest_vert >= source_vert:
                    test_graph.add_edge(source_vert, dest_vert, weight)

    # find all shortest paths from source vertex, result will be dict of dest_vert: path length
    source_vert = 1
    dest_verts = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    #shortest_paths = test_graph.compute_shortest_paths_naive(source_vert)  # both algos give same result!
    shortest_paths = test_graph.compute_shortest_paths_heap(source_vert)

    print('\n The lengths of the shortest paths from vertex 1 to the vertices\n',
          dest_verts, '\n are:\n')
    print(' ', ','.join([str(shortest_paths[dest] if shortest_paths[dest] else 1000000) \
                                                   for dest in dest_verts]), '\n')



if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('This code ran in {0:.5f} seconds.'.format(t1 - t0))

    raise SystemExit
