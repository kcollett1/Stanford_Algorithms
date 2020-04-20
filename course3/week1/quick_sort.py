
'''
    Using my quicksort implementation from previous course to sort the arrays for the
    homework problem this week. The algorithm is slightly augmented to take as input a
    list and sort maintaining pointers to the original index positions, so it returns
    a list of length-2 lists, the first element being the value from the list, and the
    second element being it's original index from the unsorted list.
'''

from numpy import random as rand


def choose_pivot(arr: list, start: int, stop: int, choice='rand') -> int:
    '''
        this function chooses a pivot element from arr and returns the index
        currently supported choices are 'first', 'last', 'med' (median of
        first/mid/last), and 'rand' which chooses a random pivot. default='first'
    '''
    if choice == 'med':
        med_dict = {arr[start][0]: start, arr[stop-1][0]: (stop-1),
                    arr[(stop-start-1)//2 + start][0]: ((stop-start-1)//2 + start)}
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
        if arr[scan][0] < arr[start][0]:
            if scan != left_stop:
                arr[scan],arr[left_stop] = arr[left_stop],arr[scan]
            left_stop += 1
        elif arr[scan][0] == arr[start][0]:  # taking care of duplicate pivot values
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


def quick_sort(arr: list, start: int, stop: int, piv_choice='rand'):
    '''
        This function is the wrapper of the recursive quick sort function and is
        used for the pre-processing of the list to maintain index vals after sorting
    '''
    # pre-processing to maintain index values
    arr = [[val, ind] for ind,val in enumerate(arr)]  # O(n)
    return quick_sort_recurse(arr, start, stop, piv_choice)  # O(nlog(n))


def quick_sort_recurse(arr: list, start: int, stop: int, piv_choice='rand'):
    '''
        this function implements the quick sort algorithm sorting arr from start
        (inclusive) to stop (exclusive) in-place using a pivot element recursively
        and returns the number of comparisons in order to answer the homework question
    '''
    # base case, one or zero elements in array
    if stop - start < 2:
        return 0

    # choose pivot
    pivot = choose_pivot(arr, start, stop, piv_choice)

    # pivot was chosen, now partition around the pivot
    left_stop,right_start = partition_list(arr, pivot, start, stop)

    # array is partitioned around pivot value, recursively sort the subarrays
    quick_sort_recurse(arr, start, left_stop, piv_choice)
    quick_sort_recurse(arr, right_start, stop, piv_choice)

    return arr
