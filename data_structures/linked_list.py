''' My implementation of a doubly linked list with head and tail pointer '''


class Node:
    def __init__(self, val=None, nex=None, prv=None):
        self.val = val
        self.nex = nex
        self.prv = prv


class LinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head  # type Node
        self.tail = tail  # tye Node
        self.l = 0  # type int, number of nodes contained in this list object
        node = self.head
        while node != None:
            self.l += 1
            node = node.nex


    def __remove__(self, node):
        '''
           Helper function to remove node, update the previous/next
           node's appropriate pointers, return val of node.
        '''
        self.l -= 1  # decrement length of list

        # update previous node's next pointer (if head, update head)
        if node == self.head:  # removing head, update head pointer
            self.head = node.nex
        else:  # not removing head, update the prv node instead
            node.prv.nex = node.nex

        # update next node's previous pointer (if tail, update tail)
        if node == self.tail:  # removing tail, update tail pointer
            self.tail = node.prv
        else:  # not removing tail, update the next node instead
            node.nex.prv = node.prv

        return node.val # done, return val, successfully removed val from list


    def __find_ith__(self, i):
        '''
           Helper function to find ith element, based on whether i is closer to the
           front of back of list. Return i-th node in list. Guaranteed to be within list.
        '''
        if (i - 1) <= (self.l - i):  # closer to beginning of list, start at head
            traverse = self.head
            ctr = 1
            inc = 1
        else:  # closer to end of list, start at tail
            traverse = self.tail
            ctr = self.l
            inc = -1

        while ctr*inc < i*inc:
            ctr += inc
            if inc > 0:  # going through list from beginning
                traverse = traverse.nex
            else:  # going through list from end
                traverse = traverse.prv

        # found i-th element, return it
        return traverse


    def push_front(self, val):
        '''Add val to beginning of list, return val to indicate success'''
        self.l += 1  # increment length of list
        self.head = Node(val, self.head)

        if self.l > 1:  # wasn't previously empty, update second node's prv pointer
            self.head.nex.prv = self.head
        else:  # was previously empty, update tail pointer
            self.tail = self.head

        return val


    def pop_front(self):
        '''Remove first node in list, return it's value, or None if empty'''
        if not self.head:  # empty list, nothing to remove
            return None

        self.l -= 1  # decrement length of list
        top_val = self.head.val
        self.head = self.head.nex  # update head pointer to point to second node

        if self.l > 0:  # didn't remove last element, update new head's prv pointer
            self.head.prv = None
        else:  # removed last element, update tail pointer
            self.tail = None

        return top_val


    def push_back(self, val):
        '''Add val to end of list, return val to indicate success'''
        self.l += 1  # increment length of list
        self.tail = Node(val=val, nex=None, prv=self.tail)

        if self.l > 1:  # wasn't previously empty, update second to last node's nex pointer
            self.tail.prv.nex = self.tail
        else:  # was previously empty, update head pointer
            self.head = self.tail

        return val


    def pop_back(self):
        '''Remove last node in list, return it's value, or None if empty'''
        if not self.tail:  # empty list, nothing to remove
            return None

        self.l -= 1  # decrement counter
        top_val = self.tail.val
        self.tail = self.tail.prv  # update tail pointer to point to second to last node

        if self.l > 0:  # didn't remove last element, update new tail's nex pointer
            self.tail.nex = None
        else:  # removed last element, update head pointer
            self.head = None

        return top_val


    def remove_val(self, val):
        '''
           Remove node with value val from list. Removes first instance of val
           Return val to indicate success, or None if val is not in list. O(n)
        '''
        traverse = self.head
        while traverse:
            if traverse.val == val: # found node to remove, remove it, and return val
                return self.__remove__(traverse)  # update pointers and return val

            traverse = traverse.nex

        return None  # made it through whole list and did not find val


    def remove_ith(self, i):
        '''
           Remove and return ith (1-bsaed) node from list. If out of range, return
           None. Removes from end of list that element is closer to, but still O(n).
        '''
        if i > self.l:  # out of range, can not remove anything
            return None

        # find i-th element, remove it, and return val
        return self.__remove__(self.__find_ith__(i))
        

    def insert_ith(self, i, val):
        '''
           Insert a node with value val into the i-th (1-based) position in the list.
           If i = length of list + 1, add to end of list, if greater than that, return None.
        '''
        if i > self.l + 1:  # i is out of range, return none, can not add val to list
            return None

        if i == self.l + 1:  # adding val to end of list (potentially to empty list)
            return self.push_back(val)

        if i == 1:  # adding val to front of list (at least one val in list already exists)
            return self.push_front(val)

        #else, we're inserting in between two elements that exist in list
        # find i-th element, insert val before this node (new node takes place of i-th element)
        ith_node = self.__find_ith__(i)
        insert_node = Node(val=val, nex=ith_node, prv=ith_node.prv)
        ith_node.prv, ith_node.prv.nex = insert_node, insert_node
        return val


    def prepend_llist(self, llist):
        '''Add another linked list (of same data type) to the front of this list, return head.'''
        if not llist:  # empty list passed to function, nothing to prepend
            return None

        if not self.tail:  # our list is currently empty, update tail pointer
            self.tail = llist.tail

        # update appropriate pointers
        llist.tail.nex, self.head.prv, self.head = self.head, llist.tail, llist.head

        return self.head

    def append_llist(self, llist):
        '''Add another linked list (of same data type) to the end of this list, return head.'''
        if not llist:  # empty list passed to function, nothing to prepend
            return self.head

        if not self.head:  # our list is currently empty, update head pointer
            self.head = llist.head

        # update appropriate pointers
        llist.head.prv, self.tail.nex, self.tail = self.tail, llist.head, llist.tail

        return self.head


    def len(self):
        return self.l  # return length of list


    def is_empty(self):
        return self.l == 0


    def reset(self):
        '''Warning: empty contents of entire list!!!'''
        self.head, self.tail = None, None
        self.l = 0
