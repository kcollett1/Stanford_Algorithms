
# this is my quick-and-dirty and verbose implementation of insertion sort and doubly linked
# list for learning purposes. run from command list with $ python insertion_sort.py


def main():
    l_list = doubly_linked_list()  # empty list
    l_list.push_front(9)
    l_list.push_front(19)
    l_list.push_back(1293)
    l_list.push_back(12)
    l_list.push_back(11)
    l_list.push_back(10)
    l_list.push_back(14)
    l_list.push_back(1)
    l_list.push_back(2)
    l_list.push_back(4)
    l_list.push_back(7)
    l_list.push_back(1)
    l_list.push_back(1)
    l_list.push_back(-8)
    print('unsorted:', l_list)

    insertion_sort_linked(l_list)
    print('sorted:', l_list)
   
    reg_list = [19, 9, 1293, 12, 11, 10, 14, 1, 2, 4, 7, 1, 1, -8]
    print('unsorted:', reg_list)

    insertion_sort_reg(reg_list)
    print('sorted:', reg_list)


class node:  # for doubly linked list
    ''' node object to contain value, and next and prev pointers
        for doubly linked list
    '''
    def __init__(self, val=None, nex=None, prv=None):
        self.val = val
        self.nex = nex
        self.prv = prv


class doubly_linked_list:
    ''' made up of a head pointing to a node object and a tail
        pointing to a node object, with methods to insert and remove
        elements at various places in the list. all methods are O(1)
        except for pop(val) to remove a specified value from the list
        and printing list as a string, which are both O(n) worst-case.
        Inserting and removing specified nodes in the insertion sort
        algorithm are O(1) operations though, given you already have a pointer
        to the node(s) you wish to alter, as you are just updating pointers
        instead of shifting elements as you would do in a regular list/array structure
    '''
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    # add value to end of list
    def push_back(self, val):
        add_node = node(val=val, prv=self.tail)
        if not self.tail:  # empty linked list, update head
            self.head = add_node
        else:
            self.tail.nex = add_node

        self.tail = add_node

    # add value to front of list
    def push_front(self, val):
        add_node = node(val=val, nex=self.head)
        if not self.head:  # empty linked list, update tail
            self.tail = add_node
        else:
            self.head.prv = add_node

        self.head = add_node

    # remove and return value from end of list
    def pop_back(self):
        if not self.tail:  # empty list, nothing to remove
            return None

        last_node = self.tail.val
        self.tail = self.tail.prv
        if not self.tail:  # removed only node, update head
            self.head = None
        else:
            self.tail.nex = None

        return last_node

    # remove and return value from front of list
    def pop_front(self):
        if not self.head:  # empty list, nothing to remove
            return None

        top_node = self.head.val
        self.head = self.head.nex
        if not self.head:  # removed only node, update tail
            self.tail = None
        else:  # update prev pointer of new head
            self.head.prv = None

        return top_node

    # remove first instance of a given value if it's in list
    def pop(self, val):
        if not self.head:  # empty list, nothing to remove
            return None

        node = self.head
        while node.val != val and node.nex:
            node = node.nex

        if node.val != val:  # val is not in list, can't remove
            return None

        # else, we found val in list and need to adjust pointers
        if node == self.head:  # trying to remove first element, update head pointer
            self.head = node.nex
        else:  # we're not removing the first element
            node.prv.nex = node.nex

        if node == self.tail:  # trying to remove last element, update tail pointer
            self.tail = node.prv
        else:  # we're not removing the last element
            node.nex.prv = node.prv

        return val  # indicate pop was a success

    # format printing of list
    def __str__(self):
        l = 'head -> '
        node = self.head

        while node:
            l += str(node.val) + ' -> '
            node = node.nex

        return l + 'tail'


def insertion_sort_linked(link_list: doubly_linked_list):
    ''' go through list, inserting curr el into appropriate location in preceding list '''
    node = link_list.head
    if not node:  # empty list, nothing to sort
        return None

    node = node.nex  # first element is already sorted, start with next
    while node:
        nexnode = node.nex

        if node.val >= node.prv.val:  # node already in correct place in list
            node = nexnode
            continue

        # first update prv and nex pointers to remove this node from current place in list
        node.prv.nex = node.nex  # we start from second node so node.prv will always be valid
        if node.nex:  # if not at last node
            node.nex.prv = node.prv
        else:  # removing last element from list, so update tail
            link_list.tail = node.prv

        # now find correct position for this node to be inserted into preceding list elements
        if node.val < link_list.head.val:  # can just put this node at beginning of list
            # update head and appropriate pointers to insert this node in beginning of list
            node.prv = None
            node.nex = link_list.head
            link_list.head.prv = node
            link_list.head = node
        else:  # else, we need to traverse backwards through list to find appropriate place for node
            place_node = node.prv.prv  # node will at least be after first node and before last node
                                       # place_node and place_node.prv and place_node.nex will be valid
            while node.val < place_node.val:
                place_node = place_node.prv

            # we want to insert node in between place_node and place_node.nex, so we
            # update appropriate pointers here. shouldn't need to update tail here ever
            node.prv = place_node
            node.nex = place_node.nex
            place_node.nex.prv = node
            place_node.nex = node

        node = nexnode


def insertion_sort_reg(arr: list):
    ''' go through list, inserting curr el into correct place in preceding list '''
    for i in range(1, len(arr)):
        j = i - 1

        while j > -1 and arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            j -= 1


if __name__ == '__main__':
    main()

    raise SystemExit

