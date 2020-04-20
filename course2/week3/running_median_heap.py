#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   This code takes the input numbers (size 10,000) from Median.txt
   and calculates a running median using the heap data structures
   (min/max) that I implemented. Results are the same using this
   structure and the binary search tree structure I implemented.
   This code runs in ~0.133771 seconds, while using the binary tree
   structure (not self-balancing), the code runs in ~0.122664 seconds.
'''

from heap import *
import time


def main():
    # from n numbers, median is simply middle number for n odd
    # and middle-left number for n even
    heap_lo = MaxHeap()
    heap_hi = MinHeap()
    running_sum = 0  # sum of all the medians, mod 10000
    itr = 2

    with open('Median.txt') as data:
        # insert first two numbers manually, to avoid checking null at each iteration
        num1 = int(next(data).strip())
        num2 = int(next(data).strip())

        running_sum = (running_sum + num1) % 10000

        if num1 > num2:
            num1, num2 = num2, num1

        running_sum = (running_sum + num1) % 10000

        heap_lo.insert(num1)
        heap_hi.insert(num2)

        for num in data:
            # format num to be int, calculate size the lo heap *should* be, get current max/min of lo/hi heaps
            num = int(num.strip())
            lo_size = itr//2 + 1
            lo_max = heap_lo.get_max()  # O(1)
            hi_min = heap_hi.get_min()  # O(1)

            # insert num into corect heap
            if num <= lo_max:
                heap_lo.insert(num)  # O(log(i))
            else:
                heap_hi.insert(num)  # O(log(i))

            # check if heaps need to be rebalanced - at most need to move one number, 2*O(log(i))
            if heap_lo.size > lo_size:
                move_num = heap_lo.extract_max()  # O(log(i))
                heap_hi.insert(move_num)  # O(log(i))
            elif heap_lo.size < lo_size:
                move_num = heap_hi.extract_min()  # O(log(i))
                heap_lo.insert(move_num)  # O(log(i))

            # done altering heaps, median is the max of the lo heap, update vars accordingly
            running_sum = (running_sum + heap_lo.get_max()) % 10000  # O(1)
            itr += 1

    print('The sum of all the running medians, mod 10000, is:', running_sum)


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('Using a heap to calculate a sum of running medians,',
          'code executed in {0:.6f} seconds'.format(t1-t0))

    raise SystemExit

