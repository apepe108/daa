import random

from project1.abtree.abtree_map import ABTreeMap
from project1.currency import Currency
from project2 import kc1c2_coverage


def opt_search(T, k, c1, c2):
    """ Algorithm that to compute the (k, C1, C2)-cover of T with the minimum number of nodes. The algorithm must
    return None if there are less than k currencies in the tree whose code is between C1 and C2."""
    solution = []

    # Look for c1, or a neighbor if that doesn't exist
    follow = T.search(c1)
    if follow is not None:
        p, i = follow
    else:
        return None

    # If the neighbor is before c1, he moves forward
    if p.key(i) < c1:
        follow = T.after(p, i)
        if follow is not None:
            p, i = follow
        else:
            return None

    # Search in subsequent currencies until you reach coverage of at least k
    while c1 <= p.key(i) <= c2:
        currency_found = 0
        if p not in solution:
            # Check in all elements of the node
            for j in range(len(p.element())):
                if c1 <= p.key(j) <= c2:
                    currency_found += 1
            solution.append((currency_found, p))
        follow = T.after(p, i)
        if follow is not None:
            p, i = follow
        else:
            break

    # sort solution
    solution.sort(key=_by_key, reverse=True)

    total = 0
    for i in range(len(solution)):
        total += solution[i][0]
        if total >= k:
            break

    _, solution = zip(*solution)

    return solution[:i + 1] if total >= k else None


def _by_key(e):
    return e[0]


def _montecarlo(T, c1, c2, k, n_try=1000):
    e_min = float('+inf')
    e_max = float('-inf')
    e_avg = 0

    o_min = float('+inf')
    o_max = float('-inf')
    o_avg = 0

    for i in range(n_try):
        o_sol = opt_search(T, k, c1, c2)
        e_sol = kc1c2_coverage.search(T, k, c1, c2)

        if len(o_sol) < o_min:
            o_min = len(o_sol)
        if len(o_sol) > o_max:
            o_max = len(o_sol)
        o_avg += len(o_sol)

        if len(e_sol) < e_min:
            e_min = len(e_sol)
        if len(e_sol) > e_max:
            e_max = len(e_sol)
        e_avg += len(e_sol)

    o_avg = o_avg / n_try
    e_avg = e_avg / n_try

    return o_min, o_max, o_avg, e_min, e_max, e_avg


if __name__ == '__main__':
    L = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF',
         'BMD', 'BND', 'BOB', 'BOV', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHE', 'CHF', 'CHW', 'CLF',
         'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB',
         'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF',
         'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD',
         'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU',
         'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN',
         'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD',
         'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD',
         'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'USN', 'UYI', 'UYU', 'UYW', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG',
         'XAU', 'XBA', 'XBB', 'XBC', 'XBD', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'XSU', 'XTS', 'XUA', 'XXX', 'YER',
         'ZAR', 'ZMW', 'ZWL']

    i1 = random.randint(0, len(L) - 1)
    i2 = random.randint(i1, len(L) - 1)
    c1 = L[i1]
    c2 = L[i2]

    random.shuffle(L)

    t = ABTreeMap(2, 8)
    for cur_code in L:
        t[cur_code] = Currency(cur_code)
    print(t)

    k = random.randint(0, len(L) // 3)

    print('opt_search(t, {}, {}, {}) -> '.format(k, c1, c2), end='')
    print(opt_search(t, k, c1, c2))

    print('search(t, {}, {}, {}) -> '.format(k, c1, c2), end='')
    print(kc1c2_coverage.search(t, k, c1, c2))
