import random

from TdP_collections.graphs.graph import Graph
from project1.currency import Currency


def _create_graph(set_currencies):
    """Given a set of currency, it returns a graph that represents all the exchange possibilities.

    :param set_currencies: a set of Currency objects such that, for every Object c in the set, the attribute Change
    contains the rate exchange of c against every Other currency in the set different from c;
    :returns: a graph representing all the exchange way;
    :returns: a map containing the vertex associated at them currency code."""
    # instantiate direct graph
    g = Graph()
    V = {}  # store V[currencycode] = vertex(currency)

    # add all vertices
    for cur in set_currencies:
        V[cur.code()] = g.insert_vertex(cur)

    # for each vertex add edge corresponding to exchange rate
    for vert in g.vertices():
        cur = vert.element()
        for change in cur.iter_changes():
            if g.get_edge(vert, V[change]) is None:
                g.insert_edge(vert, V[change], cur.get_change(change))

    return g, V


def _hamiltonian_brute_force(g, curr=None, hc=None, cost=0):
    """Given a graph, it returns a generator of all hamiltonian cycle."""
    if curr is None:
        curr = random.choice(list(g.vertices()))

    # By default, the cycle is evaluated from the beginning.
    if hc is None:
        hc = [curr]

    # Try different vertices as a next candidate in Hamiltonian Cycle
    for e in g.incident_edges(curr):
        o = e.opposite(curr)  # for each adjacent vertex
        if o not in hc:
            hc.append(o)

            # base case: if all vertices are included in the path Last vertex must be adjacent to the first vertex in
            # path to make a cycle
            if g.vertex_count() == len(hc):
                ce = g.get_edge(hc[0], hc[-1])
                if ce is not None:
                    yield hc + [hc[0]], round(cost + e.element() + ce.element(), 10)
            else:
                # Start recurs
                for res in _hamiltonian_brute_force(g, o, hc, cost + e.element()):
                    yield res

            # remove the current currency and try with another
            hc.pop()


def excange_tour_brute_force(C):
    """A local search algorithm that takes in input a set of Currency objects and looks for
    an exchange tour of minimal rate."""
    g, V = _create_graph(C)

    min_cost = min_cycle = None
    for hc in _hamiltonian_brute_force(g):
        if min_cost is None or hc[1] < min_cost:
            min_cycle, min_cost = hc
    return min_cycle, min_cost


def _random_hamiltonian(g, curr=None, hc=None, cost=0):
    """Given a graph, it returns one of the possible Hamiltonian cycles if it exists.

    :param g: the graph where to look for a Hamiltonian cycle.
    :param hc: the hamiltonian cycle path.
    :returns: True if an Hamiltonian cycles exists, otherwise False;
    :returns: a list of vertex representing the path;
    :returns: the solution cost;
    """
    # By default, the cycle is evaluated from the beginning, starting from a random node.
    if hc is None:
        if curr is None:
            curr = random.choice(list(g.vertices()))
        hc = [curr]
        return _random_hamiltonian(g, curr, hc, cost)

    # base case: if all vertices are included in the path Last vertex must be adjacent to the first vertex in path to
    # make a cycle
    if g.vertex_count() == len(hc):
        e = g.get_edge(hc[0], hc[-1])
        return e is not None, hc + [hc[0]], round(cost + e.element(), 10) if e is not None else cost

    # Try different vertices as a next candidate in Hamiltonian Cycle
    for e in g.incident_edges(curr):
        o = e.opposite(curr)  # for each adjacent vertex
        if o not in hc:
            hc.append(o)

            # Start recurs
            res = _random_hamiltonian(g, o, hc, round(cost + e.element(), 10))

            if res[0]:  # if solution found
                return res
            else:  # remove the current currency and try with another
                hc.pop()

    # Fail case
    return False, hc, cost


def excange_tour(C):
    """A local search algorithm that takes in input a set of Currency objects and looks for
    an exchange tour of minimal rate."""
    g, V = _create_graph(C)

    found, hc, cost = _random_hamiltonian(g)
    if not found:
        return None

    edited = True
    while edited:
        edited, hc, cost = _2opt_with_rotation(g, hc, cost)

    return hc, cost


def _2opt_with_rotation(g, hc, cost):
    cnt = 0
    edited = False

    while cnt < 3:
        edited, hc, cost = _2opt(g, hc, cost)
        if edited:
            cnt = 0
        else:
            hc = _rotate(hc)
            cnt += 1

    return edited, hc, cost


def _2opt(g, hc, cost):
    # DEBUG PRINT
    print('start:   ', hc)

    edited = False

    # for each excangable 2opt moves
    for i in range(len(hc) - 3):

        # The idea is the following:
        # unconnect hc[i] - hc[i+1] and hc[i+2] - hc[i+3]
        # try to reconnect hc[i] - hc[i+3] and hc[i+1] - hc[i+2], if it's possible and if the solution is better
        #
        # ..  hc[i]       hc[j]                  ..  hc[i]   -    hc[j]
        #             x     |         ---->                         |
        # .. hc[j+1]     hc[i+1]                 .. hc[j+1]  -   hc[i+1]

        for j in range(i + 2, len(hc) - 1):
            old_e1, old_e2 = g.get_edge(hc[i], hc[i + 1]), g.get_edge(hc[j], hc[j + 1])
            new_e1, new_e2 = g.get_edge(hc[i], hc[j]), g.get_edge(hc[i + 1], hc[j + 1])

            # verify existance of edge ...
            # old edges exists!
            if new_e1 is not None and new_e2 is not None:
                # ...and, in the case, if it's a better solution.
                old_w = round(old_e1.element() + old_e2.element(), 10)
                new_w = round(new_e1.element() + new_e2.element(), 10)
                if old_w > new_w:
                    edited = True
                    cost = round(cost - old_w + new_w, 10)
                    hc[i + 1:j + 1] = hc[j:i:-1]

                    # DEBUG PRINT
                    print('r {}:{} -> '.format(i + 1, j + 1), hc)

    return edited, hc, cost


def _rotate(hc):
    return hc[1:] + [hc[1]]


def _populate_graph1():
    usd = Currency('USD')
    usd.add_change('GBP', 0.09)
    usd.add_change('EUR', 0.3)
    usd.add_change('JPY', 0.43)

    gbp = Currency('GBP')
    gbp.add_change('USD', 0.09)
    gbp.add_change('CNY', 0.05)
    gbp.add_change('EUR', 0.31)

    eur = Currency('EUR')
    eur.add_change('USD', 0.3)
    eur.add_change('GBP', 0.31)
    eur.add_change('CNY', 0.87)

    cny = Currency('CNY')
    cny.add_change('JPY', 0.11)
    cny.add_change('GBP', 0.05)
    cny.add_change('EUR', 0.87)

    jpy = Currency('JPY')
    jpy.add_change('USD', 0.43)
    jpy.add_change('CNY', 0.11)

    return {usd, gbp, eur, cny, jpy}


def _populate_graph2():
    gbp = Currency('GBP')
    gbp.add_change('BDT', 0.66)
    gbp.add_change('AED', 0.2)
    gbp.add_change('USD', 0.09)
    gbp.add_change('EUR', 0.31)
    gbp.add_change('CNY', 0.05)

    cny = Currency('CNY')
    cny.add_change('GBP', 0.05)
    cny.add_change('EUR', 0.87)
    cny.add_change('ILS', 0.34)
    cny.add_change('JPY', 0.11)

    eur = Currency('EUR')
    eur.add_change('GBP', 0.31)
    eur.add_change('CNY', 0.87)
    eur.add_change('DOP', 0.15)
    eur.add_change('USD', 0.3)

    ils = Currency('ILS')
    ils.add_change('DOP', 0.15)
    ils.add_change('CNY', 0.34)
    ils.add_change('LAB', 0.6)
    ils.add_change('JOD', 0.05)

    dop = Currency('DOP')
    dop.add_change('EUR', 0.15)
    dop.add_change('ILS', 0.15)
    dop.add_change('JOD', 0.11)
    dop.add_change('USD', 0.2)

    aed = Currency('AED')
    aed.add_change('GBP', 0.2)
    aed.add_change('USD', 0.15)
    aed.add_change('JPY', 0.4)
    aed.add_change('ETB', 0.4)
    aed.add_change('BDT', 0.48)

    usd = Currency('USD')
    usd.add_change('AED', 0.15)
    usd.add_change('GBP', 0.09)
    usd.add_change('EUR', 0.3)
    usd.add_change('DOP', 0.2)
    usd.add_change('JPY', 0.43)

    jod = Currency('JOD')
    jod.add_change('DOP', 0.11)
    jod.add_change('ILS', 0.05)
    jod.add_change('LAB', 0.4)

    lab = Currency('LAB')
    lab.add_change('ILS', 0.6)
    lab.add_change('JOD', 0.4)

    etb = Currency('ETB')
    etb.add_change('AED', 0.4)
    etb.add_change('GIP', 0.3)
    etb.add_change('CAD', 0.5)

    gip = Currency('GIP')
    gip.add_change('ETB', 0.3)
    gip.add_change('CAD', 0.25)

    cad = Currency('CAD')
    cad.add_change('ETB', 0.5)
    cad.add_change('GIP', 0.25)
    cad.add_change('JPY', 0.06)
    cad.add_change('BDT', 0.85)

    bdt = Currency('BDT')
    bdt.add_change('GBP', 0.66)
    bdt.add_change('AED', 0.48)
    bdt.add_change('CAD', 0.85)
    bdt.add_change('JPY', 0.12)

    jpy = Currency('JPY')
    jpy.add_change('BDT', 0.12)
    jpy.add_change('CAD', 0.06)
    jpy.add_change('AED', 0.4)
    jpy.add_change('USD', 0.43)
    jpy.add_change('CNY', 0.11)

    return {gbp, cny, eur, ils, dop, aed, usd, jod, lab, etb, gip, cad, bdt, jpy}


if __name__ == '__main__':
    print('-------- GRAPH 1 -----------------')
    print('\n1)  Brute force:')
    print(excange_tour_brute_force(_populate_graph1()))
    print('\n2)  Local Search:')
    print(excange_tour(_populate_graph1()))

    print('\n\n------------ GRAPH 2 -----------------')
    print('\n1)  Brute force:')
    print(excange_tour_brute_force(_populate_graph2()))
    print('\n2)  Local Search:')
    print(excange_tour(_populate_graph2()))
