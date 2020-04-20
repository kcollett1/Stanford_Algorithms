
# this is my very rough implementation of merge sort
# run from command line with $ python merge_sort.py


def main():
    test_list = [4,3,5,6,3,2,5,6,4,4,1249,-31]
    print('unsorted:', test_list)

    merge_sort(test_list)
    print('sorted:', test_list)


def merge_sort(arr: list) -> list:
    '''
       recursively split list into sub-lists and sort/merge those building answer up
       to final result. this algorithm is O(n*log(n)) running time, as it makes two
       recursive calls each time until a base case is hit, but each time the input size
       is halved. the running time of the merge part is linear, and very basically n
       elements will be "sorted"/operated on, and that will happen log_2(n) times
    '''
    # base case: len(arr) == 1, this is a sorted array
    # or arr is empty, nothing to sort
    if len(arr) < 2:
        return arr

    # if arr is odd length, subarr2 contains an extra element
    subarr1 = merge_sort(arr[:len(arr)//2])
    subarr2 = merge_sort(arr[len(arr)//2:])

    # subarr1,2 are now sorted, ready to merge together
    i1,i2 = 0,0
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
            i2 += 1

    return arr


if __name__ == '__main__':
    main()

    raise SystemExit
