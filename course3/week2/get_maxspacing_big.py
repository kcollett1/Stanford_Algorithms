#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   This code takes an input file specifying 200,000 nodes making up a completely connected
   graph (i.e. each node is connected to every other node). The goal of this algorithm is
   to compute the maximum number of clusters we would need to split the data into clusters
   that have a maximum spacing of at least 3. The input of these points are given in 24 bits
   per node. Each node is represented by a string of 24 bits, and the distance between each
   node is the Hamming distance (the number of differing bits). Looking through/keeping track
   of/sorting all of the edges in this graph/universe of points, even linearly, would require a
   lot of time/processing power. Therefore, we take a different approach to solve this problem.
   We initialize a disjoint set for all of our nodes, where all nodes are unconnected in their
   own clusters. For this program, we label each node in the disjoint set by its line in the
   input file. We only care about finding pairs that are of distance 1 or 2 away from each other,
   so we can merge them all if needed. If we are able to do this, we would be left with at least
   a spacing of 3 between each cluster (in theory we could group all distance 3 node pairs in the
   same clusters, making the *actual* spacing more than 3, but we just care about the lower bound
   for this problem, so spacing=4 would satisfy our condition anyway). So instead of looking
   through each node pair, we look through each node, and then all of the possible nodes that are
   of distance 1 and 2 away by changing 1 and 2 bits respectively. We use a hash structure to
   store nodes in our universe, making lookup of these possible nodes O(1)! For any nodes that
   ARE in our universe, we merge the two nodes together. Additionally, we keep track of seen pairs
   so that we don't try to double merge any nodes/do any extra work that we don't need to. For any
   nodes we try to merge that are already in the same cluster, nothing happens. At the end of
   merging all pairs that are of distance 1 or 2 away, our disjoint set contains the clusters we
   sought. And the answer to this problem is simply the number of groups contained in the disjoint
   set! This code ran in ~66.91 seconds.
'''


from disjoint_set import DisjointSet
import time


def main():

    with open('clustering_big.txt') as node_info:
        head = next(node_info).strip().split(' ')
        num_nodes = int(head[0])
        num_bits = int(head[1])
        clusters = DisjointSet(num_nodes)
        nodes = {}  # use hash table/dict to store the nodes!
        for node_num,line in enumerate(node_info, start=1):
            node_int = int(''.join(line.strip().split(' ')), 2)
            if node_int not in nodes:
                nodes[node_int] = []  # will be very few duplicates, so using list to store them won't cost us
            nodes[node_int].append(node_num)

    # go through all nodes to merge all distance 1 and 2 pairs
    for n in nodes:
        curr_nodes = nodes[n]  # just for ease of reading/typing when repeatedly using this value

        # merge all distance 0 pairs first!!
        for i in range(len(curr_nodes) - 1):
            for j in range(i + 1, len(curr_nodes)):
                clusters.union(curr_nodes[i], curr_nodes[j])

        # change one and two bits at a time and check if it is a node in our graph
        # double loop to check all possibilities (which is much less computationally
        # intensive than checking all possible pairs within our completely connected
        # graph of 200,000 nodes!)
        for i in range(num_bits):
            # first change one bit and check if we need to merge nodes
            one_bit_diff = n ^ (1 << i)
            if one_bit_diff in nodes:  # this node exists in our graph/universe!
                diff_nodes = nodes[one_bit_diff]
                # we need to merge ALL nodes corresponding to int n
                # with ALL nodes corresponding to int one_bit_diff
                for c in curr_nodes:
                    for d in diff_nodes:
                        # merge these 2 nodes in disjoint set
                        clusters.union(c, d)

            # now with this one bit changed, change all other bits one at a time to generate
            # all distance 2 possible nodes (for i=num_bits-1 this loop won't execute)
            for j in range(i + 1, num_bits):
                two_bits_diff = one_bit_diff ^ (1 << j)
                if two_bits_diff in nodes:  # this node exists in our graph/universe!
                    diff_nodes = nodes[two_bits_diff]
                    # we again need to merge ALL nodes corresponding to int n
                    # with ALL nodes corresponding to int two_bits_diff
                    for c in curr_nodes:
                        for d in diff_nodes:
                            # merge these 2 nodes in disjoint set
                            clusters.union(c, d)

    # after merging all pairs that were distance 1 and 2 apart
    # we are left with clusters that are all AT LEAST distance 3 apart (the actual
    # spacing distance COULD possibly be greater than 3 if no distance 3 pairs exist
    # in different clusters). so the answer to our question of what is the largest k
    # value (num of clusters) needed such that there is spacing at least 3 between
    # all clusters, is simply the number of disjoint groups contained in our disjoint set!
    max_k = clusters.num_groups

    print('\n The maximum number of clusters needed to ensure a maximum spacing of',
          '\n at least 3 for the given data is', max_k, '\n')


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('This code ran in {0:.2f} seconds.\n'.format(t1 - t0))

    raise SystemExit
