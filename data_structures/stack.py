''' my implementation of a stack class '''


class Node:  # hold whatever type of data you're using in your stack
    def __init__(self, val=None, prv=None):
        self.val = val  # of type whatever data you're interested in using
        self.prv = prv  # of type Node


class Stack:
    def __init__(self, val=None):
        if val:  # initializing stack with a value
            self.size = 1
            self.head = Node(val=val, prv=None)
        else:  # initialize empty stack
            self.size = 0
            self.head = None


    def top(self):
        '''Return top value in stack. If empty, return None'''
        if self.size == 0:
            return None
        else:
            return self.head.val


    def pop(self):
        '''Remove and return the top value in the stack. If empty, return None'''
        if self.size == 0:
            return None
        else:
            top_val = self.head.val  # save top val to return after removing
            self.size -= 1  # decrement size of stack
            self.head = self.head.prv  # point top of stack to most previously added node
            return top_val  # done removing, return removed value


    def push(self, val):
        '''Add node with value val to top of stack. Return val to indicate success'''
        self.size += 1
        self.head = Node(val=val, prv=self.head)
        return val


    def len(self):
        return self.size


    def is_empty(self):
        return self.size == 0


    def reset(self):
        '''Warning: empty entire contents of stack!!!'''
        self.size = 0
        self.head = None
        return 1
