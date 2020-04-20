
'''
    this is my implementation of the O(n) randomized algorithm to select
    the i-th smallest element of a 1D array utilizing the pivot and partition
    subroutines of the quick sort algorithm. the O(n) deterministic algorithm
    is also able to be implemented by this code, if you pass piv_choice='determ'
    to function call. this algorithm has slightly worse performance than the
    randomized algorithm due to higher constants.
'''

import numpy as np
from numpy import random as rand


def choose_pivot(arr: list, start: int, stop: int, choice='first') -> int:
    '''
        this function chooses a pivot element from arr and returns the index
        currently supported choices are 'first', 'last', 'med' (median of
        first/mid/last), 'rand' which chooses a pivot at random, and 'determ'
        which uses the deterministic selection algorithm to choose a pivot from
        the "median of medians". default val for pivot choice set to 'first'
        if choice='determ': split arr[start:stop] into (stop-start)/5 lists of 5
        elements each (last element may have 1-4), and sort each subarray (using
        builtin function since each array is only length 5, and choose the median
        of each from this n/5 array of values, use the selection algorithm to find
        the median of this array and use that value as the pivot! median will be the
        n/10-th smallest element in this array (as it is in the (n/5)/2 position)
    '''
    if choice == 'determ':
        meds = [sorted(arr[start+(i*5):start+(i*5)+5])[2] for i in range((stop-start) // 5)]
        extra = (stop - start) % 5
        if extra > 0:
            i = (stop-start) // 5
            meds.append(arr[start+(i*5):start+(i*5)+5][(extra-1) // 2])
        return arr.index(select_ith_smallest(meds, 0, len(meds), choice, (len(meds) - 1) // 2))
    elif choice == 'med':
        med_dict = {arr[start]: start, arr[stop-1]: (stop-1),
                    arr[(stop-start-1)//2 + start]: ((stop-start-1)//2 + start)}
        return med_dict[sorted(med_dict)[1]]
    else:
        return {'first': start, 'last': stop-1, 'rand': rand.randint(start, stop)}[choice]


def partition_list(arr:list, piv_ind: int, start: int, stop: int) -> (int,int):
    '''
        swap to make pivot the first element in the array (if it is not already)
        then scan through array linearly, swapping pairs as needed to move smaller
        values before larger values, keeping track of where we are putting the smaller
        and larger and equal values as we iterate through the list.
    '''
    arr[start],arr[piv_ind] = arr[piv_ind],arr[start]  # put pivot value in beginning of array
    left_stop = start + 1
    dup_stop = start + 1
    for scan in range(left_stop, stop): # O(n)
        if arr[scan] < arr[start]:
            if scan != left_stop:
                arr[scan],arr[left_stop] = arr[left_stop],arr[scan]
            left_stop += 1
        elif arr[scan] == arr[start]:  # taking care of duplicate pivot values
            if left_stop != scan or left_stop != dup_stop:  # we've seen a smaller/larger val
                arr[scan],arr[dup_stop] = arr[dup_stop],arr[scan]
                if left_stop != scan and left_stop != dup_stop:  # we've seen BOTH a smaller/larger val
                    arr[scan],arr[left_stop] = arr[left_stop],arr[scan]
            # inc duplicate pointer and end of smaller array every time we are in this section of code
            dup_stop += 1
            left_stop += 1
        # else arr[scan] > pivot, is already in correct place, scan continues looking at next val

    swap_l, swap_r = start, left_stop - 1
    while swap_l < dup_stop and swap_r >= dup_stop:
        arr[swap_l],arr[swap_r] = arr[swap_r],arr[swap_l]
        swap_l += 1
        swap_r -= 1

    return left_stop - dup_stop + start, left_stop


def select_ith_smallest(arr: list, start: int, stop: int, piv_choice: str, i: int) -> int:
    '''
        this function returns the i-th smallest element in arr from start(inclusive) to
        stop (exclusive). it utilizes the quick sort algorithm, sorting arr in-place
        using a pivot element recursively, but instead each time it finds the correct
        placement of the pivot, it then only needs to recurse on one subarray. using
        a random pivot choice makes this algorithm run in O(n) time, which improves on
        brute force method of sorting the whole array and returning the i-th element
    '''
    # base case, one or zero elements in array
    if stop - start == 0:
        return None  # something went wrong
    elif stop - start == 1:
        return arr[start]

    # choose pivot
    pivot = choose_pivot(arr, start, stop, piv_choice)

    # pivot was chosen, now partition around the pivot
    left_stop,right_start = partition_list(arr, pivot, start, stop)

    # array is now partitioned around pivot, check if pivot is i-th smallest
    if i - 1 in range(left_stop, right_start):
        return arr[left_stop]

    #print('array is partitioned and looking for i-th smallest and pivot is:', arr[start:stop], i, pivot)
    #print('and pivot index (range) is', left_stop,'to', right_start-1)
    # if not, check which side of the partitioned array we should recurse on
    if i - 1 < left_stop:  # i-th smallest element is before the pivot
        return select_ith_smallest(arr, start, left_stop, piv_choice, i)
    else:  # i-th smallest element is after the pivot
        return select_ith_smallest(arr, right_start, stop, piv_choice, i)  # keeping indices same since this is in-place



if __name__ == "__main__":
    #test_arr = [5,1,2,3,4,8,7]
    test_arr = [5,1,2,3,4,2,4,5,3,8,7,8,5,2,1]
    #test_arr = [10,2,3,5,10,6,7,8,9,1]
    print('original array:', test_arr)
    print('\nfinding max value (should be 8):')
    #print(select_ith_smallest(test_arr, 0, len(test_arr), 'rand', 7))
    print(select_ith_smallest(test_arr, 0, len(test_arr), 'determ', len(test_arr)))

    raise SystemExit
