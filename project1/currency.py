from TdP_collections.map.avl_tree import AVLTreeMap
from project1.double_hashing_hash_map import DoubleHashingHashMap
import re


class Currency:
    """A Currency Class implementation in Python."""

    def __init__(self, c):
        """The constructor of the class takes as input a code 'c' and initializes Code to this value,
        denominations as an empty map, and change as an empty hash map.

        :parameter 'c' The code three capital letters identifying a currency according to the standard ISO 4217.
        :raise 'ValueError' if 'c' do not respect ISO 4217."""
        if not self._validate_iso4217(c):
            raise TypeError('c must respect ISO 4217')
        self._code = c
        self._denomination = AVLTreeMap()
        self._changes = DoubleHashingHashMap()

    # complexity O(2 log N)
    def add_denomination(self, value):
        """Add value in the Denominations map. It raises an exception if value is already present.

        :parameter 'value' is the value to add in Denomination map.
        :raise 'ValueError' if value is already present in the map."""
        if value in self._denomination:  # O(log N)
            raise ValueError('The value is already present')
        self._denomination[value] = 0  # O(log N)

    # complexity O(log N)
    def del_denomination(self, value):
        """Remove value from the Denominations map. It raises an exception if value is not present.

        :parameter 'value' is the value to remove in Denomination map.
        :raise 'ValueError' if value is not present in the map."""
        del (self._denomination[value])  # O(log N)

    # complexity O(2 log N)
    def min_denomination(self, value=None):
        """The parameter value is optional. If it is not given, it returns the minimum denomination (it raises an
        exception if no denomination exists), otherwise it returns the minimum denomination larger than value
        (it raises an exception if no denomination exists larger than value)."""
        if value is None:
            e = self._denomination.find_min()  # O(log N)
            if e is None:
                raise ValueError('no denomination exists')
            return e[0]
        else:
            p = self._denomination.find_position(value)  # O(log N)
            if p.key() < value:
                p = self._denomination.after(p)  # O(log N)
            if p is None:
                raise ValueError('no denomination exists')
            return p.key()

    # complexity O(2 log N)
    def max_denomination(self, value=None):
        """The parameter value is optional. If it is not given, it returns the maximum denomination(it raises an
        exception if no denomination exists), otherwise it returns the maximum denomination smaller than value (it
        raises an exception if no denomination exists larger than value)."""
        if value is None:
            e = self._denomination.find_max()  # O(log N)
            if e is None:
                raise ValueError('no denomination exists')
            return e[0]
        else:
            p = self._denomination.find_position(value)  # O(log N)
            if p.key() > value:
                p = self._denomination.before(p)  # O(log N)
            if p is None:
                raise ValueError('no denomination exists')
            return p.key()

    # complexity O(2 log N)
    def next_denomination(self, value):
        """Return the denomination that follows value, if it exists, None otherwise. If value is not a denomination it
        raises an exception."""
        p = self._denomination.find_position(value)  # O(log N)
        if p is None or p.key() != value:
            raise ValueError('denomination not present')
        n = self._denomination.after(p)  # O(log N)
        return n.key() if n is not None else None

    # complexity O(2 log N)
    def prev_denomination(self, value):
        """Return the denomination that precedes value, if it exists, None otherwise. If value is not a denomination it
        raises an exception."""
        p = self._denomination.find_position(value)  # O(log N)
        if p is None or p.key() != value:
            raise ValueError('denomination not present')
        prev = self._denomination.before(p)  # O(log N)
        return prev.key() if prev is not None else None

    def has_denominations(self):
        """Return true if the Denominations map is not empty."""
        return not self._denomination.is_empty()  # O(1)

    def num_denominations(self):
        """Returns the number of elements in the Denominations map."""
        return len(self._denomination)  # O(1)

    def clear_denominations(self):
        """Remove all elements from the Denominations map."""
        self._denomination.clear()  # O(N)

    def iter_denominations(self, reverse=False):
        """Returns an iterator over the Denominations map. If reverse is false (default value), the iterator must
        iterate from the smaller to the larger denomination, otherwise it must iterate from the larger to the smaller
        denomination."""
        if reverse:
            for k in reversed(self._denomination):
                yield k
        else:
            for k in iter(self._denomination):
                yield k

    def add_change(self, currencycode, change):
        """Add an entry in the Changes hash map, whose key is currencycode and whose value is change. It raises an
        exception if the key currencycode is already present."""
        if currencycode in self._changes:  # O(1) EXPECTED
            raise KeyError('currencycode already exists')
        self._changes[currencycode] = change  # O(1) EXPECTED

    def remove_change(self, currencycode):
        """Remove the entry with key currencycode from the Changes hash map. It raises an exception if the key
        currencycode is not present."""
        del (self._changes[currencycode])  # O(1) EXPECTED

    def update_change(self, currencycode, change):
        """Updates the value associated with key currencycode to change.If the key currencycode does not exist, it will
         be inserted in the Changes hash map."""
        self._changes[currencycode] = change  # O(1) EXPECTED

    def copy(self):
        """Create a new Object Currency whose attributes are equivalent to the ones of the current currency.

        :return: a copy of the object."""
        new = Currency(self._code)
        new._code = self._code
        new._denomination = self._denomination
        new._changes = self._changes
        return new

    def deepcopy(self):
        """Create a new Object Currency whose attributes are equivalent but not identical to the ones of the current
        currency.

        :return: a deepcopy of the object."""
        new = Currency(self._code)
        for d in self._denomination:
            new.add_denomination(d)
        for c in self._changes:
            new.add_change(c, self._changes[c])
        return new

    @staticmethod
    def _validate_iso4217(s):
        pattern = re.compile("^[A-Z]{3}$")
        return pattern.match(s) is not None

    def __str__(self):
        return self._code


    def get_change(self, currencycode):
        return self._changes[currencycode]

if __name__ == '__main__':
    print('---------- Try add_denomination and reverse iter ----------------------')
    cur = Currency('EUR')
    print("cur = Currency('EUR')")
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\ncur.add_denomination(50)')
    cur.add_denomination(50)
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\ncur.add_denomination(10)')
    cur.add_denomination(10)
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\ncur.add_denomination(200)')
    cur.add_denomination(200)
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\ncur.add_denomination(10)')
    try:
        cur.add_denomination(200)
    except ValueError as e:
        print('error:', e)
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\n\n---------- Try del_denomination and iter----------------------')

    print('\ncur.del_denomination(200)')
    try:
        cur.del_denomination(200)
    except ValueError as e:
        print('error:', e)
    for e in cur.iter_denominations():
        print(e, end=' ')
    print()

    print('\ncur.del_denomination(500)')
    try:
        cur.del_denomination(500)
    except KeyError as e:
        print('error:', e)
    for e in cur.iter_denominations():
        print(e, end=' ')
    print()

    print('\n\n---------- Try min_denomination ----------------------')

    print('\ncur.min_denomination(): ', end='')
    try:
        print(cur.min_denomination())
    except ValueError as e:
        print('error:', e)

    print('\ncur.min_denomination(10): ', end='')
    try:
        print(cur.min_denomination(10))
    except ValueError as e:
        print('error:', e)

    print('\ncur.min_denomination(20): ', end='')
    try:
        print(cur.min_denomination(20))
    except ValueError as e:
        print('error:', e)

    print('\ncur.min_denomination(50): ', end='')
    try:
        print(cur.min_denomination(50))
    except ValueError as e:
        print('error:', e)

    print('\ncur.min_denomination(70): ', end='')
    try:
        print(cur.min_denomination(70))
    except ValueError as e:
        print('error:', e)

    print('\n\n---------- Try max_denomination ----------------------')

    print('\ncur.max_denomination(): ', end='')
    try:
        print(cur.max_denomination())
    except ValueError as e:
        print('error:', e)

    print('\ncur.max_denomination(70): ', end='')
    try:
        print(cur.max_denomination(70))
    except ValueError as e:
        print('error:', e)

    print('\ncur.max_denomination(50): ', end='')
    try:
        print(cur.max_denomination(50))
    except ValueError as e:
        print('error:', e)

    print('\ncur.max_denomination(20): ', end='')
    try:
        print(cur.max_denomination(20))
    except ValueError as e:
        print('error:', e)

    print('\ncur.max_denomination(10): ', end='')
    try:
        print(cur.max_denomination(10))
    except ValueError as e:
        print('error:', e)

    print('\ncur.max_denomination(5): ', end='')
    try:
        print(cur.max_denomination(5))
    except ValueError as e:
        print('error:', e)

    print('\n\n---------- Try next_denomination ----------------------')

    print('\ncur.next_denomination(10): ', end='')
    try:
        print(cur.next_denomination(10))
    except ValueError as e:
        print('error:', e)

    print('\ncur.next_denomination(50): ', end='')
    try:
        print(cur.next_denomination(50))
    except ValueError as e:
        print('error:', e)

    print('\ncur.next_denomination(70): ', end='')
    try:
        print(cur.next_denomination(70))
    except ValueError as e:
        print('error:', e)

    print('\n\n---------- Try prev_denomination ----------------------')

    print('\ncur.prev_denomination(10): ', end='')
    try:
        print(cur.prev_denomination(10))
    except ValueError as e:
        print('error:', e)

    print('\ncur.prev_denomination(50): ', end='')
    try:
        print(cur.prev_denomination(50))
    except ValueError as e:
        print('error:', e)

    print('\ncur.prev_denomination(70): ', end='')
    try:
        print(cur.prev_denomination(70))
    except ValueError as e:
        print('error:', e)

    print('\n\n---------- Try has_denomination, num_denomination e clear_denomination----------------------')
    print('\ncur.has_denominations(): {}'.format(cur.has_denominations()))
    print('\ncur.num_denominations(): {}'.format(cur.num_denominations()))
    print('\ncur.clear_denominations()')
    cur.clear_denominations()
    print('\ncur.has_denominations(): {}'.format(cur.has_denominations()))
    print('\ncur.num_denominations(): {}'.format(cur.num_denominations()))

    print('\n\n---------- Try add_change ----------------------')

    print("\ncur.add_change('USD', 1.35): ", end='')
    try:
        cur.add_change('USD', 1.35)
        print('success')
    except KeyError as e:
        print('error:', e)

    print("\ncur.add_change('JBP', 0.49): ", end='')
    try:
        cur.add_change('JBP', 0.49)
        print('success')
    except KeyError as e:
        print('error:', e)

    print("\ncur.add_change('JBP', 0.78): ", end='')
    try:
        cur.add_change('JBP', 0.78)
        print('success')
    except KeyError as e:
        print('error:', e)

    print('\n\n---------- Try update_change ----------------------')

    print("\ncur.update_change('USD', 1.45): ", end='')
    try:
        cur.update_change('USD', 1.45)
        print('success')
    except KeyError as e:
        print('error:', e)

    print("\ncur.update_change('FFP', 1.45): ", end='')
    try:
        cur.update_change('FFP', 1.38)
        print('success')
    except KeyError as e:
        print('error:', e)

    print('\n\n---------- Try remove_change ----------------------')

    # print("\ncur.remove_change('USD'): ", end='')
    # try:
    #     cur.remove_change('USD')
    #     print('success')
    # except KeyError as e:
    #     print('error:', e)
    #
    # print("\ncur.remove_change('BAB'): ", end='')
    # try:
    #     cur.remove_change('BAB')
    #     print('success')
    # except KeyError as e:
    #     print('error:', e)

    print('\n\n---------- Try copy and deepcopy ----------------------')

    print('\ncur.add_denomination(50)')
    cur.add_denomination(50)
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\ncur.add_denomination(10)')
    cur.add_denomination(10)
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\ncur.add_denomination(200)')
    cur.add_denomination(200)
    for e in cur.iter_denominations(True):
        print(e, end=' ')
    print()

    print('\ncopy_cur = cur.copy()')
    copy_cur = cur.copy()
    print('\ndeepcopy_cur = cur.deepcopy()')
    deepcopy_cur = cur.deepcopy()

    print('\ncur is copy_cur: {}'.format(cur is copy_cur))
    print('\ncur is deepcopy_cur: {}'.format(cur is deepcopy_cur))

    print('\ncur._denomination == copy_cur._denomination: {}'.format(cur._denomination == copy_cur._denomination))
    print(
        '\ncur._denomination == deepcopy_cur._denomination: {}'.format(cur._denomination == deepcopy_cur._denomination))
    print('\ncur._denomination is copy_cur._denomination: {}'.format(cur._denomination is copy_cur._denomination))
    print(
        '\ncur._denomination is deepcopy_cur._denomination: {}'.format(cur._denomination is deepcopy_cur._denomination))

    print('\ncur._changes == copy_cur._changes: {}'.format(cur._changes == copy_cur._changes))
    print('\ncur._changes == deepcopy_cur._changes: {}'.format(cur._changes == deepcopy_cur._changes))
    print('\ncur._changes is copy_cur._changes: {}'.format(cur._changes is copy_cur._changes))
    print('\ncur._changes is deepcopy_cur._changes: {}'.format(cur._changes is deepcopy_cur._changes))



    print(cur.get_change('USD'))
