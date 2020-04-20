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
   that). In this program, I implement the algorithm via maintaining the characters in a
   Min Heap, merging the two min characters from the heap into one, until all have been
   merged into one. This code ran in ~0.039130 seconds (compare to queue-version of this
   algorithm which ran in ~0.023852 seconds).
'''

from data_structures import *
import time


def main():
    # initialize the min heap to store the characters sorted by their weights
    alphabet = MinHeap()

    with open('huffman.txt') as alphabet_info:
        num_chars = int(next(alphabet_info).strip())

        if num_chars == 0:
            print('There are no characters in our alphabet; there is nothing to encode!')
            return
        if num_chars < 3:
            print('There are less than 3 characters in our alphabet; the max and min',
                  'encoding length will trivially be 1')
            return

        # go through the chars from input file, add them as Character objects to the heap
        for ind,char_weight in enumerate(alphabet_info):
            alphabet.insert( Character( ind, float( char_weight.strip() ) ) )

    # all of our characters are now in the heap. for this algo, we want to "merge" the two
    # minimum weight chars from our current alphabet. to do this, we extract the two min
    # chars, create a new "internal" node char with weight equal to the sum of the two we're
    # merging together and the index picked arbitrarily from the two being merged. we insert
    # this merged "char" (which is actually a binary tree with pointers to all merged chars)
    # back into the heap, and do this repeatedly until all chars have been "merged" into one.
    # as we merge, we build our binary tree of encodings, and at the end we have one value left
    # in the heap which is actually our encoding tree with all chars as leaves!
    while alphabet.size > 1:
        min_char1 = alphabet.extract_min()
        min_char2 = alphabet.extract_min()
        new_val = min_char1.char_val
        new_weight = min_char1.weight + min_char2.weight
        new_internal_char = Character(char_val=new_val, weight=new_weight,
                                      left=min_char1, right=min_char2)
        alphabet.insert(new_internal_char)

    # we've now merged all chars into one in our heap, and this val is our tree that
    # contains our alphabets optimal encoding based on the weights of characters provided!
    # to answer the question originally posed to us, we want to find the shallowest and deepest
    # char in the tree and report how many bits it takes to encode them
    # to acheive this, we use a queue for BFS-esque traversal through tree
    # when we see our first leaf, this is the minimum encoding length of a char in our alphabet
    # when we finally reach an empty level, this is max encoding length of a char in our alphabet
    BFS_queue = Queue()
    BFS_queue.enqueue(alphabet.get_min())
    depth = -1
    min_encoding = -1
    avg_encoding = 0

    while not BFS_queue.is_empty():
        depth += 1
        nextlev_queue = Queue()
        while not BFS_queue.is_empty():
            node = BFS_queue.dequeue()
            if node.left == None and node.right == None:
                avg_encoding += depth * node.weight
            if min_encoding == -1 and node.left == None and node.right == None:
                min_encoding = depth
            if node.right != None:
                nextlev_queue.enqueue(node.right)
            if node.left != None:
                nextlev_queue.enqueue(node.left)
        BFS_queue = nextlev_queue

    max_encoding = depth

    # we're done, report answers we found!
    print('\n The maximum encoding length of a character in our alphabet is', max_encoding)
    print('\n And the minimum encoding length of a character in our alphabet is', min_encoding)
    print('\n The expected number of bits to encode 1000-chars is {0}.'.format(avg_encoding*1000))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
