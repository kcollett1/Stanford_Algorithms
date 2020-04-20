'''
    my implementation of a min and max heap. I use min heap for
    djikstra's algo and both min/max for calculating a running median
    alternatively, a min-heap could be used as a max-heap if we negate
    the values as we insert them. max heap is implemented here with min
    heap implementation but insertion is altered so that values passed
    are negated before inserting them into heap.
'''

class Heap:
    def __init__(self):
        self.arr = []
        self.size = 0  # equivalent to len(self.arr) which is O(1); including here for completeness


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
        self.arr[0] = self.arr[self.size - 1]
        self.arr.pop()  # O(1) with pythons list structure
        self.size -= 1

        # finally, sift down the (new) first element, and return top value which has been removed
        self.__sift_down__(0)  # O(log(n))
        return top_val


    def __insert__(self, val):
        ''' Insert a val into the heap, increment size of heap by 1. O(log(n)) '''
        self.arr.append(val)  # amortized O(1) with pythons list structure
        self.size += 1
        self.__sift_up__(self.size - 1)  # sift up element we just added, O(log(n))


    def __delete__(self, i):
        '''
           Delete val from the heap at index i if it exists, and rebalance.
           Return val removed; if not a valid index in the heap, return None.
        '''
        if i >= self.size:  # not a valid value in the heap, can't delete anything
            return None

        # keep track of value, replace with last element, remove last element from heap, decrement size
        val = self.arr[i]
        self.size -= 1
        self.arr[i] = self.arr[self.size]
        self.arr.pop()  # O(1) with pythons list structure

        # try sifting up and down if needed; if it's not, nothing will change, so no harm done
        self.__sift_up__(i)  # heap property only violated at most in one direction, only one will
        self.__sift_down__(i)  # actually do any work, at worst O(1*log(n))

        # return extracted val
        return val


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
        parent = self.__parent__(i)

        # main loop can run up to log_2(n) times (depth of heap tree, one swap per level at most)
        while parent != None and self.arr[i] < self.arr[parent]:
            # heap property is violated, swap elements, update parent/current indices
            self.arr[parent], self.arr[i] = self.arr[i], self.arr[parent]
            i, parent = parent, self.__parent__(parent)


    def __sift_down__(self, i):  # override Heap defined sift down method
        '''
           Swap elements (downwards in heap tree) repeatedely until heap property
           is no longer violated for value at index i. O(log(n)) runtime worst case.
        '''
        l_child, r_child = self.__children__(i)
        min_child = l_child
        if r_child != None and self.arr[r_child] <= self.arr[l_child]:
            min_child = r_child

        # main loop can run up to log_2(n) times (depth of heap tree, one swap per level at most)
        while min_child != None and self.arr[i] > self.arr[min_child]:
            # heap property is violated, swap elements, update current/children/min_child indices
            self.arr[i], self.arr[min_child] = self.arr[min_child], self.arr[i]
            i, (l_child, r_child) = min_child, self.__children__(min_child)
            min_child = l_child
            if r_child != None and self.arr[r_child] <= self.arr[l_child]:
                min_child = r_child


    def get_min(self): return self.__get_top__()

    def extract_min(self): return self.__extract_top__()

    def insert(self, val): self.__insert__(val)

    def delete(self, i): return self.__delete__(i)


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


    def delete(self, i):
        deleted_val = self.__delete__(i)
        return -deleted_val if deleted_val != None else None


#    def heapify(self, batch: list):  # try to implement maybe...
#        ''' Add list of batch values to the heap in O(len(batch)) time. '''
#        pass
