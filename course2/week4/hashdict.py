
'''
   this is a pretty trivial/quick-and-dirty implementation of a hash table/dict
   implemented for a specific input data set, with values chosen
   so there would be very few collisions per bucket. lower n to see behavior
   if there are collisions in the table. mainly just for learning.
'''


from linked_list import *

class HashDict:
    def __init__(self):
        self.num_keys = 0
        #self.n = 500000
        # tried half the space, will roughly double the size of each linekd list
        # slowed down code almost by factor of 2!
        self.n = 20000003  # we have ~2*10^7 values to hash, so choose n to be prime ~2*10^7
                           # but also not too close to a power of 2 or 10
        self.load = 0  # self.num_keys / self.n
        self.data = [None for _ in range(self.n)]  # list of linked lists (using chaining here)


    def __hash_func__(self, key):
        '''
           convert val to int if not already, and send to hash_int.
           currently only support numeric types, boolean, and strings
        '''
        if any((type(key) == i for i in (int, float, complex, bool))):
            return self.__hash_int__(int(key))
        elif type(key) == str:
            run_sum = 0
            mult_const = 314159
            mod_const =  10**11  # max of number in our data set
            for c in key:
                c = ord(c)  # ascii number code
                run_sum = (run_sum * mult_const + c) % mod_const
            return self.__hash_int__(run_sum)
        else:
            raise ValueError('Warning: implementation does not support hashing object of type', type(key), 'yet')


    def __hash_int__(self, key: int):
        '''
           Simply return key shifted by 10^7 (to shift negative bucket
           numbers up and avoid collisions as much as possible) mod num
           of buckets n - quick and dirty hash function implementation
           just to see how performance compares to pythons built-ins.
        '''
        return (key + 10**7) % self.n


    def __update_load__(self):
        if self.n == 0:
            raise ValueError('Warning: number of buckets to hash into can never be 0!!')
        self.load = self.num_keys / self.n


    def insert(self, key, val):
        if self.search(key):  # key/val already in table, don't need to do anything
            return val

        ind = self.__hash_func__(key)
        if self.data[ind] == None:
            self.data[ind] = LinkedList()
        self.data[ind].push_front(key, val)
        self.num_keys += 1
        self.__update_load__()
        return val


    def search(self, key):
        ''' Just a boolean function to test if key is in hash table or not '''
        ind = self.__hash_func__(key)

        if self.data[ind] == None:
            return False

        node = self.data[ind].head
        while node != None and node.key != key:
            node = node.nex

        return True if node != None else False


    def get(self, key):
        ''' Return the actual value if key is in hash table, else return None '''
        ind = self.__hash_func__(key)

        if self.data[ind] == None:
            return False

        node = self.data[ind].head
        while node != None and node.key != key:
            node = node.nex

        return node.val if node != None else None


    def delete(self, key):
        ind = self.__hash_func__(key)

        if self.data[ind] == None:  # key is not in hash table, nothing to delete
            return None

        removed = self.data[ind].remove_key(key)
        if removed != None:  # key was present in the list and it was removed
            self.num_keys -= 1
            self.__update_load__()

        return removed
