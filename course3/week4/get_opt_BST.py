#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   We take as input data consisting of keys belonging to a binary search tree, and the
   probability/weight/frequency associated with each key. We output the optimal binary
   search tree's average (weighted) search time (we can alter this to actually output the
   optimal BST strcuture as well, but this is just a quick-and-dirty implemntation for
   learning purposes and the actual tree is not needed to analyze correctness/run-time).
'''

import numpy as np
import time


def main():
    keys = [1, 2, 3, 4, 5, 6, 7]
    weights = [0.2, 0.05, 0.17, 0.1, 0.2, 0.03, 0.25]
    n = len(keys)
    sub_solns = np.array([[0. for _ in range(n)] for _ in range(n)])
    roots = np.array([[0 for _ in range(n)] for _ in range(n)])

    # initialize: each sub-tree with itself as the only key has min search time of its own weight
    for i in range(n):
        sub_solns[i,i] = weights[i]
        roots[i,i] = i + 1

    for s in range(1, n):
        for i in range(n - s):
            sum_weights = sum(weights[i:i+s+1])
            # for root = i (the first key is root):
            min_searchtime = sub_solns[i + 1, i + s]
            min_root = i + 1
            # for root = i + s (the last key is root):
            searchtime = sub_solns[i, i + s - 1]
            if searchtime < min_searchtime:
                min_searchtime = searchtime
                min_root = i + s + 1
            # for all other roots from i+1 to i+s-1
            for root in range(i + 1, i + s):
                searchtime = sub_solns[i, root - 1] + sub_solns[root + 1, i + s]
                if searchtime < min_searchtime:
                    min_searchtime = searchtime
                    min_root = root + 1

            sub_solns[i, i + s] = min_searchtime + sum_weights
            roots[i, i + s] = min_root

    # each entry represents a level of the tree, with the root keys from left to right, and None
    # marking that the parent node does not have a child on this branch
    opt_tree = []
    def recon(start, end, level):
        if len(opt_tree) == level:
            opt_tree.append([])

        if start > end:
            opt_tree[level].append(None)
            return

        this_root = roots[start, end]
        opt_tree[level].append(this_root)

        recon(start, this_root - 2, level + 1)  # left child
        recon(this_root, end, level + 1)  # right child
    recon(0, n-1, 0)

    # we're done, report our findings
    print('\n The optimal (minimal) BST given the keys and their associated frequencies',
          '\n has a weighted average search time of {0}'.format(sub_solns[0, n-1]))
    print('\n And the optimal tree looks like:')
    for level in opt_tree:
        print(' ', level)


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
