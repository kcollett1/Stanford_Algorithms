''' this is my implementation of the divide-and-conquer O(n*log(n))
    algorithm to find the smallest distance between any two points
    given a 2-D set of points. we first use merge sort (O(n*log(n)))
    to sort the points based on BOTH x- and y- coordinates and store
    the results in separate arrays. next, recursively find closest
    points in left- and right-half subarrays. base-case is 2 points
    for which we just return the distance between them, or 3 points
    for which we just manually compare the 3 distances and return the
    minimum. then we set d to be the minimum of the two closest distances
    found in both halves of the subarray, and search in a reduced space
    for any possible closer distances that are from points lying on
    different sides of the array split. if this is the case, neither
    point can be further away from the middle point than d (distances
    from points between the two halves that are outside this range don't
    matter because they will automatically have distance greater than d
    and we just want to find a minimum), so we get rid of all points
    with x-coordinates outside of this range, and go through the y-sorted
    points to find the distances but for each y point we only need to
    look at points that are 7 away due to geometric considerations
    (if there are more than 8 points in the search space, a smaller
    distance d would have been found when searching in the recursive
    step as this forces the points to be closer than d on strictly one
    side of the array split, but since we did not find a smaller d in
    the recursive step, it must be the case that there are only at most
    8 points in the search space, therefore any outside of that are
    further away and we don't need to calculate anything). finally, we
    just return the minimum of d and the value we find from searching
    the split distances.
'''

import math

def merge_sort(arr: list, sortind=0)-> list:
    ''' recursively split 2D list into sub-lists and sort/merge
        those on the 'sortind' element (default first) building answer
        up to final result. this algorithm is O(n*log(n)) running time,
        as it makes two recursive calls each time until a base case is
        hit, but each time the input size is halved. the running time
        of the merge part is linear, and very basically n elements will
        be "sorted"/operated on, and that will happen log_2(n) times
    '''

    # base case: len(arr) == 1, this is a sorted array
    # or arr is empty, nothing to sort
    if len(arr) < 2:
        return arr

    # if arr is odd length, subarr2 contains an extra element
    subarr1 = merge_sort(arr[:len(arr)//2], sortind)
    subarr2 = merge_sort(arr[len(arr)//2:], sortind)

    # subarr1,2 are now sorted, ready to merge together
    i1,i2 = 0,0
    for i in range(len(arr)):
        if i1 == len(subarr1):
            arr[i:] = subarr2[i2:]
            break
        elif i2 == len(subarr2):
            arr[i:] = subarr1[i1:]
            break
        elif subarr1[i1][sortind] <= subarr2[i2][sortind]:
            arr[i] = subarr1[i1]
            i1 += 1
        else:
            arr[i] = subarr2[i2]
            i2 += 1

    return arr

def dist(p1: tuple, p2: tuple) -> (int,(tuple,tuple)):
    ''' calculate the distance between two pairs of points on a euclidean 2D plane'''
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2), (p1,p2)

def closest_pair_recurse(Px: list, Py: list) -> (int,(tuple,tuple)):
    '''this is the recursion function to actually do they heavy lifting and find the
       closest pair. we need main function (below) to take care of the preprocessing step
    '''
    if len(Px) < 2:  # need at least 2 points to compute a distance
        return None

    # base case, 2 points
    if len(Px) == 2:
        return dist(Px[0],Px[1])

    # base case, 3 points
    if len(Px) == 3:
        min_d,min_pts = dist(Px[0], Px[1])
        for i in (0,1):
            d,pts = dist(Px[i], Px[2])
            if d < min_d:
                min_d = d
                min_pts = pts
        return min_d, min_pts

    left_x,right_x = Px[:len(Px)//2], Px[len(Px)//2:]  # these are O(n) steps
    left_y,right_y = Py[:len(Py)//2], Py[len(Py)//2:]

    min_d,min_pts = closest_pair_recurse(left_x, left_y)
    right_d,right_pts = closest_pair_recurse(right_x, right_y)
    if right_d < min_d:
        min_d = right_d
        min_pts = right_pts

    # combine step, check possible cross points
    # first prune unneeded points that lay outside of mid_x +/- min_d
    # but sorted by y, so we use our pre-sorted Py list now
    min_x, max_x = left_x[-1][0] - min_d, left_x[-1][0] + min_d
    S = []
    for pt in Py:
        if pt[0] > min_x and pt[0] < max_x:
            S.append(pt)

    for i in range(len(S) - 1):
        for j in range(i + 1, min(i + 8, len(S))):  # only need to check the 7 points following S[i]
            dis,pts = dist(S[i], S[j])
            if dis < min_d:
                min_d = dis
                min_pts = pts

    return min_d, min_pts


def closest_2D_points(points: list) -> (tuple,tuple):
    ''' given 2D array of points on a plane in the form [(x1,y1), find the closest pair'''
    # pre-process. sort on x- and y- coordinate separately
    # both O(nlogn) operations
    points_x = merge_sort(points)
    points_y = merge_sort(points, 1)

    # step into recursion now, returned result will be final answer
    return closest_pair_recurse(points_x, points_y)[1]
    

test_points = [(1,1),(2,2),(10,10),(50,3),(50.5,3),(9,9),(7,6),(124,41),(-14,53),(35,31),(51,3)]
print('original list:', test_points)
print('closest pair:', closest_2D_points(test_points))
#print('sorted on x-coord:', merge_sort(test_points))
#print('sorted on y-coord:', merge_sort(test_points, 1))
