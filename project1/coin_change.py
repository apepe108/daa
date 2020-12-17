from TdP_collections.priority_queue.heap_priority_queue import HeapPriorityQueue
from project1.currency import Currency


# Recursive solution for change problem
# Required time: O(m*2^n)
#     m: #denominations
#     n: value/0.01

def change_recurs(value, currency, canonical=False):
    """The function return the minimum number of coins of the given currency that sums up to the given value.

    E.g.: on input 12,85 and EUR currency, the function must return 6 corresponding to 10+2+0,50+0,20+0,10+0,5.
    :param value: the value of you want get the minimum number of coins.
    :param currency: the currency object to use to calculate the minimum number of coins.
    :param canonical: True if the denomination is canonical, False if is not. NOTE: the time complexity is linear if
    the denomination is canonical, exponential if not. You can use canonical=True and get a list of cash for give the
    change, but this is not the optimal solution.
    :return: the minimum number of coins of the given currency that sums up to the given value and the list of the
    corresponding coins.
    :raise ValueError if is not possible give the change with the given currency."""
    p = HeapPriorityQueue()
    _change_recursion(value, currency, p, canonical=canonical)
    if not p.is_empty():
        return p.min()
    else:
        raise ValueError('can not give this change')


def _change_recursion(value, currency, pq, n_of_cash=0, cash_list=None, canonical=False):
    if cash_list is None:
        cash_list = []
    # base case
    if value == 0:
        pq.add(n_of_cash, cash_list)
        return
    # recurs
    for den in currency.iter_denominations(reverse=True):
        if den > value:
            continue
        support_list = cash_list[:]
        support_list.append(den)
        _change_recursion(round(value - den, 2), currency, pq, n_of_cash + 1, support_list, canonical)
        if canonical:
            return


#   Dynamic solution for change problem
#   Time complexity: O(m*n)
#       m: #denomination
#       n: value/0.01

def change(value, currency):
    """The function return the minimum number of coins of the given currency that sums up to the given value.

    E.g.: on input 12,85 and EUR currency, the function must return 6 corresponding to 10+2+0,50+0,20+0,10+0,5.
    :param value: the value of you want get the minimum number of coins.
    :param currency: the currency object to use to calculate the minimum number of coins.
    :return: the minimum number of coins of the given currency that sums up to the given value and the list of the
    corresponding coins.
    :raise ValueError if is not possible give the change with the given currency."""
    solution = {0: (0, [])}
    # min_denomination = currency.min_denomination()[0]
    current_value = 0
    while True:
        current_value = round(current_value + 0.01, 2)
        p = HeapPriorityQueue()
        _change_dynamic(current_value, currency, p, solution)
        if not p.is_empty():
            solution[current_value] = p.min()
        else:
            continue
        if current_value >= value:
            break
    if value in solution:
        return solution[value]
    else:
        raise ValueError('can not give this change')


def _change_dynamic(value, currency, pq, solution):
    for den in currency.iter_denominations(reverse=True):
        if den > value:
            continue
        new_value = round(value - den, 2)
        if new_value not in solution:
            continue
        s = solution[new_value]
        pq.add(1 + s[0], s[1] + [den])


if __name__ == '__main__':
    # -------------------  NO RECURSIVE --------------------------
    print('TEST WITH SAVING SOLUTION APPROACH')
    c = Currency('EUR')
    # c.add_denomination(0.01)
    # c.add_denomination(0.02)
    c.add_denomination(0.05)
    c.add_denomination(0.1)
    c.add_denomination(0.2)
    c.add_denomination(0.5)
    c.add_denomination(1)
    c.add_denomination(2)
    c.add_denomination(5)
    c.add_denomination(10)
    c.add_denomination(20)
    c.add_denomination(50)
    c.add_denomination(100)
    c.add_denomination(200)
    c.add_denomination(500)
    print('\n\n--------------- Conventional currency -----------------------')
    print('List of denomination:', [x for x in c.iter_denominations()])
    v = 12.35
    try:
        print('change({}, {}): {}'.format(v, c, change(v, c)))
    except ValueError as e:
        print('change({}, {}): {}'.format(v, c, e))

    v = 12.38
    try:
        print('change({}, {}): {}'.format(v, c, change(v, c)))
    except ValueError as e:
        print('change({}, {}): {}'.format(v, c, e))

    ncc = Currency('CNC')
    ncc.add_denomination(0.01)
    ncc.add_denomination(0.03)
    ncc.add_denomination(0.04)
    print('\n\n--------------- Non conventional currency -----------------------')
    print('List of denomination:', [x for x in ncc.iter_denominations()])
    v = 0.06
    try:
        print('change({}, {}): {}'.format(v, ncc, change(v, ncc)))
    except ValueError as e:
        print('change({}, {}): {}'.format(v, ncc, e))

    pro = Currency('AAA')
    # pro.add_denomination(0.01)
    pro.add_denomination(0.05)
    pro.add_denomination(0.08)
    # pro.add_denomination(0.1)
    print('\n\n--------------- Currency with lowest cash less than 0.01 ---------------')
    print('List of denomination:', [x for x in pro.iter_denominations()])
    v = 0.45
    try:
        print('change({}, {}): {}'.format(v, pro, change(v, pro)))
    except ValueError as e:
        print('change({}, {}): {}'.format(v, pro, e))

    # -------------------  RECURSIVE  --------------------------
    print('\n\n\nTEST WITH RECURSIVE APPROACH')
    print('(trying with small values because temporal complexity is very high)')

    c = Currency('EUR')
    # c.add_denomination(0.01)
    # c.add_denomination(0.02)
    c.add_denomination(0.05)
    c.add_denomination(0.1)
    c.add_denomination(0.2)
    c.add_denomination(0.5)

    print('\n\n--------------- Conventional currency -----------------------')
    print('List of denomination:', [x for x in c.iter_denominations()])
    v = .55
    try:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, c, change_recurs(v, c)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, c, e))
    try:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, c, change_recurs(v, c, canonical=True)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, c, e))

    v = .58
    try:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, c, change_recurs(v, c)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, c, e))
    try:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, c, change_recurs(v, c, canonical=True)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, c, e))

    ncc = Currency('CNC')
    ncc.add_denomination(0.01)
    ncc.add_denomination(0.03)
    ncc.add_denomination(0.04)
    print('\n\n--------------- Non conventional currency -----------------------')
    print('List of denomination:', [x for x in ncc.iter_denominations()])
    v = 0.06
    try:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, ncc, change_recurs(v, ncc)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, ncc, e))
    try:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, ncc, change_recurs(v, ncc, canonical=True)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, ncc, e))

    pro = Currency('AAA')
    # pro.add_denomination(0.01)
    pro.add_denomination(0.05)
    pro.add_denomination(0.08)
    # pro.add_denomination(0.1)
    print('\n\n--------------- Currency with lowest cash less than 0.01 ---------------')
    print('List of denomination:', [x for x in pro.iter_denominations()])
    v = 0.45
    try:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, pro, change_recurs(v, pro)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, pro, e))
    try:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, pro, change_recurs(v, pro, canonical=True)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, pro, e))

    v = 0.44
    try:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, pro, change_recurs(v, pro)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=False): {}'.format(v, pro, e))
    try:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, pro, change_recurs(v, pro, canonical=True)))
    except ValueError as e:
        print('change_recurs({}, {}, canonical=True): {}'.format(v, pro, e))
