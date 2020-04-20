
'''
    This is my implementation of a disjoint_set (AKA union-find)
    data structure which uses a lazy rank by union approach to
    maintain near constant find() and union() operations for the
    data it contains.

'''

class disjoint_set:
    def __init__(self, num_objs=0):
        '''
           Each object in our universe initially points to itself as its parent,
           with size 1, since they all start out in their own unconnected sets.
        '''
        self.objs_arr = [[i+1, 0] for i in range(num_objs)]  # [parent obj, RANK of this sub-group]


    def find(self, obj: int):
        ''' Traverse parent pointers until an object points to itself, this is the leader. '''
        leader = obj
        while self.objs_arr[leader-1][0] != leader:  # runtime of this in worst-case is O(log(n))
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

        # swap groups to update smaller rank group if necessary
        if self.objs_arr[l1-1][1] > self.objs_arr[l2-1][1]:
            l1,l2 = l2,l1

        # change l1's parent to be l2 and update rank of group 2 if needed
        self.objs_arr[l1-1][0] = l2
        self.objs_arr[l2-1][1] = max(self.objs_arr[l2-1][1], self.objs_arr[l1-1][1] + 1)

        return l2
