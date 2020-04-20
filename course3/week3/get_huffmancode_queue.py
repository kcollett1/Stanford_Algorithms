#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   We take as input data consisting of the size of the alphabet that we want to
   encode, and the weights/frequencies of the alphabet. In this specific case, we
   are dealing with non-normalized weights rather than probabilities, but this does
   not affect the outcome of our greedy Huffman bottom-up algorithm at all. If a
   non-normalized weight is smaller than another one, it's normalized probability
   will also be smaller, and we just care about relative size in this algorithm.
   As output, we desire to use the Huffman algorithm to encode our alphabet as
   efficiently as possible, meaning minimizing the average number of bits used per
   character. To achieve this, we successively merge the two characters with the
   smallest weight/probability into a binary tree (order of characters in the tree
   doesn't matter and breaking ties arbitrarily still leads to optimal results, so
   actually there can be multiple different encodings chosen that all perform optimally
   in terms of minimizing average bits per character, and in this algorithm we only find
   one such encoding). The answer we are actually seeking though, is the maximum encoding
   length of a single character in our alphabet, and the minimum encoding length of a
   single character in our alphabet (The minimum we would need in any case would be at
   least one bit, but in an optimal encoding the minimum length could be greater than
   that). In this program, I implement the algorithm via maintaining two queues of the
   characters, sorted by weights with quick sort, merging chars from the front of the queues
   as appropriate until all have been merged into one. This code ran in ~0.023852 seconds
   (compare to heap-version of algorithm which ran in ~0.039130 seconds).
'''

from data_structures import *
from quick_sort import *
import time


def main():
    queue_orig = Queue()
    queue_merg = Queue()

    with open('huffman.txt') as alphabet_info:
        num_chars = int(next(alphabet_info).strip())

        if num_chars == 0:
            print('There are no characters in our alphabet; there is nothing to encode!')
            return
        if num_chars < 3:
            print('There are less than 3 characters in our alphabet; the max and min',
                  'encoding length will trivially be 1')
            return

        # go through the chars from input file, add their weights to alphabet list
        alphabet_weights = [0 for _ in range(num_chars)]
        for ind,char_weight in enumerate(alphabet_info):
            alphabet_weights[ind] = int(char_weight.strip())

        # sort by weights, tracking index/char value, add in non-decreasing order to queue
        for char in quick_sort(alphabet_weights):
            # char is a list of [weight, character index], instantiate Character object and enqueue
            queue_orig.enqueue( Character( *char[::-1] ) )

    # initially, we always merge the first two chars in the queue_orig, and enqueue to queue_merg
    # we have non-trivial case with at least two chars in our alphabet
    char1 = queue_orig.dequeue()
    char2 = queue_orig.dequeue()
    char_merg = Character(char_val=char1.char_val, weight=char1.weight + char2.weight,
                          left=char1, right=char2)
    queue_merg.enqueue(char_merg)

    # all chars are in queue in non-decreasing order (with ties broken arbitrarily)
    while queue_orig.len() + queue_merg.len() > 1:  # loop until all chars have been merged into one!
        # at each iteration, we are either merging the first val from queue orig with second val from
        # queue orig, or first val from queue orig with first val from queue merg, or first val from
        # queue merg with second val from queue merg
        if queue_orig.is_empty():
            char1 = queue_merg.dequeue()
            char2 = queue_merg.dequeue()
        elif queue_merg.is_empty():
            char1 = queue_orig.dequeue()
            char2 = queue_orig.dequeue()
        elif queue_orig.front() < queue_merg.front():
            char1 = queue_orig.dequeue()
            if queue_orig.is_empty() or queue_merg.front() <= queue_orig.front():
                char2 = queue_merg.dequeue()
            else:
                char2 = queue_orig.dequeue()
        else:
            char1 = queue_merg.dequeue()
            if queue_merg.is_empty() or queue_orig.front() < queue_merg.front():
                char2 = queue_orig.dequeue()
            else:
                char2 = queue_merg.dequeue()
        # we got our two character to merge, create new internal char node, and enqueue that in merg queue
        char_merg = Character(char_val=char1.char_val, weight=char1.weight + char2.weight,
                              left=char1, right=char2)
        queue_merg.enqueue(char_merg)

    # we've now merged all chars into one, which is the last obj remaining in queue_merg. this object is
    # in fact our binary encoding tree that contains our alphabets optimal encoding based on the weights
    # of characters provided! to answer the question originally posed to us, we want to find the shallowest
    # and deepest char in the tree and report how many bits it takes to encode them to acheive this, we use
    # our queue for a BFS-esque traversal through tree when we see our first leaf, this is the minimum
    # encoding length of a char in our alphabet when we finally reach an empty level, this is max encoding
    # length of a char in our alphabet, which the depth var will be equal to after exiting loop
    depth = -1
    min_encoding = -1

    while not queue_merg.is_empty():
        depth += 1
        nextlev_queue = Queue()
        while not queue_merg.is_empty():
            node = queue_merg.dequeue()
            if min_encoding == -1 and node.left == None and node.right == None:
                min_encoding = depth
            if node.right != None:
                nextlev_queue.enqueue(node.right)
            if node.left != None:
                nextlev_queue.enqueue(node.left)
        queue_merg = nextlev_queue

    # we're done, report answers we found!
    print('\n The maximum encoding length of a character in our alphabet is', depth)
    print(' And the minimum encoding length of a character in our alphabet is', min_encoding)


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
