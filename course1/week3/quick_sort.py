
'''
    this is my implementation of the quick sort algorithm. we choose a pivot (O(1))
    element, partition the array in place around this pivot (O(n)), and recursively
    call the quick sort algorithm on the partitioned left and right subarrays which
    is O(nlog(n)) on average. function 'my_partition_list' was the function I came
    up to partition the list in-place before watching the video lecture. function
    'partition_list' is the implementation of the way they do it in the video
    lectures, as it was needed to do the homework problem correctly.
'''

import numpy as np
from numpy import random as rand


def choose_pivot(arr: list, start: int, stop: int, choice='first') -> int:
    '''
        this function chooses a pivot element from arr and returns the index
        currently supported choices are 'first', 'last', 'med' (median of
        first/mid/last), and 'rand' which chooses a random pivot. default='first'
    '''
    if choice == 'med':
        med_dict = {arr[start]: start, arr[stop-1]: (stop-1),
                    arr[(stop-start-1)//2 + start]: ((stop-start-1)//2 + start)}
        return med_dict[sorted(med_dict)[1]]
    else:
        return {'first': start, 'last': stop-1, 'rand': rand.randint(start, stop)}[choice]


def my_partition_list(arr: list, piv_ind: int, start: int, stop: int) -> (int,int):
    '''
        this function partitions arr[start:stop] in-place using the piv_ind as the
        pivot and returns the last index and the first index of the subarrays after
        putting the pivot (and all equal values) in their correct positions.
        ex: if there are no duplicates of pivot in the list, left_stop would be
        piv_ind (stop values are exclusive), and right_start would be piv_ind + 1
        ex: if there are duplicates of pivot in the list, they are put after the
        pivot, so the left_stop remains the same, but right_start would then be
        piv_ind + dup_ctr + 1
    '''
    pivot = arr[piv_ind]
    dup_ctr = -1
    left = start
    scan = start
    right = stop - 1
    while scan <= right: # O(n)
        if arr[scan] == pivot:
            dup_ctr += 1
            scan += 1
        elif arr[scan] < pivot:
            arr[left] = arr[scan]
            left += 1
            scan += 1
        else:
            while right > scan and arr[right] > pivot:
                right -= 1
            arr[right],arr[scan] = arr[scan],arr[right]
            right -= 1
    for piv_ind in range(left, left + dup_ctr + 1):
        arr[piv_ind] = pivot

    return left, left + dup_ctr + 1


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
            # increment duplicate pointer and end of smaller array every time we encounter this situation
            dup_stop += 1
            left_stop += 1
        # else arr[scan] > pivot, is already in correct place, scan continues looking at next val

    swap_l, swap_r = start, left_stop - 1
    while swap_l < dup_stop and swap_r >= dup_stop:
        arr[swap_l],arr[swap_r] = arr[swap_r],arr[swap_l]
        swap_l += 1
        swap_r -= 1

    return left_stop - dup_stop + start, left_stop


def quick_sort(arr: list, start: int, stop: int, piv_choice: str) -> int:
    '''
        this function implements the quick sort algorithm sorting arr from start
        (inclusive) to stop (exclusive) in-place using a pivot element recursively
        and returns the number of comparisons in order to answer the homework question
    '''
    # base case, one or zero elements in array
    if stop - start < 2:
        return 0

    num_comparisons = stop - start - 1

    # choose pivot
    pivot = choose_pivot(arr, start, stop, piv_choice)

    # pivot was chosen, now partition around the pivot
    left_stop,right_start = partition_list(arr, pivot, start, stop)
    #left_stop,right_start = my_partition_list(arr, pivot, start, stop)

    # array is partitioned around pivot value, recursively sort the subarrays
    num_comparisons += quick_sort(arr, start, left_stop, piv_choice)
    num_comparisons += quick_sort(arr, right_start, stop, piv_choice)

    return num_comparisons
