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
    V = {}  # store V[currencycode] = vertex(currency)

    # add all vertices
    for cur in set_currencies:
        V[cur.code()] = g.insert_vertex(cur)

    # for each vertex add edge corresponding to exchange rate
    for vert in g.vertices():
        cur = vert.element()
        for change in cur.iter_changes():
            g.insert_edge(vert, V[change], cur.get_change(change))

    return g, V


def _reconstruct_cycle(g, s, V, P):
    """Given a graph with a negative cycle inside it and a dictionary that reconstructs the path of a negative cycle,
    it reconstructs the path from an initial currency s to the cycle and back to s, so that the gain is negative.

    :param g: graph containing the negative cycle;
    :param s: the starting currency;
    :param V: a dict representing V[currencycode] = vector(currency);
    :param P: dictionary used to reconstruct the cycle path;
    :return: a list of vector sequence and the earned value."""

    cycle = []
    earn = 0
    curr = list(P.keys())[0]

    # go up the cycle until you find the negative cycle
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
        earn -= g.get_edge(V[cycle[-1].code()], V[rem.code()]).element()

    if s in cycle:
        # if starting currency is in the cycle
        i = cycle.index(s)
        return cycle[i:] + cycle[1:i + 1], round(earn, 10)
    else:
        # if starting currency is not in the cycle
        earn_go_to_cycle = g.get_edge(V[s.code()], V[cycle[0].code()]).element()
        earn_go_back = g.get_edge(V[cycle[-1].code()], V[s.code()]).element()
        move_earn = earn_go_back + earn_go_to_cycle

        k = 0
        while move_earn + k * earn > 0:
            k += 1

        new_cycle = [s]
        if k > 1:
            new_cycle += (k-1) * cycle[:-1]
            new_cycle += cycle
        else:
            new_cycle += (k * cycle)
        new_cycle.append(s)
        return new_cycle, round(k * earn + earn_go_to_cycle + earn_go_back, 10)


def arbitrage_opportunity(C, s):
    """Given a set of Currency objects, it returns an arbitrary opportunity if it exists, otherwise False.

    :param C: a set C of Currency objects such that, for every Object c in C, the attribute Change contains the rate
    exchange of c against every Other currency in C different from c;
    :param s: a specific Currency Object s.
    :return: None if s is not in C. If s belongs to C, then the algorithm returns False if there is not an arbitrage
    opportunity for s within the given set of currencies, and otherwise it returns a cycle that witnesses the arbitrage
    opportunity for s."""

    g, V = _create_graph(C)  # V[currencycode] = vertex(currency)

    # check if s is in C
    try:
        if V[s.code()] not in g.vertices():
            return None
    except KeyError:
        return None

    D = {}  # Store D[vertex] = w max
    P = {}  # Store P[next] = prev

    # Step 1: Initialize single source
    for vert in g.vertices():
        if vert.element() is s:
            D[vert] = 0
        else:
            D[vert] = float('inf')

    # Step 2: Relax all edges |V| - 1 times.
    for _ in range(g.vertex_count()):
        for edge in g.edges():
            u, v = edge.endpoints()  # for each u, v couple of vertex in g
            w = edge.element()
            if D[v] > round(D[u] + w, 10):  # relax
                D[v] = round(D[u] + w, 10)
                P[v] = u

    # Verify presence of negative cycle
    for edge in g.edges():
        u, v = edge.endpoints()  # for each u, v couple of vertex in g
        if D[v] > D[u] + edge.element():
            # Bellman theorem not satisfied -> there's a negative cycle
            return _reconstruct_cycle(g, s, V, P)

    # There is not arbitrage opportunity
    return False


if __name__ == '__main__':
    iteration = 5

    # GRAPH 1 in ./arbitrage_opportunity_img/graph1.jpg
    eur = Currency('EUR')
    eur.add_change('GBP', -0.31)
    eur.add_change('USD', 0.1)

    usd = Currency('USD')
    usd.add_change('EUR', 0.1)
    usd.add_change('GBP', 0.1)

    gbp = Currency('GBP')
    gbp.add_change('USD', 0.1)
    gbp.add_change('EUR', 0.1)

    print('\n\n---------- GRAPH 1 - STARTING FROM EUR ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp}, eur))

    print('\n\n---------- GRAPH 1 - STARTING FROM GBP ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp}, gbp))

    print('\n\n---------- GRAPH 1 - STARTING FROM GBP ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp}, usd))

    aed = Currency('AED')
    aed.add_change('USD', -0.1)
    aed.add_change('EUR', 0.2)
    aed.add_change('GBP', 0.23)

    print('\n\n---------- GRAPH 1 - STARTING FROM AED ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp}, aed))

    # GRAPH 2 in ./arbitrage_opportunity_img/graph2.jpg
    eur = Currency('EUR')
    eur.add_change('GBP', -0.42)
    eur.add_change('USD', 0.34)
    eur.add_change('AED', 0.11)

    usd = Currency('USD')
    usd.add_change('EUR', 0.05)
    usd.add_change('GBP', -0.05)
    usd.add_change('AED', 0.43)

    gbp = Currency('GBP')
    gbp.add_change('USD', 0.33)
    gbp.add_change('EUR', 0.2)
    gbp.add_change('AED', 0.15)

    aed = Currency('AED')
    aed.add_change('USD', -0.1)
    aed.add_change('EUR', 0.2)
    aed.add_change('GBP', 0.23)

    print('\n\n---------- GRAPH 2 - STARTING FROM EUR ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp, aed}, eur))

    print('\n\n---------- GRAPH 2 - STARTING FROM USD ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp, aed}, usd))

    print('\n\n---------- GRAPH 2 - STARTING FROM AED ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp, aed}, aed))

    print('\n\n---------- GRAPH 2 - STARTING FROM GBP ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp, aed}, gbp))

    # GRAPH 3 in ./arbitrage_opportunity_img/graph3.jpg
    eur = Currency('EUR')
    eur.add_change('GBP', -0.05)
    eur.add_change('USD', -0.1)

    usd = Currency('USD')
    usd.add_change('EUR', 0.1)
    usd.add_change('GBP', 0.1)

    gbp = Currency('GBP')
    gbp.add_change('USD', 0.1)
    gbp.add_change('EUR', 0.1)

    print('\n\n---------- GRAPH 3 - STARTING FROM EUR ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp}, eur))

    print('\n\n---------- GRAPH 3 - STARTING FROM GBP ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp}, gbp))

    print('\n\n---------- GRAPH 3 - STARTING FROM GBP ----------------')
    for _ in range(iteration):
        print(arbitrage_opportunity({eur, usd, gbp}, usd))
