from TdP_collections.graphs.transitive_closure import floyd_warshall
from project1.currency import Currency
from TdP_collections.graphs.graph import Graph

def create_graph(setCurrencies):
    # instanciate direct graph
    graph = Graph(True)

    # add all vertices
    for i in setCurrencies:
        graph.insert_vertex(i)

    for i in graph.vertices():
        elem = i.element()
        for j in elem._changes:
            vert = get_vertex(graph, j)
            if vert is not None:
                graph.insert_edge(i, vert, elem.get_change(j))

    return graph

def print_graph(graph):
    print("Vertices : ")
    for i in graph.vertices():
        print(i)
    print("Edges : ")
    for i in graph.edges():
        print(i)

def get_vertex(graph, elem):
    for i in graph.vertices():
        if elem == i.element()._code:
            return i
    return None

def negative_cycle_detector(graph, src):
    if get_vertex(graph, src.element()._code) == None:
        return None

    V = graph.vertex_count()
    # Initialize the distance to infinite for all vertices different from 0
    dist = {}
    p = {}
    for i in graph.vertices():
        dist[i] = float('inf')
    dist[src] = 0

    # Step 2: Relax all edges |V| - 1 times.
    # A simple shortest path from src to any
    # other vertex can have at-most |V| - 1
    # edges. If at the last iteration the values still changes (x!=-1) then there is a negative cycle

    for i in range(0, V):
        x = -1
        for j in graph.edges():
            u, v = j.endpoints()
            weight = j.element()
            if (dist[u] != float('inf') and dist[u] + weight < dist[v]):
                dist[v] = dist[u] + weight
                p[v] = u
                x = v

    # Cycle Detection:
    if x == -1:
        return False
    else:
        for i in range(V):
            x = p[x]

        cycle = []
        v = x
        # Starting from a vertex, travels to its ancestors until it finds a the vertex from which started
        while v != p[v]:
            cycle.append(v)
            v = p[v]
            if (v == x and len(cycle) > 1):
                break

        return cycle if src in cycle else False


if '__main__':
    cur1 = Currency('EUR')
    cur1.add_change('USD', 1000)
    cur1.add_change('AAA', -2000)

    cur2 = Currency('GBP')
    cur2.add_change('USD', 5)
    cur2.add_change('EUR', 1000)

    cur3 = Currency('USD')
    cur3.add_change('EUR', 1)
    cur3.add_change('GBP', 10000)

    cur4 = Currency('AAA')
    cur4.add_change('GBP', 1000)
    cur4.add_change('USD', 1)
    cur4.add_change('BBB', 40)
    cur2.add_change('CCC', 1)

    cur5 = Currency('BBB')

    cur5.add_change('GBP', 1000)
    cur5.add_change('AAA', 5)
    cur5.add_change('USD', -9)

    cur6 = Currency('CCC')
    cur6.add_change('EUR', 1)
    cur6.add_change('GBP', 1000)
    cur6.add_change('BBB', -32)

    cur7 = Currency('DDD')
    cur7.add_change('EUR', 1)
    cur7.add_change('GBP', 1000)

    currencies = {cur1, cur2, cur3, cur4, cur5, cur6, cur7}
    graph = create_graph(currencies)
    print_graph(graph)

    closure = floyd_warshall(graph)
    print("Number of edges in closure is", closure.edge_count())

    print("\n\n")
    x = ""
    for i in graph.vertices():
        if i.element()._code == 'USD':
            x = i
            break
    print("Source : ", x.element()._code)
    cycle = negative_cycle_detector(graph, x)

    if cycle == None:
        print("argument not in graph")
    elif cycle == False:
        print("No cycle Found")
    else:
        print("Cycle :")
        for i in cycle:
            print(i.element()._code)
