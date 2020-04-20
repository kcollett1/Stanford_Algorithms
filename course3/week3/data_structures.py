
# my implemented data structures used to implement Huffman's encoding algorithm stored here


###################### CHARACTER BINARY TREE ###########################################################


class Character:
    '''
       Character class for use in Huffman's algo to store alphabet with
       weighted chars in a MinHeap. The comparisons in the min heap will
       be based on the characters weight. We also use this class as a tree
       node in the binary tree used to store the optimal encoding found.
    '''
    def __init__(self, char_val=None, weight=None, left=None, right=None):
        self.char_val = char_val  # for our application this will simply be a char index
        self.weight = weight
        self.left = left
        self.right = right

    # make all ordering comparisons based on weight
    def __lt__(self, other): return self.weight < other.weight
    def __le__(self, other): return self.weight <= other.weight
    def __gt__(self, other): return self.weight > other.weight
    def __ge__(self, other): return self.weight >= other.weight


#########################################################################################################

################### HEAP ################################################################################


class Heap:
    '''
        My implementation of a min and max heap, from a previous section,
        with some very slight modifications to apply it to Huffman's greedy
        alphabet encoding algorithm.
    '''
    def __init__(self):
        self.arr = []
        self.size = 0  # equivalent to len(self.arr) which is O(1); including here for completeness
        self.pos = {}  # dict of {element in heap: index in heap}, added for O(1) find
                       # (which allows for O(log(n)) delete) NOTE: in this specific implementation
                       # I am altering the pos key to be the char value rather than the Char obj

    def __parent__(self, i):
        ''' Return (0-based) index of parent of value at index i, if i=0 return None. '''
        return (i-1) // 2 if i > 0 else None  # only root (at index 0) has no parent


    def __children__(self, i):
        '''
           Return (0-based) indices of children of value at index i as tuple.
           If not a child value, replace with None. i.e. a node with only 1
           child returns (left_child_ind, None)
        '''
        l = 2*i + 1 if (2*i + 1) < self.size else None
        r = l + 1 if (l != None and (l + 1) < self.size) else None
        return (l ,r)


    def __sift_up__(self, i): pass


    def __sift_down__(self, i): pass


    def __get_top__(self):
        ''' Return top value of heap (min or max), return None if empty heap. '''
        return self.arr[0] if self.size > 0 else None


    def __extract_top__(self):
        ''' Remove top value and rebalance heap, return value removed, None if empty heap. '''
        if self.size == 0:  # no values in heap, nothing to remove
            return None

        # record top value, replace it with the last element, remove last element, decrement size
        top_val = self.arr[0]
        top_ind = top_val.char_val  # this is specific for Huffman's greedy algo
        last_val = self.arr[self.size - 1]
        last_ind = last_val.char_val  # this is specific for Huffman's greedy algo
        self.arr[0] = last_val
        self.pos[last_ind] = 0  # update index of last_val which was replaced to be at index 0
        self.arr.pop()  # O(1) with pythons list structure
        del self.pos[top_ind]  # remove top_val from pos dict since we removed it from heap
        self.size -= 1

        # finally, sift down the (new) first element, and return top value which has been removed
        self.__sift_down__(0)  # O(log(n))
        return top_val


    def __insert__(self, val):
        ''' Insert a val into the heap, increment size of heap by 1. O(log(n)) '''
        self.arr.append(val)  # amortized O(1) with pythons list structure
        self.pos[val.char_val] = self.size  # add val to pos dict pointing to last index of heap
        self.size += 1
        self.__sift_up__(self.size - 1)  # sift up element we just added, O(log(n))


    def __delete__(self, char_val):
        ''' Delete and return val from the heap if it exists. If not, return None. O(log(n))'''
        ind = self.find(char_val)  # O(1)
        if ind == None:
            return None

        # replace this element with last element, remove last element from heap, decrement size
        self.size -= 1
        this_val = self.arr[ind]
        last_val = self.arr[self.size]
        last_ind = last_val.char_val  # this is specific for Huffman's greedy algo
        self.arr[ind] = last_val
        self.pos[last_ind] = ind  # update last_val index in pos dict to ind we just placed it at
        self.arr.pop()  # O(1) with pythons list structure
        del self.pos[char_val]  # and remove val from pos dict since we just removed it from the heap

        if ind == self.size:  # we removed the last element, we're done
            return this_val

        # try sifting up and down if needed; if it's not, nothing will change, so no harm done
        self.__sift_up__(ind)    # heap property only violated at most in one direction, only one
        self.__sift_down__(ind)  # will actually do any work, at worst O(1*log(n)) runtime.

        # return extracted val to indicate success
        return this_val


    def find(self, char_val):
        ''' Find and return index of val in heap if it exists. If not, return None. O(1) '''
        if char_val not in self.pos:
            return None
        else:
            return self.pos[char_val]


class MinHeap(Heap):
    '''
       Heap property in min heap is that val of a node <= all of it's children
       Main methods that need to be implemented here are sift up and sift down,
       the others are largely inherited from Heap class, with some minor bookkeeping..
    '''
    def __sift_up__(self, i):  # override Heap defined sift up method
        '''
           Swap elements (upwards in heap tree) repeatedely until heap property
           is no longer violated for value at index i. O(log(n)) runtime worst case.
        '''
        if i >= self.size or i < 0:  # index is out of range, nothing to sift
            return

        parent = self.__parent__(i)

        # main loop can run up to log_2(n) times (depth of heap tree, one swap per level at most)
        while parent != None and self.arr[i] < self.arr[parent]:
            # heap property is violated, swap elements, update parent/current indices
            # also need to track the index swap in pos dict
            self.pos[self.arr[parent].char_val] = i  # specific for Huffman's algo
            self.pos[self.arr[i].char_val] = parent  # specific for Huffman's algo
            self.arr[parent], self.arr[i] = self.arr[i], self.arr[parent]
            i, parent = parent, self.__parent__(parent)


    def __sift_down__(self, i):  # override Heap defined sift down method
        '''
           Swap elements (downwards in heap tree) repeatedely until heap property
           is no longer violated for value at index i. O(log(n)) runtime worst case.
        '''
        if i >= self.size or i < 0:  # index is out of range, nothing to sift
            return

        l_child, r_child = self.__children__(i)
        min_child = l_child
        if r_child != None and self.arr[r_child] <= self.arr[l_child]:
            min_child = r_child

        # main loop can run up to log_2(n) times (depth of heap tree, one swap per level at most)
        while min_child != None and self.arr[i] > self.arr[min_child]:
            # heap property is violated, swap elements, update current/children/min_child indices
            # also need to track the index swap in pos dict
            self.pos[self.arr[min_child].char_val] = i  # specific for Huffman's algo
            self.pos[self.arr[i].char_val] = min_child  # specific for Huffman's algo
            self.arr[i], self.arr[min_child] = self.arr[min_child], self.arr[i]
            i, (l_child, r_child) = min_child, self.__children__(min_child)
            min_child = l_child
            if r_child != None and self.arr[r_child] <= self.arr[l_child]:
                min_child = r_child


    def get_min(self): return self.__get_top__()

    def extract_min(self): return self.__extract_top__()

    def insert(self, val): self.__insert__(val)

    def delete(self, val): return self.__delete__(val)


class MaxHeap(MinHeap, Heap):
    '''
       Heap property in max heap is that val of a node >= all of it's children.
       This implementation of maxheap uses a minheap and inserts the values into
       the heap negated. Data that you put in max heap needs to be able to be negated.
    '''
    def get_max(self):
        max_val = self.__get_top__()
        return -max_val if max_val != None else None


    def extract_max(self):
        max_val = self.__extract_top__()
        return -max_val if max_val != None else None


    # override MinHeap insert method to insert negative values
    def insert(self, val): self.__insert__(-val)

    # override MinHeap delete method to actually delete the negated value passed in by user
    def delete(self, val):
        deleted_val = self.__delete__(-val)
        return -deleted_val if deleted_val != None else None


###########################################################################################################

############### QUEUE #####################################################################################


class QueueNode:  # use to hold whatever type of data you're interested in using
    def __init__(self, val=None, nex=None, prv=None):
        self.val = val  # of type whatever data you're interested in using
        self.nex = nex  # of type QueueNode
        self.prv = prv  # of type QueueNode


class Queue:
    ''' my implementation of a queue class '''
    def __init__(self):
        self.head = None  # of type QueueNode
        self.tail = None  # of type QueueNode
        self.size = 0


    def enqueue(self, val):
        '''Add node with value val to back of queue. Return val to indicate success.'''
        add_node = QueueNode(val=val, nex=self.tail)

        if self.size == 0:  # empty queue, update both head and tail pointers
            self.tail = add_node
            self.head = add_node
        else:  # non-empty, just update tail and current tail's prv pointer
            self.tail.prv = add_node
            self.tail = add_node

        self.size += 1
        return val


    def dequeue(self):
        '''Remove and return first value from queue. If empty, return None.'''
        if self.size == 0:  # empty queue, nothing to remove
            return None
        else:
            frontval = self.head.val
            if self.size == 1:  # removing last element from queue, update head and tail pointers
                self.head = None
                self.tail = None
            else:  # there will be remaining elements in queue, update head and new head's nex pointer
                self.head = self.head.prv
                self.head.nex = None

            self.size -= 1  # decrement size of queue
            return frontval


    def front(self):
        '''Return front (first in) value of queue. If empty, return None.'''
        if self.size == 0:
            return None
        else:
            return self.head.val


    def back(self):
        '''Return back (last in) value of queue. If empty, return None.'''
        if self.size == 0:
            return None
        else:
            return self.tail.val


    def len(self):
        return self.size


    def is_empty(self):
        return self.size == 0


    def reset(self):
        '''Warning: emptying entire queue!!!'''
        self.size = 0
        self.head = None
        self.tail = None


###########################################################################################################
