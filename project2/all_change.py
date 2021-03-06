from typing import List, Union

from project1.currency import Currency
import sys


def _float2int(x: float) -> int:
    """ Convert float value with 2 decimal points to convenient notation in cents, with no CPU calculation error.

    :param x: the float value;
    :return: the values in cents."""
    return round(x * 100)


def _int2float(x: int) -> float:
    """ Convert cents value to float value with 2 decimal points, with no CPU calculation error.

    :param x: the values in cents;
    :return: the float value."""
    return round(x / 100, 2)


def all_change_number_only(cur: Currency, r: float, only_cents=True) -> int:
    """This function, given in input a Currency Object and a float number r with at most two decimal points, returns all
    possible way to change r value with the currency c.
    (E.g., for a currency whose denominations are {0.1, 0.2, 0.5} and r=0.6, the algorithm must return 5, and the five
    different possible ways that can be used for changing 0.6, i.e., 0.5+0.1, 3*0.2, 0.2+4*0.1, 6*0.1.)

    :param cur: the currency to use to get the change;
    :param r: the value to return the change;
    :param only_cents: if the currency contain only integer denomination, set True for minimize (:100) the iteration.
    :return: the number of different ways that value r can be achieved by using denominations of the given currency;"""

    # sub problem: combinations to return n < r with a set of coins s' subset of s
    # base case: combinations to return 0 = 1
    # characteristic equation: sum of combinations using that coin with combinations without using that coin.

    # introducing convenient notation working in cents
    m = cur.num_denominations()
    S = [_ for _ in cur.iter_denominations()] if only_cents else [_float2int(x) for x in cur.iter_denominations()]
    n = _float2int(r) if not only_cents else r

    # Construct table
    T = [[0 for _ in range(m)] for _ in range(n + 1)]

    # Fill the entries for 0 value case (n = 0)
    for i in range(m):
        T[0][i] = 1

    # Fill rest of the table entries
    for i in range(1, n + 1):
        for j in range(m):
            # Count of solutions including S[j]
            x = T[i - S[j]][j] if i - S[j] >= 0 else 0

            # Count of solutions excluding S[j]
            y = T[i][j - 1] if j >= 1 else 0

            # total count
            T[i][j] = x + y

    return T[-1][-1]


def all_change(cur: Currency, r: float, max_permutation=1000, only_cents=True) -> List[Union[int, List]]:
    """This function, given in input a Currency Object and a float number r with at most two decimal points, returns all
    possible way to change r value with the currency c.
    (E.g., for a currency whose denominations are {0.1, 0.2, 0.5} and r=0.6, the algorithm must return 5, and the five
    different possible ways that can be used for changing 0.6, i.e., 0.5+0.1, 3*0.2, 0.2+4*0.1, 6*0.1.)

    :param cur: the currency to use to get the change;
    :param r: the value to return the change;
    :param max_permutation: the number of max list of different changes to return;
    :param only_cents: if the currency contain only integer denomination, set True for minimize (:100) the iteration.
    :returns: the number of different ways that value r can be achieved by using denominations of the given currency;
    :returns: the list of different changes of the value r that can be achieved by using denominations."""

    # sub problem: combinations to return n < r with a set of coins s' subset of s
    # base case: combinations to return 0 = 1: empty list
    # characteristic equation: sum of combinations using that coin with combinations without using that coin.

    # introducing convenient notation working in cents
    m = cur.num_denominations()
    S = [_ for _ in cur.iter_denominations()] if only_cents else [_float2int(x) for x in cur.iter_denominations()]
    n = _float2int(r) if not only_cents else r

    # Construct table
    T = [[[0, []] for _ in range(m)] for _ in range(n + 1)]

    # Base case (value zero has just one solution: empty list)
    for i in range(m):
        T[0][i] = [1, [[0 for _ in range(m)]]]

    # Fill rest of the table entries
    for i in range(1, n + 1):
        for j in range(m):
            # Count of solutions including S[j]
            x = T[i - S[j]][j][0] if i - S[j] >= 0 else 0

            # get max_permutation permutation value
            if x > 0:
                k = 0
                while len(T[i][j][1]) < max_permutation and k < len(T[i - S[j]][j][1]):
                    sol = T[i - S[j]][j][1][k]
                    T[i][j][1].append(sol[:])
                    T[i][j][1][-1][j] += 1
                    k += 1

            # Count of solutions excluding S[j]
            y = T[i][j - 1][0] if j >= 1 else 0

            # get max_permutation permutation value
            if y > 0:
                k = 0
                while len(T[i][j][1]) < max_permutation and k < len(T[i][j - 1][1]):
                    sol = T[i][j - 1][1][k]
                    T[i][j][1].append(sol[:])
                    k += 1

            # total count
            T[i][j][0] = x + y

    return T[-1][-1]


def all_change_number_only_bottom_up(cur: Currency, r: float, only_cents=True) -> int:
    """This function, given in input a Currency Object and a float number r with at most two decimal points, returns all
    possible way to change r value with the currency c.
    (E.g., for a currency whose denominations are {0.1, 0.2, 0.5} and r=0.6, the algorithm must return 5, and the five
    different possible ways that can be used for changing 0.6, i.e., 0.5+0.1, 3*0.2, 0.2+4*0.1, 6*0.1.)

    :param cur: the currency to use to get the change;
    :param r: the value to return the change;
    :param only_cents: if the currency contain only integer denomination, set True for minimize (:100) the iteration.
    :return: the number of different ways that value r can be achieved by using denominations of the given currency;"""

    # sub problem: combinations to return n < r with a set of coins s' subset of s
    # base case: combinations to return 0 = 1
    # characteristic equation: sum of combinations using that coin with combinations without using that coin.
    #
    # Since it is expensive to save all solutions m times as many coins, the spatial complexity of m can be reduced by
    # using a bottom up method.

    # introducing convenient notation working in cents
    m = cur.num_denominations()
    S = [_ for _ in cur.iter_denominations()] if only_cents else [_float2int(x) for x in cur.iter_denominations()]
    n = _float2int(r) if not only_cents else r

    # Construct table
    T = [0 for _ in range(n + 1)]

    # Base case (value zero has just one solution)
    T[0] = 1

    # Pick all coins one by one and update the T[] values after the index greater than or equal to the value of the
    # picked coin
    for i in range(0, m):
        for j in range(S[i], n + 1):
            T[j] += T[j - S[i]]

    return T[n]


def all_change_bottom_up(cur: Currency, r: float, max_permutation=1000, only_cents=True) -> List[Union[int, List]]:
    """This function, given in input a Currency Object and a float number r with at most two decimal points, returns all
    possible way to change r value with the currency c.
    (E.g., for a currency whose denominations are {0.1, 0.2, 0.5} and r=0.6, the algorithm must return 5, and the five
    different possible ways that can be used for changing 0.6, i.e., 0.5+0.1, 3*0.2, 0.2+4*0.1, 6*0.1.)

    :param cur: the currency to use to get the change;
    :param r: the value to return the change;
    :param max_permutation: the number of max list of different changes to return;
    :param only_cents: if the currency contain only integer denomination, set True for minimize (:100) the iteration.
    :returns: the number of different ways that value r can be achieved by using denominations of the given currency;
    :returns: the list of different changes of the value r that can be achieved by using denominations."""

    # sub problem: combinations to return n < r with a set of coins s' subset of s
    # base case: combinations to return 0 = 1: empty list
    # characteristic equation: sum of combinations using that coin with combinations without using that coin.
    #
    # Since it is expensive to save all solutions m times as many coins, the spatial complexity of m can be reduced by
    # using a bottom up method.

    # introducing convenient notation working in cents
    m = cur.num_denominations()
    n = _float2int(r) if not only_cents else r
    S = [_ for _ in cur.iter_denominations()] if only_cents else [_float2int(x) for x in cur.iter_denominations()]

    # Construct table
    T = [[0, []] for _ in range(n + 1)]

    # Base case (value zero has just one solution: empty list)
    T[0] = [1, [[0 for _ in range(m)]]]

    # Pick all coins one by one and update the T[] values after the index greater than or equal to the value of the
    # picked coin
    for i in range(0, m):
        for j in range(S[i], n + 1):
            # Get permutation number
            T[j][0] += T[j - S[i]][0]

            # get max_permutation permutation value
            k = 0
            while len(T[j][1]) < max_permutation and k < len(T[j - S[i]][1]):
                sol = T[j - S[i]][1][k]
                T[j][1].append(sol[:])
                T[j][1][-1][i] += 1
                k += 1

    return T[n]


def print_sequence(c, sequence, only_cent):
    S = [_ for _ in c.iter_denominations()]
    first = True

    print('(', end='')
    for i in range(len(sequence)):
        if sequence[i] != 0:
            if only_cent:
                print(', {} x {}'.format(sequence[i], S[i]) if not first else '{} x {}'.format(
                    sequence[i], S[i]), end='')
            else:
                print(', {} x {:.2f}'.format(sequence[i], S[i]) if not first else '{} x {:.2f}'.format(
                    sequence[i], S[i]), end='')
            first = False

    print(') ', end='')


def print_result(c, result, only_cent=True):
    print('{}, '.format(result[0]), end='')
    for sequence in result[1]:
        print_sequence(c, sequence, only_cent)


if __name__ == '__main__':
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

    value = 4.55

    cent = Currency('CEN')
    # cent.add_denomination(1)
    # cent.add_denomination(2)
    cent.add_denomination(5)
    cent.add_denomination(10)
    cent.add_denomination(20)
    cent.add_denomination(50)
    cent.add_denomination(100)
    cent.add_denomination(200)
    cent.add_denomination(500)
    cent.add_denomination(1000)
    cent.add_denomination(2000)
    cent.add_denomination(5000)

    original_stdout = sys.stdout  # Save a reference to the original standard output

    with open('output_all_change.txt', 'w') as f:
        sys.stdout = f  # Change the standard output to the file we created.

        print('\n\nvalue {} -> {}'.format(value, all_change_number_only(c, value, only_cents=False)))
        print('\nvalue {} -> '.format(value), end='')
        print_result(c, all_change(c, value, only_cents=False))
        print('\n\nvalue {} -> {}'.format(value, all_change_number_only_bottom_up(c, value, only_cents=False)))
        print('\nvalue {} -> '.format(value), end='')
        print_result(c, all_change_bottom_up(c, value, only_cents=False))

        print('\n\nvalue {} -> {}'.format(_float2int(value), all_change_number_only(cent, _float2int(value))))
        print('\nvalue {} -> '.format(_float2int(value)), end='')
        print_result(cent, all_change(cent, _float2int(value)))
        print('\n\nvalue {} -> {}'.format(_float2int(value), all_change_number_only_bottom_up(cent, _float2int(value))))
        print('\nvalue {} -> '.format(_float2int(value)), end='')
        print_result(cent, all_change_bottom_up(cent, _float2int(value)))

        sys.stdout = original_stdout  # Reset the standard output to its original value

    print('Algorithm terminated: output is in output_all_change.txt.')
