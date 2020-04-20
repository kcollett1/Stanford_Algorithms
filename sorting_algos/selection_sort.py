
# This is my very rough implementation of selection sort
# run from command line with $ python selection_sort.py


def main():
    test_list = [6,7,5,6,4,6,7,3,2,1]
    print('unsorted:', test_list)

    iter_list = list(test_list)
    selection_sort_iter(iter_list)
    print('sorted via iterative implementation:', iter_list)

    recurs_list = list(test_list)
    selection_sort_recurs(recurs_list, 0)
    print('sorted via recursive implementation:', recurs_list)


def selection_sort_recurs(arr: list, ind: int):
    '''
       Find minimum value from arr starting from index ind and swap element at ind with appropriate
       value. Repeatedly do this from (ind+1), etc. until end of list. Pass in list to sort, and ind=0.
    '''
    if not arr:  # empty list, nothing to sort
        return arr

    if ind == len(arr) - 1:  # at last element in list, done sorting
        return arr

    # find minimum and index of minimum - roughly O(n) operation
    # after each recursive call the input size is decreased by 1
    min_ind, min_val = ind, arr[ind]
    for i,v in enumerate(arr[ind+1:], start=ind+1):
        if v < min_val:
            min_ind,min_val = i,v

    # swap min element found with first unsorted element
    # redundant if ind == min_ind
    arr[ind], arr[min_ind] = arr[min_ind], arr[ind]

    # run selection sort of remaining unsorted list recursively
    # this is called O(n) times (n-1)
    # therefore, this algorithm is *at most* O(n^2)
    arr = selection_sort_recurs(arr, ind + 1)


def selection_sort_iter(arr: list):
    ''' See above description. This alg uses an iterative approach rather than a recursive one. '''
    # if empty, outer loop will not execute, and empty list is returned
    for start_ind in range(len(arr)):
        min_ind = start_ind

        # inner loop will not execute for last element in list
        for search_ind in range(start_ind + 1, len(arr)):
            if arr[search_ind] < arr[min_ind]:
                min_ind = search_ind

        arr[start_ind],arr[min_ind] = arr[min_ind], arr[start_ind]


if __name__ == '__main__':
    main()

    raise SystemExit

