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
            if g.get_edge(vert, V[change]) is not None:
                g.insert_edge(vert, V[change], cur.get_change(change))

    return g, V


def _random_hamiltonian(g, V):
    """Given a graph, it returns one of the possible Hamiltonian cycles if it exists, otherwise None.

    :param g: the graph where to look for a Hamiltonian cycle.
    :param V: a map that stores the vertices as V[currencycode] = vertex(currency)
    :return: one of the possible Hamiltonian cycles if it exists, otherwise None."""
    pass


def excange_tour(C):
    """Design a local search algorithm that takes in input a set of Currency objects and looks for
    an exchange tour of minimal rate."""
    pass
