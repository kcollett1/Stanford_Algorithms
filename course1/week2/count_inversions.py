
# this is my very rough implementation of counting inversions in a list via merge sort

def count_inversions(arr: list)-> (int,list):
    ''' recursively split list into sub-lists and sort/merge those
        building answer up to final result, and counting inversions
        as they are found. this algorithm is O(n*log(n)) running
        time, as it makes two recursive calls each time until a base
        case is hit, but each time the input size is halved. the running time
        of the merge part is linear, and very basically n elements will be
        "sorted"/operated on, and that will happen log_2(n) times.
        returns tuple (int of number of inversions in list, and sorted list).
    '''

    # base case: len(arr) == 1, this is a sorted array
    # or arr is empty, nothing to sort
    if len(arr) < 2:
        return (0, arr)

    # if arr is odd length, subarr2 contains an extra element
    inv1,subarr1 = count_inversions(arr[:len(arr)//2])  # count left only inversions
    inv2,subarr2 = count_inversions(arr[len(arr)//2:])  # count right only inversions
    i1,i2 = 0,0

    # initialize count_inv with left only and right only inversions already
    # counted and add split inversions during following merge sub-routine
    count_inv = inv1 + inv2

    # subarr1,2 are now sorted, ready to merge together
    for i in range(len(arr)):
        if i1 == len(subarr1):
            arr[i:] = subarr2[i2:]
            break
        elif i2 == len(subarr2):
            arr[i:] = subarr1[i1:]
            break
        elif subarr1[i1] <= subarr2[i2]:
            arr[i] = subarr1[i1]
            i1 += 1
        else:
            arr[i] = subarr2[i2]
            count_inv += len(subarr1) - i1
            i2 += 1

    return (count_inv, arr)

#unsorted_l = [4,3,5,6,3,2,5,6,4,4,1249,-31]
#unsorted_l = [6,5,4,3,2,1]  # max number inversions
unsorted_l = [0 for _ in range(100000)]
with open('integer_array.txt', 'r') as fileobj:
    for i,line in enumerate(fileobj):
        unsorted_l[i] = int(line)
#print('unsorted:', unsorted_l)

num_inv, sorted_l = count_inversions(unsorted_l)

#print('sorted:', sorted_l)
#print('num inversions (should be 29)...', num_inv)  # first test list
#print('num inversions (should be 15)...', num_inv)  # second test list
print('num inversions:', num_inv)  # answer to homework problem
