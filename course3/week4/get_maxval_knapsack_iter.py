#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   We take as input data consisting of a number of items that each have an
   associated value and weight. We are given also a maximum weight capacity, and
   the problem is to find the maximum sum of item values that we can possibly get
   by choosing to include some number of our items with the constraint that the
   grouping of items we choose does not have a summed weight exceeding max capacity.
   This algorithm naively computes all possible sub-problems (O(n*W) in space) and
   memoizes them iteratively in a double-loop. This could lead to wasted CPU and
   memory if we are computing a lot of sub-problems that we never actually need to use.
   This code ran in ~1.944682 seconds.
'''

import numpy as np
from quick_sort import *
import time


def main():
    with open('knapsack1.txt') as data:
        W,n = (int(i) for i in next(data).strip().split(' '))
        vals = np.array([0 for _ in range(n)])
        weights = np.array([0 for _ in range(n)])

        for i,item in enumerate(data):
            vals[i],weights[i] = (int(d) for d in item.strip().split(' '))

    ###################################
    # sort items by weight, keeping track of original index positions to get correct vals
    # when we do this pre-processing step, we see basically no change in run-time. without
    # sorting first, code runs in ~1.97 seconds. when we sort first, code runs in ~1.94 seconds.
    weights = quick_sort(weights)  # items in weights are now a list: [weight, index]
    min_weight = weights[0][0]
    ##################################

    # loaded data, now build up solutions to final solution. our subproblem solns will
    # be stored in the max_val 2-D list (size n by W). the first W subproblem solns
    # given by including 0 items for any possible weight capacity (up to W) are trivial
    # and manually initialized. the solutions for further values depend on two previous
    # sub-solns, which will already have been calculated. we may be doing unnecessary
    # work calculating sub-problems that never actually get used, but the data for this
    # specific problem is small enough that we can do this and not suffer much in our
    # computation time/memory used. this is an O(n*W) loop, with constant work each
    # iteration. for large W or n this may need to be altered for feasibility.
    max_val = np.array([[0 for _ in range(W + 1)] for _ in range(n + 1)])
    for item in range(1, n + 1):
        for capacity in range(min_weight, W + 1):
            # soln excluding this item being included in knapsack, which is just the soln
            # to including item-1 items in the knapsack with same capacity
            poss_soln1 = max_val[item - 1, capacity]

            # soln INCLUDING this item being included in knapsack, which is the soln to
            # including item-1 items in the knapsack with capacity reduced by this items size
            reduced_weight = capacity - weights[item - 1][0]
            if reduced_weight < 0:  # this item will not fit even as the only item
                poss_soln2 = 0
            else:  # we can include this item and possibly some other items can fit as well
                poss_soln2 = vals[weights[item - 1][1]]
                if reduced_weight >= min_weight:  # we can possibly fit other items with this one
                    poss_soln2 += max_val[item - 1, reduced_weight]

            max_val[item, capacity] = max(poss_soln1, poss_soln2)

    # we're done solving the problem, but now we can back-track if we'd like to see
    # which items make up an optimal solution
    soln = set()  # will be a set of indices of the items we include in our "knapsack"
    cap = W
    for i in range(n, 0, -1):  # looping through items labelled 1..n (O(n) to reconstruct)
        i_score = max_val[i, cap]

        not_in_score = max_val[i - 1, cap]
        if i_score != not_in_score:  # include this item in "knapsack", update capacity also
            cap -= weights[i - 1][0]  # 1-based item i is 0-based indexed by i-1 in weights list
            soln.add(i)
    soln = np.array(list(soln))

    # we're done, report our findings
    print('\n The maximum value of items we can fit in this "knapsack" of max capacity',
          W, 'is', max_val[n, W])
    print('\n One possible solution is to use items (specified by index):\n', soln)

    # sanity check, add up the weights and values of items we included in our reconstructed soln
    tot_weight_soln = 0
    tot_val_soln = 0
    for i in np.nditer(soln):
        tot_weight_soln += weights[i - 1][0]
        tot_val_soln += vals[weights[i - 1][1]]
    print('\n Using the reconstructed solution, the total weight of our included items is',
          tot_weight_soln, 'which\n should not exceed the max capacity weight of', W,
          'and the total value of these items is', tot_val_soln)


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
