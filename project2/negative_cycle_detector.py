from TdP_collections.graphs.transitive_closure import floyd_warshall
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

    # print_graph(g)
    # closure = floyd_warshall(g)
    # print("Number of edges in closure is", closure.edge_count(), '\n\n')

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
    prev = {}

    # Step 1: Initialize single source
    for vert in g.vertices():
        if vert.element() is s:
            D[vert] = 0
        else:
            D[vert] = float('inf')

    # Step 2: Relax all edges |V| - 1 times.
    for _ in range(g.vertex_count()):   # miss -1
        for edge in g.edges():
            u, v = edge.endpoints()  # for each u, v couple of vertex in g
            w = edge.element()
            if D[v] > round(D[u] + w, 3):  # relax
                D[v] = round(D[u] + w, 3)
                prev[v] = u

    # Verify presence of negative cycle
    for edge in g.edges():
        u, v = edge.endpoints()  # for each u, v couple of vertex in g
        w = edge.element()
        if D[v] > round(D[u] + w, 3):
            # algorithm does not work because there is a negative cycle
            try:
                # Starting from s, travels to its ancestors until it finds a the vertex from which started
                cycle = []
                curr = V[s._code]
                while True:
                    p = prev[curr]
                    cycle.append(p.element())
                    if p == V[s._code]:
                        cycle.reverse()
                        return cycle
                    curr = p
            except KeyError:
                # the negative cycle do not pass by s
                return False, prev

    # There is not arbitrage opportunity
    return False


def print_graph(graph):
    print("Vertices : ")
    for i in graph.vertices():
        print(i)
    print("Edges : ")
    for i in graph.edges():
        print(i)


if __name__ == '__main__':
    # cur1 = Currency('EUR')
    # cur1.add_change('USD', 1000)
    # cur1.add_change('AAA', -2000)
    #
    # cur2 = Currency('GBP')
    # cur2.add_change('USD', 5)
    # cur2.add_change('EUR', 1000)
    #
    # cur3 = Currency('USD')
    # cur3.add_change('EUR', 1)
    # cur3.add_change('GBP', 10000)
    #
    # cur4 = Currency('AAA')
    # cur4.add_change('GBP', 1000)
    # cur4.add_change('USD', 1)
    # cur4.add_change('BBB', 40)
    # cur2.add_change('CCC', 1)
    #
    # cur5 = Currency('BBB')
    #
    # cur5.add_change('GBP', 1000)
    # cur5.add_change('AAA', 5)
    # cur5.add_change('USD', -9)
    #
    # cur6 = Currency('CCC')
    # cur6.add_change('EUR', 1)
    # cur6.add_change('GBP', 1000)
    # cur6.add_change('BBB', -32)
    #
    # cur7 = Currency('DDD')
    # cur7.add_change('EUR', 1)
    # cur7.add_change('GBP', 1000)
    #
    # currencies = {cur1, cur2, cur3, cur4, cur5, cur6, cur7}
    # graph = _create_graph(currencies)
    # print_graph(graph[0])
    #
    # closure = floyd_warshall(graph[0])
    # print("Number of edges in closure is", closure.edge_count())
    #
    # print("\n\n")

    eur = Currency('EUR')
    eur.add_change('GBP', -0.31)
    eur.add_change('USD', 1)

    usd = Currency('USD')
    usd.add_change('EUR', 0.3)
    usd.add_change('GBP', 1)

    gbp = Currency('GBP')
    gbp.add_change('USD', 0.005)
    gbp.add_change('EUR', 1)

    for _ in range(1000):
        print(arbitrage_opportunity({eur, usd, gbp}, usd))
