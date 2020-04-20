
'''
    my implementation of a binary search tree, not balanced
'''


class BinarySearchNode:
    def __init__(self, val=None, parent=None, left=None, right=None):
        self.val = val
        self.parent = parent
        self.left = left
        self.right = right
        self.size = 1
        if self.left != None:
            self.size += self.left.size
        if self.right != None:
            self.size += self.right.size


class BinarySearchTree:
    def __init__(self, root=None):
        self.root = root


    def search(self, val):
        '''
           Given a val, return node with first instance of this val.
           If not in tree, return None.
        '''
        node = self.root

        while node != None:
            if node.val == val:
                return node  # found val, return node containing val
            elif node.val > val:
                node = node.left
            else:
                node = node.right

        return None  # val is not in this tree, return None


    def insert(self, val):
        node = self.root

        if node == None:  # inserting into an empty tree
            self.root = BinarySearchNode(val=val)
            return val  # indicate success

        while node != None:  # may need to keep checking any children
            node.size += 1  # our val will be inserted *somewhere* underneath this node
            if node.val >= val:
                if node.left == None:  # we found the node to insert our val under
                    break
                # else keep traversing
                node = node.left
            else:
                if node.right == None:  # we found the node to insert our val under
                    break
                # else keep traversing
                node = node.right

        add_node = BinarySearchNode(val=val, parent=node)
        if node.val >= val:  # insert val to node's left pointer
            node.left = add_node
        else:  # insert val to node's right pointer
            node.right = add_node

        return val


    def min(self, node=None):
        if node == None:
            node = self.root  # if no node passed, find min of whole tree

        if node == None:  # tree is empty, can't find a min
            return None

        while node.left != None:
            node = node.left

        return node.val


    def max(self, node=None):
        if node == None:
            node = self.root  # if no node passed, find min of whole tree

        if node == None:  # tree is empty, can't find a max
            return None

        while node.right != None:
            node = node.right

        return node.val


    def in_order_traversal(self):
        '''
           Operate on vals recursively in order from smallest to largest.
           Here we print vals, but replace print with whatever operation
           you are interested in performing.
        '''
        if self.root != None:
            self.__in_order__(self.root)  # recursive function


    def __in_order__(self, node):
        if node != None:  # reached end of a path, done recursing this path
            self.__in_order__(node.left)
            print(node.val, end=' ')
            self.__in_order__(node.right)


    def pre_order_traversal(self, node):
        '''
           Here we print vals, but replace print with
           whatever operation you are interested in performing.
        '''
        if node != None:  # reached end of a path, done recursing this path
            print(node.val)
            self.pre_order_traversal(node.left)
            self.pre_order_traversal(node.right)


    def post_order_traversal(self, node):
        '''
           Here we print vals, but replace print with
           whatever operation you are interested in performing.
        '''
        if node != None:  # reached end of a path, done recursing this path
            self.post_order_traversal(node.left)
            self.post_order_traversal(node.right)
            print(node.val)


    def pred(self, val):  # need to test
        '''
           Find predecessor of a node with a given val. If val is ambiguous in tree,
           it returns the first distinct predecessor present in the tree. If val
           is either not present in tree or is the minimum, return None.
        '''
        node = self.search(val)
        if node == None:  # val is not in tree, no predecessor
            return None

        if node.left != None:
            return self.max(node.left)
        
        node = node.parent
        while node != None and node.val >= val:
            node = node.parent

        if node == None:  # val we searched for is actually the minimum in this tree
            return None

        return node.val


    def succ(self, val):  # need to test
        '''
           Find succcessor of a node with a given val. If val is ambiguous in tree,
           it returns the first distinct successor present in the tree. If val is
           either not present in tree or is the maximum, return None.
        '''
        node = self.search(val)
        if node == None:  # val is not in tree, no successor
            return None

        if node.right != None:
            return self.min(node.right)
        
        node = node.parent
        while node != None and node.val <= val:
            node = node.parent

        if node == None:  # val we searched for is actually the maximum in this tree
            return None

        return node.val


    def delete(self, val):  # FIXME test for correctness
        ''' Delete the given val if it exists from this tree. '''
        node = self.search(val)
        if node == None:  # val is not in tree, don't need to delete anything
            return None

        # update sizes of all nodes above node
        node_change = node.parent
        while node_change != None:
            node_change.size -= 1
            node_change = node_change.parent

        if node.left == None and node.right == None:  # node has no children
            # check if we're deleting the last node from the tree
            if node.parent == None:
                self.root = None
            elif node.parent.right == node: # just delete pointer to this node from parent
                node.parent.right = None
            else:
                node.parent.left = None
            return val  # to indicate success

        if node.left == None or node.right == None:  # only has one child
            # replace node with only child, updating appropriate pointers
            child = node.left if node.left != None else node.right
            child.parent = node.parent  # could be None
            if node.parent == None:  # if deleting the root element, update root pointer
                self.root = child
            elif node.parent.right == node:
                node.parent.right = child
            else:
                node.parent.left = child
            return val  # to indicate success

        # node we're trying to delete has two children, replace with max from left
        # subtree, i.e. it's predecessor :) many cases can arise in this situation
        # the outline to dealing with this situation is as follows:
        # remove pointer from this node's parent to itself and replace with max_left's
        # left child (could be None) (by definition it will definitely not have a right
        # child but may still have a left child), which will always be the parents
        # right child if the node is not directly under the node we're removing
        # finally, reset this nodes parent's child pointer
        # both children's parent pointers (we're in the case where node has TWO children)
        # and all 3 of this nodes pointers

        # get the max node from left subtree
        max_left = self.max(node.left)
        # update sizes of all nodes below (and including) node and above max_left (inclusive)
        node_change = max_left.parent
        while node_change != None and node_change != node:
            # node_change should never equal None, included just in case...
            node_change.size -= 1
            node_change = node_change.parent
        # update max_left node's size
        max_left.size = node.size - 1


        # remove node from the tree: set parent to point to left child, and vice versa
        if max_left.left != None:
            max_left.left.parent = max_left.parent

        if max_left.parent.right == max_left:
            max_left.parent.right = max_left.left  # could be None
        else: # need to update this to correctly specify this nodes new children later
            max_left.parent.left = max_left.left  # could be None

        # put this node back in tree in the spot we are removing node from
        # set parent to point to this node, and vice versa
        max_left.parent = node.parent  # could be None if we're removing root node

        if max_left.parent == None:  # if removing root, update root pointer
            self.root = max_left
        elif max_left.parent.right == node:
            max_left.parent.right = max_left
        else:
            max_left.parent.left = max_left

        # finally, update this nodes new children and the chidlrens new parent
        max_left.left = node.left
        max_left.left.parent = max_left
        max_left.right = node.right
        max_left.right.parent = max_left

        return val  # to indicate success


    def select(self, i):
        '''
           Find and return the i-th smallest value in this tree. If i is larger
           then the number of nodes in the tree, return None.
        '''
        if i < 1 or self.root == None or i > self.root.size:
            # tree is empty or doesn't have enough elements, or index is out of range (must be > 0)
            return None

        node = self.root
        smaller = node.left.size if node.left != None else 0

        while smaller != i - 1:
            if smaller < i:  # move to right subtree
                i -= (smaller + 1)
                node = node.right  # by initial checks, we should be guaranteed to find a node in the tree
            else:  # move to left subtree
                node = node.left  # again by initial checks, should be guaranteed this node exists
            # update smaller val at this new node
            smaller = node.left.size if node.left != None else 0

        # found correct node, return it's val
        return node.val

    def rank(self, val):  # FIXME test for correctness...
        '''
           Find and return the rank of a given val, i.e. the number of nodes in the
           tree with vals less than or equal to val. Min = 0, Max = number of nodes.
        '''
        node = self.root
        smaller = 0
        while node != None and node.val != val:
            if node.val < val:
                node = node.right
                smaller += 1
                if node.left != None:
                    smaller += node.left.size
            else:
                node = node.left

        if node != None and node.left != None:
            smaller += node.left.size

        return smaller


    def get_median(self):
        return self.select(self.root.size//2 + self.root.size%2) if self.root != None else None
