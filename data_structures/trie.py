''' my implementation of a trie data structure '''


class TrieNode:
    def __init__(self, end_of_word=False):
        self.chars = [None for _ in range(26)]
        self.end_of_word = end_of_word


    def set_char(self, c, end_of_word=False):
        ''' Add letter 'c' to this trie node '''
        ind = ord(c.lower()) - 97

        if not self.chars[ind]:  # doesn't exist in this TrieNode yet
            self.chars[ind] = TrieNode()

        if not self.chars[ind].end_of_word and end_of_word:
            self.chars[ind].end_of_word = end_of_word


class Trie:
    def __init__(self):
        self.root = TrieNode()


    def insert(self, key: str):
        ''' Insert key into this trie '''
        if not key:
            return None  # empty string, nothing to insert into Trie

        node = self.root
        for c in key:
            ind = ord(c.lower()) - 97
            if node.chars[ind] != None:
                node = node.chars[ind]
            else:
                node.chars[ind] = TrieNode()
                node = node.chars[ind]

        # added all necessary TrieNodes for key, now set last char to be end_of_word
        node.end_of_word = True


    def search(self, key: str):
        ''' Search for key in this Trie, return true if it's present, false if not '''
        if not key:  # empty string, by default it belongs in every Trie
            return True

        node = self.root
        for c in key:
            ind = ord(c.lower()) - 97
            if not node.chars[ind]:  # key is not in this Trie
                return False
            node = node.chars[ind]

        # found end of key in Trie, return if it is an end_of_word or not
        return node.end_of_word
