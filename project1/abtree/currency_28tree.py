from project1.abtree.abtree_map import ABTreeMap
from project1.currency import Currency
import random


class Currency28Tree(ABTreeMap):
    """A (2,8)-Tree that memorizes Currency objects, by using their Code as key."""

    def __init__(self):
        """Create a Currency 2-8 Tree Map."""
        super().__init__(2, 8)

    def insert(self, currency):
        """Insert a Currency in the map. If exists, overwrite it.

        :parameter currency: the Currency that you would insert."""
        self.__setitem__(currency._code, currency)

    def delete(self, code):
        """Delete the Currency with the code.

        :parameter code: the code of Currency that you would delete."""
        self.__delitem__(code)

    def search(self, code):
        """Search the Currency with the code.

        :parameter code: the code of Currency that you would get."""
        return self.__getitem__(code)

    def __setitem__(self, key, value):
        if not key == value._code:
            raise ValueError('code must be the corresponding currency code')
        super(Currency28Tree, self).__setitem__(key, value)


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

    random.shuffle(l)

    t = Currency28Tree()

    for e in l:
        t.insert(Currency(e))
        print('---------- Inserting {} ----------'.format(e))
        print(t)

    for e in l:
        t.delete(e)
        print('---------- Deleting {} ----------'.format(e))
        print(t)
