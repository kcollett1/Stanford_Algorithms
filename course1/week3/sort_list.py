#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   This code takes as input a list of numbers from 1 to 10000 in unsorted order. We run quick_sort
   on the list to sort it, using four different pivot choice methods. First, we always choose the
   first element to be the pivot. Second, we always choose the last element to be the pivot. Next,
   we choose the "median-of-three" to be the pivot (meaning we look at the first, middle, and last
   elements and choose the median of those to be the pivot). Last, just for fun, we run a series
   of experiments choosing a random pivot each time, to compare performance against the other
   metrics. The output we are searching for here is the number of comparisons the quick sort algo
   needs to make with each choice of pivot (which is indicative of big O running time). In the case
   of the random pivot choice, we take the average of a series of sorts using a random pivot.
   This code ran in ~10.30546 seconds.
   Run from command line with either $ ./sort_list.py or $ python sort_list.py
'''


from quick_sort import *
import time


def main():
    sorted_arr = [i for i in range(1,10001)]
    unsorted_arr = [0 for _ in range(10000)]
    with open('quick_sort.txt') as fileobj:
        for i,line in enumerate(fileobj):
            unsorted_arr[i] = int(line)
   
    unsorted_arr1 = list(unsorted_arr)
    unsorted_arr2 = list(unsorted_arr)
    unsorted_arr3 = list(unsorted_arr)
   
    num_comp_first = quick_sort(unsorted_arr1, 0, len(unsorted_arr1), 'first')
    num_comp_last = quick_sort(unsorted_arr2, 0, len(unsorted_arr2), 'last')
    num_comp_med = quick_sort(unsorted_arr3, 0, len(unsorted_arr3), 'med')
   
    # just for fun, testing randomized pivot choices and how that effects number of comparisons made
    # taking average of multiple randomized runs
    num_comp_rand_all_runs = 0
    sample_size = 100
    for i in range(sample_size):
        unsorted_arr4 = list(unsorted_arr)
        num_comp_rand_all_runs += quick_sort(unsorted_arr4, 0, len(unsorted_arr4), 'rand')
    num_comp_rand_av = num_comp_rand_all_runs // sample_size
   
    # sanity/corectness check
    print('\n Lists are completely sorted...', unsorted_arr1 == sorted_arr and unsorted_arr2 == sorted_arr and
                                               unsorted_arr3 == sorted_arr and unsorted_arr4 == sorted_arr)

    # the homework answers are the first three numbers reported (random runs are just extra)
    print('\n Number of comparisons using the first, last, med-of-three, and random element as the pivot are',
          '\n {0}, {1}, {2}, and {3}'.format(num_comp_first, num_comp_last, num_comp_med, num_comp_rand_av))

    # expected value of num of comparisons (2nlogn), and upper limit (n^2) to num of comparisons:
    print('\n Expected val of num of comparisons 2*n*log(n) and upper limit n^2:',
          int(20000*np.log(10000)), 10000**2)


if __name__ == '__main__':
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.5f} seconds.\n'.format(t1 - t0))

    raise SystemExit
