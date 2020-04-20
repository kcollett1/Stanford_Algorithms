#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   This code takes the input numbers (size 10,000) from Median.txt
   and calculates a running median using the binary search tree
   (not self-balancing) structure I implemented. Results are the
   same using this structure and the heap structure I implemented.
   This code runs in ~0.122664 seconds, while using the heap
   structure, the code runs in ~0.133771 seconds.
'''


from binary_search_tree import *
import time


def main():
    # from n numbers, median is simply middle number for n odd
    # and middle-left number for n even
    tree_obj = BinarySearchTree()
    running_sum = 0  # sum of all the medians, mod 10000

    with open('Median.txt') as data:
        for num in data:
            num = int(num.strip())
            tree_obj.insert(num)  # O(height)
            running_sum = (running_sum + tree_obj.get_median()) % 10000  # O(height)

    print('The sum of all the running medians, mod 10000, is:', running_sum)


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('Using an (unbalanced) binary search tree to calculate a sum of running medians,',
          'code executed in {0:.6f} seconds'.format(t1-t0))

    raise SystemExit

