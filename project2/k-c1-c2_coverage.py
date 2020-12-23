import random

from project1.abtree.abtree_map import ABTreeMap
from project1.currency import Currency


def search(T, k, c1, c2):
    """ Algorithm that tries to compute the (k, C1, C2)-cover of T with the minimum number of nodes. The algorithm must
    return None if there are less than k currencies in the tree whose code is between C1 and C2.

    :param T: a a-bTree on which to seek the (k, C1, C2)-cover;
    :param k: the minimum number of du currency of the coverage;
    :param c1: the left end of the set of the (k, C1, C2)-cover currencies;
    :param c2: the right end of the set of the (k, C1, C2)-cover currencies.
    :return a list of node of teh coverage, None if coverage not exist.

    This greedy algorithm runs in a time that is at most

    .. math::
        O(\\frac{n^2}{\\log^2{a}} (b - 1))

    The optimal solution, if the tree has nodes in which all the currencies (or all the necessary ones) belong to them,
    is given by (k/b - 1 rounded up) nodes.
    The solution given, in the worst case, first sees k nodes where there is only one element of the (k, C1, C2)-cover.
    So it returns k nodes in the worst case.

    Therefore, the solution of the algorithm differs from the optimal solution of

    .. math::
        ALG(I) \\ge \\frac{k}{k / (b - 1) \\text{ rounded up}} OPT(I)

    The solution therefore differs a lot when k approaches a multiple of b-1 from the left, while it is much more
    acceptable in the rest of the cases.
    Furthermore, the worst case described above is more likely to occur if C1 and C2 are very far from each other,
    otherwise the probability of obtaining the worst case is much lower.
    """
    solution = []
    currency_found = 0

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
    while currency_found < k and c1 <= p.key(i) <= c2:
        if p not in solution:
            solution.append(p)
            # Check in all elements of the node
            for j in range(len(p.element())):
                if c1 <= p.key(j) <= c2:
                    currency_found += 1
        follow = T.after(p, i)
        if follow is not None:
            p, i = follow
        else:
            break

    return solution if currency_found >= k else None


if __name__ == '__main__':
    l = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF',
         'BMD', 'BND', 'BOB', 'BOV', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHE',
         'CHF', 'CHW', 'CLF', 'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD',
         'EGP', 'ERN', 'ETB', 'FJD', 'FKP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG',
         'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW',
         'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP']

    i1 = random.randint(0, len(l) - 1)
    i2 = random.randint(i1, len(l) - 1)
    c1 = l[i1]
    c2 = l[i2]

    random.shuffle(l)

    t = ABTreeMap(2, 8)
    for cur_code in l:
        t[cur_code] = Currency(cur_code)
    print(t)

    k = random.randint(0, len(l) // 3)

    print('search(t, {}, {}, {}) -> '.format(k, c1, c2), end='')
    print(search(t, k, c1, c2))
