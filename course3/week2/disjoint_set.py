
'''
    This is my implementation of a disjoint_set (AKA union-find) data structure
    which uses a lazy rank by union approach with path compression to maintain
    near constant (iterated log) find() and union() operations for the data it
    contains. I.e., for m find & union calls, time complexity is O(m*alpha(n)),
    where n is num of objects in the disjoint_set and alpha is the inverse
    ackermann function (which is ridiculously slowly growing, even slower growing
    than log^* which is the iterated log function).
'''

class DisjointSet:
    def __init__(self, num_objs=0):
        '''
           Each object in our universe initially points to itself as its parent,
           with size 1, since they all start out in their own unconnected sets.
        '''
        self.objs_arr = [[i+1, 0] for i in range(num_objs)]  # [parent obj, RANK of this sub-group]
        self.num_groups = num_objs


    def find(self, obj: int):
        ''' Traverse parent pointers until an object points to itself, this is the leader. '''
        leader = obj
        while self.objs_arr[leader-1][0] != leader:  # runtime of this in worst-case is O(log^*(n))
            leader = self.objs_arr[leader-1][0]

        # update objects traversed on this path to point directly to the leader, path-compression
        o = obj
        while self.objs_arr[o-1][0] != leader:  # additional constant work with same loop run-time
            old_parent = self.objs_arr[o-1][0]
            self.objs_arr[o-1][0] = leader
            o = old_parent

        return leader


    def union(self, obj1: int, obj2: int):
        '''
           AKA merge. given two vertices, merge the two components they belong to,
           updating the parent pointer of the leader of the smaller group. Return new
           leader if we had to merge the groups, else return None if already in same group.
        '''
        l1 = self.find(obj1)  # two find() calls, everything else is O(1), so runtime of union
        l2 = self.find(obj2)  # depends on runtime of the find() calls, O(log(n))

        if l1 == l2:  # already in same group, don't need to update anything
            return None

        # merging two groups into one, decrease num_groups var
        self.num_groups -= 1

        # swap groups to update smaller rank group if necessary
        if self.objs_arr[l1-1][1] > self.objs_arr[l2-1][1]:
            l1,l2 = l2,l1

        # change l1's parent to be l2 and update rank of group 2 if needed
        self.objs_arr[l1-1][0] = l2
        self.objs_arr[l2-1][1] = max(self.objs_arr[l2-1][1], self.objs_arr[l1-1][1] + 1)

        return l2
