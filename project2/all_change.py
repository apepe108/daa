from project1.currency import Currency


def _float2int(x):
    return round(x * 100)


def _int2float(x):
    return round(x / 100, 2)


def all_change(cur: Currency, r: float):
    """This function, given in input a Currency Object and a float number r with at most two decimal points, returns all
    possible way to change r value with the currency c.
    (E.g., for a currency whose denominations are {0.1, 0.2, 0.5} and r=0.6, the algorithm must return 5, and the five
    different possible ways that can be used for changing 0.6, i.e., 0.5+0.1, 3*0.2, 0.2+4*0.1, 6*0.1.)

    :param cur: the currency to use to get the change;
    :param r: the value to return the change;
    :returns: the number of different ways that value r can be achieved by using denominations of the given currency;
    :returns: the list of different changes of the value r that can be achieved by using denominations."""

    # introducing convenient notation working in cents
    m = cur.num_denominations()
    S = [_float2int(x) for x in cur.iter_denominations()]
    n = _float2int(r)

    # Construct table
    T = [[0 for _ in range(m)] for _ in range(n + 1)]

    # Fill the entries for 0 value case (n = 0)
    for i in range(m):
        T[0][i] = 1

    # Fill rest of the table entries in bottom up manner
    for i in range(1, n + 1):
        for j in range(m):
            # Count of solutions including S[j]
            x = T[i - S[j]][j] if i - S[j] >= 0 else 0

            # Count of solutions excluding S[j]
            y = T[i][j - 1] if j >= 1 else 0

            # total count
            T[i][j] = x + y

    #for row in table:
    #    print(row)

    return T[n][m - 1]


if __name__ == '__main__':
    c = Currency('EUR')
    c.add_denomination(0.05)
    c.add_denomination(0.1)
    c.add_denomination(0.2)

    print(all_change(c, 0.30))