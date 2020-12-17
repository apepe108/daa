from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from TdP_collections.hash_table.map_base import MapBase
import random
import sympy


class DoubleHashingHashMap(ProbeHashMap):
    """Hash map implemented with double hash probing for collision resolution."""
    __slots__ = '_collisions'

    class _Item(MapBase._Item):
        def __str__(self):
            return str(self._key)

        def __repr__(self):
            return str(self)

    def __init__(self, cap=17, p=109345121):
        """Create an empty double-hashing-hash-table map.

        cap     initial table size (default 17)
        p       positive prime used for MAD (default 109345121)
        """
        super().__init__(cap, p)
        self._collisions = 0

    def _find_slot(self, j, k, count_collision=False):
        """Search for key k in bucket at index j.

        Return (success, index) tuple, described as follows:
        If match was found, success is True and index denotes its location.
        If no match found, success is False and index denotes first available slot.
        """
        firstAvail = None
        count = 0
        while True:
            if count == len(self._table):  # if all available element is _AVAIL
                return False, firstAvail  # search has failed
            count += 1
            if self._is_available(j):
                if firstAvail is None:
                    firstAvail = j  # mark this as first avail
                if self._table[j] is None:
                    return False, firstAvail  # search has failed
            elif k == self._table[j]._key:
                return True, j  # found a match
            # keep looking (double hashing)
            j = (j + self._second_hash(k, count_collision and firstAvail is None)) % len(self._table)

    def get_collisions(self):
        """:return: the number of collision in __setitem__ happened in hash table lifetime."""
        return self._collisions

    def _hash_code(self, k):
        hash_value = ord(k[0])
        for i in range(1, len(k)):
            hash_value += ord(k[i]) + 33 * hash_value
        return hash_value

    def _hash_function(self, k):
        return round((self._hash_code(k) * self._scale + self._shift) % self._prime % len(self._table), 0)

    def _second_hash(self, k, count_collision=False):
        if count_collision:
            self._collisions += 1
        q = sympy.prevprime(len(self._table) - 1)
        return q - (self._hash_code(k) % q)

    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)  # subroutine maintains self._n
        if self._n > round(len(self._table) * 0.49, 0):  # keep load factor <= 0.5
            self._resize(sympy.prevprime(2 * len(self._table)))  # number 2^x - 1 is often prime

    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)  # may raise KeyError
        self._n -= 1
        if self._n < round(len(self._table) * 0.21, 0) and len(self._table) != 17:  # subroutine maintains self._n
            new_c = sympy.nextprime(len(self._table) // 2)  # keep load factor >= 0.2
            if new_c < 17:
                new_c = 17
            self._resize(new_c)

    def _resize(self, c):
        """Resize bucket array to capacity c and rehash all items."""
        old = list(self.items())  # use iteration to record existing items
        self._table = c * [None]  # then reset table to desired capacity
        self._n = 0  # n recomputed during subsequent adds
        for (k, v) in old:
            j = self._hash_function(k)
            self._bucket_setitem(j, k, v, False)  # reinsert old key-value pair

    def _bucket_setitem(self, j, k, v, count_collisions=True):
        found, s = self._find_slot(j, k, count_collisions)
        if not found:
            self._table[s] = self._Item(k, v)  # insert new item
            self._n += 1  # size has increased
        else:
            self._table[s]._value = v  # overwrite existing

    def get_load_factor(self):
        return self._n / len(self._table)


if __name__ == '__main__':
    l = ['EUR', 'USD', 'GBP', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT',
         'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BOV', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHE',
         'CHF', 'CHW', 'CLF', 'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD',
         'EGP', 'ERN', 'ETB', 'FJD', 'FKP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG',
         'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW',
         'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP',
         'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB',
         'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK',
         'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY',
         'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USN', 'UYI', 'UYU', 'UYW', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG',
         'XAU', 'XBA', 'XBB', 'XBC', 'XBD', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'XSU', 'XTS', 'XUA', 'XXX', 'YER',
         'ZAR', 'ZMW', 'ZWL']

    def _gen_iso4217():
        for i in range(ord('A'), ord('Z') + 1):
            for j in range(ord('A'), ord('Z') + 1):
                for k in range(ord('A'), ord('Z') + 1):
                    yield chr(i) + chr(j) + chr(k)

    d = DoubleHashingHashMap()
    # l = list(_gen_iso4217())
    random.shuffle(l)
    i = 0
    j = 0
    while i < 70 or j < 30:
        ins = random.random() < 0.7
        if not j < 30:
            ins = True
        if not i < 70:
            ins = False
        if i <= j or ins:
            i += 1
            print('\n\n------- Inserting {}, n. {} --------------'.format(l[i], i))
            d[l[i]] = 0
        else:
            j += 1
            print('\n\n------- Deleting {}, n. {} --------------'.format(l[j], j))
            del (d[l[j]])
        print('Collisions:', d.get_collisions())
        print('Size: {}'.format(len(d)))
        print('Load factor:', d.get_load_factor())
