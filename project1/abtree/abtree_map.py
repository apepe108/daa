from TdP_collections.map.map_base import MapBase
from project1.abtree.abtree import ABTree
import random


class ABTreeMap(ABTree, MapBase):
    # -------------- Nested Class Item --------------
    class _Item(MapBase._Item):
        def __str__(self):
            return str(self._key) + ': ' + str(self._value)

        def __repr__(self):
            return str(self)

    # -------------- Nested Class Position --------------
    class ABPosition(ABTree.ABPosition):
        def key(self, i):
            """Return key of map's key-value pair."""
            return self.element()[i]._key

        def value(self, i):
            """Return value of map's key-value pair."""
            return self.element()[i]._value

        def __str__(self):
            return str(self.element())

        def __repr__(self):
            return str(self)

    # -------- ABMap Method ---------------------------------

    def __getitem__(self, key):
        """Search the value for the key.

        :parameter key: Key to search for.
        :return: the value associated at the key
        :raise KeyError if the code does not exist."""
        if self.is_empty():
            raise KeyError('not found')
        p, i = self._subtree_search(self.root(), key)
        if i < len(p.element()) and p.key(i) == key:
            return p.value(i)
        else:
            raise KeyError('not found')

    def search(self, key):
        """Search the value for the key. Return the Position and teh index where is the element, otherwise the
         nearest neighbor.

        :parameter key: Key to search for.
        :return: the value associated at the key"""
        p, i = self._subtree_search(self.root(), key)
        if i < len(p.element()):
            return p, i
        else:
            return p, i - 1

    def _subtree_search(self, p, e):
        found, i = self._list_search(p.element(), e)
        if self.is_leaf(p) or found:
            return p, i
        else:
            return self._subtree_search(self.child(p, i), e)

    def find_min(self):
        """Find the minimum in the whole tree"""
        p, i = self._subtree_first_position(self.root())
        return p.key(i), p.value(i)

    def find_max(self):
        """Find the maximum in the whole tree."""
        p, i = self._subtree_last_position(self.root())
        return p.key(i), p.value(i)

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty():
            p, i = self._add_root(self._Item(k, v))
        else:
            p, i = self._subtree_search(self.root(), k)
            if i < len(p.element()) and p.key(i) == k:
                p.element()[i]._value = v  # replace existing item's value
                return
            else:
                self._add_element(p, i, self._Item(k, v))

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        if self.is_empty():
            raise KeyError('not found')
        p, i = self._subtree_search(self.root(), k)
        if i < len(p.element()) and p.key(i) == k:
            self._delete_element(p, i)
        else:
            raise KeyError('not found')

    @staticmethod
    def _list_search(l, key):
        """Binary search algorithm for searching within an ordered list.

        :parameter l: the list of _Item.
        :parameter key: _Item to search.
        :returns: True if value is in l, else False.
        :returns: The index of the element if is present, else the index of the bigger element. If value is the last
        element return an index out of range."""
        inf = 0
        sup = len(l) - 1
        median = None
        found = False
        while (inf <= sup) and (not found):
            median = (inf + sup) // 2
            if l[median]._key < key:
                inf = median + 1
            elif l[median]._key == key:
                found = True
            else:
                sup = median - 1
        return found, median + 1 if l[median]._key < key else median


if __name__ == '__main__':
    t = ABTreeMap(2, 8)

    l = list(range(1, 150, 2))
    random.shuffle(l)

    for e in l:
        t[e] = e
        print('---------- Inserting {} ----------'.format(e))
        print(t)

    print('---------- Inorder visit --------------')
    for e in t.inorder():
        print(e, end=' ')
    print('\n')

    print('----------- Value of 55 ----------------')
    print(t[55], '\n')

    for e in l:
        del (t[e])
        print('---------- Deleting {} ----------'.format(e))
        print(t)
