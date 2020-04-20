''' this is my implementation of an algorithm I designed to compute
    the maximum value in an array that is unimodal and all values
    distinct. this works in a similar fashion to binary search,
    it looks at the middle of the array, determines if that point
    is the maximum, or if the array is currently increasing or decreasing
    and recursively searches one array of roughly half the size until
    it finds the correct value. this runs in O(log(n)).
'''

def max_in_unimodal(arr: list, currmax=None)-> int:
    ''' this function takes in a unimodal list, i.e. all numbers
        are strictly increasing until the maximum, and then they
        are all strictly decreasing, and finds recursively the
        maximum value. this runs in O(log(n)) time at worst-case.
    '''

    if len(arr) == 0:
        return currmax  # if empty array passed initially, will return None

    if len(arr) < 3:  # base case, if 2 elements or smaller, just find the max val
        if not currmax:
            return max(arr)
        else:
            return max(currmax, max(arr))

    mid = len(arr) // 2
    a = arr[mid] - arr[mid-1]
    b = arr[mid+1] - arr[mid]

    # if currently increasing, a and b both positive
    # if max, a positive, b negative
    # if currently decreasing, a and b both negative
    if a > 0 and b < 0:  # we found the maximum
        return arr[mid]
    elif a > 0 and b > 0:  # arr is currently increasing
        if not currmax:
            currmax = arr[mid+1]
        else:
            currmax = max(currmax, arr[mid+1])
        currmax = max_in_unimodal(arr[mid+2:], currmax)
    else:  # a and b both negative, arr is currently decreasing
        if not currmax:
            currmax = arr[mid-1]
        else:
            currmax = max(currmax, arr[mid-1])
        currmax = max_in_unimodal(arr[:mid-1], currmax)

    return currmax

testarr = [-102,-98,-73,-32,-1,0,1,2,3,4,5,6,5,4,3,2,1,0,-1,-4,-1042]
print('answer should be 6...:', max_in_unimodal(testarr))
