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


def _random_hamiltonian(g, curr, hc=None, cost=0):
    """Given a graph, it returns one of the possible Hamiltonian cycles if it exists.

    :param g: the graph where to look for a Hamiltonian cycle.
    :param hc: the hamiltonian cycle path.
    :returns: True if an Hamiltonian cycles exists, otherwise False;
    :returns: a list of vertex representing the path;
    :returns: the solution cost;
    """
    # By default, the cycle is evaluated from the beginning.
    if hc is None:
        hc = [curr]
        return _random_hamiltonian(g, curr, hc, cost)

    # base case: if all vertices are included in the path Last vertex must be adjacent to the first vertex in path to
    # make a cycle
    if g.vertex_count() == len(hc):
        e = g.get_edge(hc[0], hc[-1])
        return e is not None, hc, cost + e.element() if e is not None else cost

    # Try different vertices as a next candidate in Hamiltonian Cycle
    for e in g.incident_edges(curr):
        o = e.opposite(curr)  # for each adjacent vertex
        if o not in hc:
            hc.append(o)

            # Start recurs
            res = _random_hamiltonian(g, o, hc, cost + e.element())

            if res[0]:  # if solution found
                return res
            else:  # remove the current currency and try with another
                hc.pop()

    # Fail case
    return False, hc, cost


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


def excange_tour(C):
    """Design a local search algorithm that takes in input a set of Currency objects and looks for
    an exchange tour of minimal rate."""
    g, V = _create_graph(C)

    min_cost = min_cycle = None
    for hc in _hamiltonian_brute_force(g):
        if min_cost is None or hc[1] < min_cost:
            min_cycle, min_cost = hc
    return min_cycle, min_cost


if __name__ == '__main__':
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

    print(excange_tour({usd, gbp, eur, cny, jpy}))
