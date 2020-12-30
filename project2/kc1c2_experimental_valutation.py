import random

from project1.abtree.abtree_map import ABTreeMap
from project1.currency import Currency
from project2 import kc1c2_coverage

import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np


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


def montecarlo_on_k(L, c1, c2, k1, k2, n_try):
    e_res = []
    o_res = []

    for i in range(k1, k2 + 1):
        print(i, 'of', k2)

        e_min, e_max, e_avg = float('inf'), float('-inf'), 0
        o_min, o_max, o_avg = float('inf'), float('-inf'), 0

        for j in range(n_try):
            # generate random tree
            t = ABTreeMap(2, 8)
            random.shuffle(L)
            for cur_code in L:
                t[cur_code] = Currency(cur_code)

            # compute max, min and avg solution for greedy algorithm
            res = kc1c2_coverage.search(t, i, c1, c2)
            if len(res) < e_min:
                e_min = len(res)
            if len(res) > e_max:
                e_max = len(res)
            e_avg += len(res)

            # compute max, min and avg solution for optimal algorithm
            res = opt_search(t, i, c1, c2)
            if len(res) < o_min:
                o_min = len(res)
            if len(res) > o_max:
                o_max = len(res)
            o_avg += len(res)

        e_avg /= n_try
        o_avg /= n_try

        e_res.append((e_min, e_max, e_avg))
        o_res.append((o_min, o_max, o_avg))

    e_min, e_max, e_avg = zip(*e_res)
    o_min, o_max, o_avg = zip(*o_res)
    e_bound = [e / o for e, o in zip(*(e_max, o_max))]
    print(e_bound)

    _plot_result(e_min, e_max, e_avg, o_min, o_max, o_avg, e_bound, k1, k2 + 1)


def _plot_result(e_min, e_max, e_avg, o_min, o_max, o_avg, e_bound, k1, k2):
    gs = gridspec.GridSpec(3, 1)

    plt.figure()

    plt.suptitle('2-8 Tree with 50 element in [c1, c2]')

    plt.subplot(gs[0, 0])
    plt.gca().set_title('greedy approach - optimal approach - theoretical/experimental bound', fontsize=10)
    plt.ylabel('#node')
    plt.plot(list(range(k1, k2)), e_min, 'b--', label='min')
    plt.plot(list(range(k1, k2)), e_max, 'r--', label='max')
    plt.plot(list(range(k1, k2)), e_avg, 'g', label='avg')
    # Place a legend above this subplot, expanding itself to fully use the given bounding box.
    plt.legend(fontsize=7)

    plt.subplot(gs[1, 0])
    plt.ylabel('#node')
    plt.plot(list(range(k1, k2)), o_min, 'b--', label='min')
    plt.plot(list(range(k1, k2)), o_max, 'r--', label='max')
    plt.plot(list(range(k1, k2)), o_avg, 'g', label='avg')
    # Place a legend above this subplot, expanding itself to fully use the given bounding box.
    plt.legend(fontsize=7)

    x = np.arange(k1, k2, 1)
    y = x / (x // 7 + 1)

    plt.subplot(gs[2, 0])
    plt.xlabel('k')
    plt.ylabel('alpha')
    plt.plot(x, y, 'r', label='theoretical')
    plt.axhline(y=1, color='k', linestyle='--', label='optimal')
    plt.plot(list(range(k1, k2)), e_bound, 'g', label='experimental')
    # Place a legend above this subplot, expanding itself to fully use the given bounding box.
    plt.legend(fontsize=7)

    plt.savefig('exp.png')


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

    k = 50
    c1 = 'IDR'
    c2 = 'PHP'

    montecarlo_on_k(L, c1, c2, 0, k, 10000)
