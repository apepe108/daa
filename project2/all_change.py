from project1.currency import Currency


def all_change(c: Currency, r: float):
    """This function, given in input a Currency Object and a float number r with at most two decimal points, returns all
    possible way to change r value with the currency c.
    (E.g., for a currency whose denominations are {0.1, 0.2, 0.5} and r=0.6, the algorithm must return 5, and the five
    different possible ways that can be used for changing 0.6, i.e., 0.5+0.1, 3*0.2, 0.2+4*0.1, 6*0.1.)

    :param c: the currency to use to get the change;
    :param r: the value to return the change;
    :returns: the number of different ways that value r can be achieved by using denominations of the given currency;
    :returns: the list of different changes of the value r that can be achieved by using denominations.
    """
