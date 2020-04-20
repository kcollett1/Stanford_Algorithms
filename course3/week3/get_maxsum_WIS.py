#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   We take as input data consisting of weights of vertices of a weighted path graph
   of 1000 nodes. The problem we are trying to solve is to maximize the sum of
   weighted independent subsets (WIS), where the condition that needs to be met is
   that no two adjacent nodes can belong in the subset together. We use a dynamic
   programming approach to solve this problem, memoizing previous results as we
   iterate along the path and using the previous two results to help us determine the
   current nodes result. When we reach the last node, our result will simply be the
   solution we get at that node from the previous two nodes. Note this algorithm only
   works for non-negative weights. We then also are able to back-track through our
   max_sum memoized solutions to recreate a possible subset of nodes that leads to the
   optimal solution (though with non-distinct weights, note that this solution may be
   ambiguous). If we didn't need to reconstruct the actual subset, and only cared about
   the maximal sum, we could store the previous two solutions in two variables (O(1)
   space) instead of storing all of the sub-solutions in an O(n) space matrix.
   This code ran in ~0.006658 seconds.
'''

import numpy as np
import time


def main():
    with open('mwis.txt') as data:
        num_nodes = int(next(data).strip())
        data_arr = np.array([0 for _ in range(num_nodes)])

        for ind,node_weight in enumerate(data):
            data_arr[ind] = int(node_weight.strip())

    # loaded data, now build up solutions to final solution. our subproblem solutions
    # will be stored in the max_sum list, the first two subproblem solutions are
    # trivial and manually initialized. the solutions for further values depend on the
    # previous two solutions. this is an O(n) loop, with constant work each iteration.
    max_sum = np.array([0 for _ in range(num_nodes)])
    max_sum[0] = data_arr[0]
    max_sum[1] = max(data_arr[0], data_arr[1])
    for i in range(2, num_nodes):
        max_sum[i] = max(max_sum[i-1], max_sum[i-2] + data_arr[i])

    # we're done solving the problem, but now we can back-track if we'd like to see
    # which nodes make up a possible solution (can be ambiguous)
    soln = np.array([False for _ in range(num_nodes)])
    ind = num_nodes - 1
    while ind >= 1:
        # maxsum will only increase if current element is chosen
        if max_sum[ind] > max_sum[ind - 1]:
            soln[ind] = True
            ind -= 2
        else:
            soln[ind - 1] = True
            ind -= 3
    if ind == 0:
        soln[ind] = True

    # we're done, report our findings
    print('\n One possible solution is given (in order) by the nodes:\n',
          data_arr[soln])
    print('\n And the vertices these values correspond to are:\n',
          np.array(np.where(soln)) + 1)  # 1-based indexing of vertices
    print('\n The maximum sum among all weighted independent sets from',
          '\n the data given is', max_sum[-1])


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
