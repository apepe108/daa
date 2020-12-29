import math

from TdP_collections.graphs.graph import Graph
from project2.exchange_tour.hybridham import hybridHAM
from project2.exchange_tour.two_three_opt import two_three_opt
from project2.exchange_tour import dataset

from datetime import datetime


def exchange_tour(C):
    """A local search algorithm that takes in input a set of Currency objects and looks for
    an exchange tour of minimal rate.

    :param C: a set of Currency objects.
    :return list representing the computed Hamiltonian cycle or None if the set made a non Hamiltonian graph."""
    g, V = _create_graph(C)

    hc = []

    # Given that hybridHam fails in cases where the Hamiltonian cycle exists as the graph grows and that the computation
    # time of this is significantly lower than the rest of the time, we have chosen to run it several times to try to
    # obtain a better result.
    cnt = 0
    while not hybridHAM(g, hc):
        if cnt > math.log2(g.vertex_count()):
            return None
        cnt += 1

    # print('founded first', datetime.now())  # ------------------------------------------------------------ DEBUG PRINT
    # print('part:{}\ncost:{}'.format(hc, get_cost(C, hc) if hc is not None else 0))

    while two_three_opt(g, hc, num_cycle=math.log2(g.vertex_count())):
        pass

    return [v.element() for v in hc]


def get_cost(hc):
    """Given a Hamiltonian cycle, it returns the cost of the cycle.

    :param hc: the Hamiltonian cycle.
    :return: the cost."""
    cost = 0
    for i in range(len(hc)):
        cost += hc[i].get_change(hc[(i + 1) % len(hc)].code())
    return round(cost, 10)


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

    # print('created', datetime.now())  # ------------------------------------------------------------------ DEBUG PRINT
    return g, V


# --------------------- DRIVER TEST ------------------------------------------------------------------------------------

if __name__ == '__main__':
    def do_local_search(C):
        print('\nLocal Search')
        start_time = datetime.now()
        tour = exchange_tour(C)
        end_time = datetime.now()
        print('founded in {}'.format(end_time - start_time))
        print('tour:{}\ncost:{}'.format(tour, get_cost(tour) if tour is not None else 0))


    print('-------- GRAPH 5n -----------------')
    C1 = dataset.graph_5n()
    do_local_search(C1)

    print('\n\n------------ GRAPH 14n -----------------')
    C2 = dataset.graph_14n()
    do_local_search(C2)

    print('\n\n------------ GRAPH 45n -----------------')
    C3 = dataset.graph_45n()
    do_local_search(C3)

    print('\n\n------------ GRAPH 100n -----------------')
    C4 = dataset.graph_100n()
    do_local_search(C4)
