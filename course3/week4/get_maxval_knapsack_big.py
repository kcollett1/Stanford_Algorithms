#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   We take as input data consisting of a number of items that each have an
   associated value and weight. We are given also a maximum weight capacity, and
   the problem is to find the maximum sum of item values that we can possibly get
   by choosing to include some number of our items with the constraint that the
   grouping of items we choose does not have a summed weight exceeding max capacity.
   This algorithm uses the recursive approach to solve it due to the large size of
   the data we are now applying it to. The sorting pre-processing step is definitely
   not a bottle-neck in this code and as such is essentially free for us to perform.
   This code ran in ~20.064419 seconds! This is MUCH better than trying to use the
   iterative approach to solve the problem on this data size!
'''

from quick_sort import *
import numpy as np
import time
import sys
sys.setrecursionlimit(3000)


def main():
    with open('knapsack_big.txt') as data:
        W,n = (int(i) for i in next(data).strip().split(' '))
        vals = [0 for _ in range(n)]
        weights = [0 for _ in range(n)]

        for i,item in enumerate(data):
            vals[i],weights[i] = (int(d) for d in item.strip().split(' '))

    # sort items by weight, keeping track of original index positions to get correct vals
    weights = quick_sort(weights)  # items in weights are now a list: [weight, index]
    min_weight = weights[0][0]

    max_val = {}
    def max_value(i, cap):
        '''
           Calculate the max value that we can get by using items up to (and including)
           item i with a max capacity of cap. We have n total items with weights and
           values specified in the weights and vals lists respectively. This function uses
           recursive calls and memoizes result in max_val hash table once it's computed.
        '''
        token = 'i{0}cap{1}'.format(i, cap)
        if token in max_val:  # already calculated result, just look-up and return it
            return max_val[token]

        # base cases: capacity is less than min_weight, no items can fit in "knapsack"!
        # or num items is 0, nothing to put in "knapsack"!
        if cap < min_weight or i < 1:
            max_val[token] = 0
            return 0

        # soln excluding this item being included in "knapsack", which is just the soln
        # to including item-1 items in the knapsack with same capacity
        token1 = 'i{0}cap{1}'.format(i - 1, cap)
        if token1 in max_val:   # already computed this result, just look-up and set var
            poss_soln1 = max_val[token1]
        else:  # haven't computed it yet, call recursively
            poss_soln1 = max_value(i - 1, cap)

        # soln INCLUDING this item being included in "knapsack", which is the soln to
        # including item-1 items in the knapsack with capacity reduced by this items size
        reduced_weight = cap - weights[i - 1][0]
        if reduced_weight < 0:  # this item will not fit even as the only item
            poss_soln2 = 0
        else:  # we can include this item and possibly some other items can fit as well
            poss_soln2 = vals[weights[i - 1][1]]
            if reduced_weight >= min_weight:  # we can possibly fit other items with this one
                token2 = 'i{0}cap{1}'.format(i - 1, reduced_weight)
                if token2 in max_val:  # already computed this, just look-up and set var
                    poss_soln2 += max_val[token2]
                else:  # haven't computed it yet, call recursively
                    poss_soln2 += max_value(i - 1, reduced_weight)

        # memoize this result and return it
        max_val[token] = max(poss_soln1, poss_soln2)
        return max(poss_soln1, poss_soln2)

    max_val_nW = max_value(n, W)

    # we're done solving the problem, but now we can back-track if we'd like to see
    # which items make up an optimal solution
    soln = set()  # will be indices of the items we include in our "knapsack"
    cap = W
    for i in range(n, 0, -1):  # looping through items labelled 1..n (O(n) to reconstruct)
        token = 'i{0}cap{1}'.format(i, cap)
        i_score = max_val[token]

        not_in_token = 'i{0}cap{1}'.format(i - 1, cap)
        not_in_score = max_val[not_in_token]
        if i_score != not_in_score:  # include this item in "knapsack", update capacity also
            cap -= weights[i - 1][0]  # 1-based item i is 0-based indexed by i-1 in weights list
            soln.add(i)
    soln = np.array(list(soln))

    # we're done, report our findings
    print('\n One possible solution is to use items (specified by index):\n', soln)
    print('\n The maximum value of items we can fit in this "knapsack" of max capacity',
          W, 'is', max_val_nW)

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

    print('\n This code ran in {0:6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
