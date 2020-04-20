''' this is my implementation of an algorithm I designed to decide if there exists
    an index in a sorted array of distinct integers that matches the array value
    at that location. this algorithm is basically binary search, as we can check
    the middle element and if it is not equal to the index at that value, either
    all elements before or after it will also be different from their respective
    indices, as the elements at a minimum must change by at least 1 since they
    are distinct. utilizing this fact, we either find the answer to our problem
    to be true, or cut our search space in half at each recursive step, until we're
    done. this makes this an O(log(n)) algorithm, which improves on brute force O(n)
'''

def matching_index(arr: list, start=0)-> bool:
    ''' given arr, a sorted list of distinct integers, return whether there exists
        and index i such that arr[i] = i. this utilizes a binary search method
        and runs in O(log(n)) at worst-case. start is used to keep track of index
        from original list as we possibly make recursive calls into second half of arr
    '''
    if not arr:  # empty array, no matching value possible
        return False

    if len(arr) == 1:  # base case, one element in array
        return start == arr[0]

    mid = start + len(arr) // 2
    match = False

    if mid == arr[mid]:  # we found an index that matches its list value
        match = True
    elif mid < arr[mid]:                   # all values in arr after this one will also
        match =  matching_index(arr[:mid]) # be larger, so only check first half of list
    else:                                          # index is greater than value of list, all values
        match = matching_index(arr[mid+1:], mid+1) # BEFORE will not satify criteria, check second half of list

    return match

test_arr = [-12,1,3,4,6,7,8,124,149]
print('matching index algorithm ran correctly:', matching_index(test_arr) == True)
