''' my implementation of a queue class '''


class QueueNode:  # use to hold whatever type of data you're interested in using
    def __init__(self, val=None, nex=None, prv=None):
        self.val = val  # of type whatever data you're interested in using
        self.nex = nex  # of type QueueNode
        self.prv = prv  # of type QueueNode


class Queue:
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
        '''Warning: empty entire queue!!!'''
        self.size = 0
        self.head = None
        self.tail = None
