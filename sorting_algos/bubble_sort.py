
# this is my very rough implementation of bubble sort
# run from command line with: $ python bubble_sort.py


def main():
    test_list = [1,6,3,2,5,7,7,8,4,2,1,19,-2]  # test list to sort
    print('unsorted:', test_list)

    bubble_sort(test_list)
    print('sorted:', test_list)


def bubble_sort(arr: list):
    '''
       repeatedly swap adjacent elements until no more swaps are made.
       runs worst case n times through list, best case only once, but
       each time passing over n elements. therefore this is O(n^2) alg.
    '''
    swaps = True
    ctr = 0
    while swaps:
        swaps = False
        for i in range(len(arr) - ctr - 1):
            if arr[i] > arr[i + 1]:
                arr[i],arr[i + 1] = arr[i + 1],arr[i]
                swaps = True
        ctr += 1


if __name__ == '__main__':
    main()

    raise SystemExit
