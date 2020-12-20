from project1.currency import Currency
from TdP_collections.graphs.graph import Graph


def _create_graph(set_currencies):
    """Given a set of currency, it returns a graph that represents all the exchange possibilities.

    :param set_currencies: a set of Currency objects such that, for every Object c in the set, the attribute Change
    contains the rate exchange of c against every Other currency in the set different from c;
    :returns: a graph representing all the exchange way;
    :returns: a map containing the vertex associated at them currency code."""
    # instantiate direct graph
    g = Graph(True)
    V = {}

    # add all vertices
    for cur in set_currencies:
        V[cur._code] = g.insert_vertex(cur)

    # for each vertex add edge corresponding to exchange rate
    for vert in g.vertices():
        cur = vert.element()
        for change in cur._changes:
            g.insert_edge(vert, V[change], cur.get_change(change))

    return g, V


def arbitrage_opportunity(C, s):
    """Given a set of Currency objects, it returns an arbitrary opportunity if it exists, otherwise False.

    :param C: a set C of Currency objects such that, for every Object c in C, the attribute Change contains the rate
    exchange of c against every Other currency in C different from c;
    :param s: a specific Currency Object s.
    :return: None if s is not in C. If s belongs to C, then the algorithm returns False if there is not an arbitrage
    opportunity for s within the given set of currencies, and otherwise it returns a cycle that witnesses the arbitrage
    opportunity for s."""

    g, V = _create_graph(C)

    # check if s is in C
    if V[s._code] not in g.vertices():
        return None

    D = {}
    P = {}

    # Step 1: Initialize single source
    for vert in g.vertices():
        if vert.element() is s:
            D[vert] = 0
        else:
            D[vert] = float('inf')

    # Step 2: Relax all edges |V| - 1 times.
    for _ in range(g.vertex_count() - 1):
        for edge in g.edges():
            u, v = edge.endpoints()  # for each u, v couple of vertex in g
            w = edge.element()
            if D[v] > D[u] + w:  # relax
                D[v] = D[u] + w
                P[v] = u

    # Verify presence of negative cycle
    for edge in g.edges():
        u, v = edge.endpoints()  # for each u, v couple of vertex in g
        if D[v] > round(D[u] + edge.element(), 7):

            # Bellman theorem not satisfied -> there's a negative cycle
            cycle = []
            earn = 0
            curr = list(P.keys())[0]
            try:
                while earn >= 0 or curr.element() not in cycle:
                    cycle.append(curr.element())
                    prev = P[curr]
                    earn += g.get_edge(prev, curr).element()

                    curr = prev

                cycle.append(curr.element())
                cycle.reverse()

                # cycle end with same currency with which it begins
                while cycle[-1] is not curr.element():
                    rem = cycle.pop()
                    earn -= g.get_edge(V[cycle[-1]], V[rem]).element()

                if s in cycle:
                    i = cycle.index(s)
                    return cycle[i:] + cycle[1:i + 1], earn

                return cycle, earn
            except KeyError:
                print('\n\n', P)
                continue

    # There is not arbitrage opportunity
    return False


if __name__ == '__main__':
    eur = Currency('EUR')
    eur.add_change('GBP', -0.31)
    eur.add_change('USD', 0.1)

    usd = Currency('USD')
    usd.add_change('EUR', 0.005)
    usd.add_change('GBP', 0.1)

    gbp = Currency('GBP')
    gbp.add_change('USD', 0.1)
    gbp.add_change('EUR', 0.1)

    for _ in range(1000):
        print(arbitrage_opportunity({eur, usd, gbp}, usd))
