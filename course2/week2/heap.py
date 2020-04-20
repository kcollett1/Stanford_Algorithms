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
        self.pos = {}  # dict of {element in heap: index in heap}, added for O(1) find
                       # (which allows for O(log(n)) delete) NOTE: in this specific implementation
                       # I am altering the pos key to be the vertex number instead of the Vert_Path object

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
        top_vert = top_val.vert  # this is specific to dijkstra's shortest path on graph algo
        last_val = self.arr[self.size - 1]
        last_vert = last_val.vert  # this is specific to dijkstra's shortest path on graph algo
        self.arr[0] = last_val
        self.pos[last_vert] = 0  # update index of last_val which was replaced to be at index 0
        self.arr.pop()  # O(1) with pythons list structure
        del self.pos[top_vert]  # remove top_val from pos dict since we removed it from heap
        self.size -= 1

        # finally, sift down the (new) first element, and return top value which has been removed
        self.__sift_down__(0)  # O(log(n))
        return top_val


    def __insert__(self, val):
        ''' Insert a val into the heap, increment size of heap by 1. O(log(n)) '''
        self.arr.append(val)  # amortized O(1) with pythons list structure
        self.pos[val.vert] = self.size  # add val to pos dict pointing to last index of heap
        self.size += 1
        self.__sift_up__(self.size - 1)  # sift up element we just added, O(log(n))


    def __delete__(self, vert):
        ''' Delete and return val from the heap if it exists. If not, return None. O(log(n))'''
        ind = self.find(vert)  # O(1)
        if ind == None:
            return None

        # replace this element with last element, remove last element from heap, decrement size
        self.size -= 1
        this_val = self.arr[ind]
        last_val = self.arr[self.size]
        last_vert = last_val.vert  # this is specific to dijkstra's shortest path on graph algo
        self.arr[ind] = last_val
        self.pos[last_vert] = ind  # update last_val index in pos dict to ind we just placed it at
        self.arr.pop()  # O(1) with pythons list structure
        del self.pos[vert]  # and remove val from pos dict since we just removed it from the heap

        if ind == self.size:  # we removed the last element, we're done
            return this_val

        # try sifting up and down if needed; if it's not, nothing will change, so no harm done
        self.__sift_up__(ind)    # heap property only violated at most in one direction, only one
        self.__sift_down__(ind)  # will actually do any work, at worst O(1*log(n)) runtime.

        # return extracted val to indicate success
        return this_val


    def find(self, vert):
        ''' Find and return index of val in heap if it exists. If not, return None. O(1) '''
        if vert not in self.pos:
            return None
        else:
            return self.pos[vert]


    def update_len(self, vert, new_len):
        '''
           This is specific to dijkstra's shortest path on graph algo, given a vertex,
           change it's path length and then sift up and down to put it in correct position
           in heap. This is I think a more efficient work-around in this specific instance
           instead of deleting element from heap and inserting new element with diff path length.
        '''
        ind = self.find(vert)
        if ind == None:  # vert is not in heap, no value to change
            return None

        # vert is in heap, check if we need to change it's path len, sift up/down as needed
        curr_path_len = self.arr[ind].path_len
        if new_len >= curr_path_len:
            return None

        self.arr[ind].path_len = new_len
        self.__sift_up__(ind)
        self.__sift_down__(ind)
        return new_len  # to indicate that we did change the value


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
            self.pos[self.arr[parent].vert] = i  # specific to dijkstra's shortest path on graph algo
            self.pos[self.arr[i].vert] = parent  # specific to dijkstra's shortest path on graph algo
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
            self.pos[self.arr[min_child].vert] = i  # specific to dijkstra's shortest path on graph algo
            self.pos[self.arr[i].vert] = min_child  # specific to dijkstra's shortest path on graph algo
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
