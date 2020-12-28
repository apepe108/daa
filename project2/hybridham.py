import random

from TdP_collections.graphs.graph import Graph


def hybridHAM(g, tour):
    """HybridHAM algorithm based. The proposed algorithm works in three steps:
        (l) Create an initial path
        (2) Convert the initial path to Hamiltonian path.
        (3) Convert the Hamiltonian path to Hamiltonian cycle.

    :param g: the graph where to look for a Hamiltonian cycle;
    :param tour: the list in which to memorize the Hamiltonian cycle;
    :return True if a Hamiltonian cycle where found, otherwise false."""

    # From the input graph, create two arrays Va and Vd of vertices sorted in the increasing and decreasing
    # order of their degrees, respectively.
    def _by_degree(v):
        return g.degree(v)

    Va = []
    for vert in g.vertices():
        Va.append(vert)
    Va.sort(key=_by_degree)

    Vd = Va[:]
    Vd.reverse()

    # PHASE 1
    # Create an initial path
    path = []
    i = 0

    # Repeat Phase I for each of the highest degree vertex of the graph and select the longest Pi as initial path.
    while len(path) != g.vertex_count() and (i == 0 or Vd[i] == Vd[i - 1]):
        new_path = []

        # (1) Start from one of the highest degree vertex (first vertex in the array Vd). Let it be Vs.
        vs = Vd[i]

        # 2) Add it to the initial path.
        new_path.append(vs)

        # (3) Repeat until vs becomes a dead end.
        _greedy_dfs(g, vs, new_path, Va)

        print('greedy_dfs', new_path, len(new_path))

        if len(new_path) > len(path):
            path = new_path[:]
        i += 1
    # //End of Phase 1
    # (4) If |Pi| == n then go to Phase 3.

    # Phase 2
    # Convert the initial path into Hamiltonian path
    # (5) Repeat until |Pi| != n.
    while len(path) != g.vertex_count():
        # (a) Select the highest degree end of the path Pi for rotational transformation
        d_front, d_back = g.degree(path[0]), g.degree(path[-1])

        # (b) Reverse Pi if the first vertex in Pi is having degree higher than the last vertex to make the highest
        # degree vertex as the end vertex of the path. Let it be vx.
        if d_front > d_back or (d_front == d_back and random.random() > 0.5):  # Upgrade: introduced probability change
            path.reverse()

        # (c) Apply rotational transformation to Pi using c to get a new path.
        # (d) If rotational transformation could not be applied then either the graph is not having Hamiltonian path or
        # the algorithm fails to identify the Hamiltonian path and so exit.
        if not _rotational_transform(g, path):
            return False

        # (e) Extend this new path by using the greedy depth first search as in Phase 1
        _greedy_dfs(g, path[-1], path, Va)

    # (6) Now Pi is the Hamiltonian Path Pi. Assign Ph = i.
    print('maxed', path, len(path))

    # Phase 3
    # Convert Hamiltonian path into Hamiltonian cycle

    # (8) Repeat
    # (a) Select the smallest degree end of the path Ph for
    # rotational transformation
    # (b) Reverse Ph if the first vertex in Ph is having
    # degree higher than the last vertex to make the
    # smallest degree vertex as the end vertex of the
    # path. Let it be v.
    # (c) Apply rotational transformation to Ph using v»,
    # to get a new path.
    # (d) If rotational transformation could not be
    # applied then either the graph is not having
    # Hamiltonian Cycle or the algorithm fails to
    # identify the Hamiltonian path and so exit.
    # Until there is an edge connecting the first and last
    # vertices of the path Ph.
    # (9) Now Ph is the Hamiltonian cycle and return PIE.


def _greedy_dfs(g, vs, path, va):
    # (a) Select the next smallest degree neighbour of Vs. Let it be Vi.
    vi = None

    for v in va:
        edge = g.get_edge(vs, v)
        if edge is not None:
            if v not in path:
                # UNREACHABLE VERTEX HEURISTIC (not implemented)
                # (b) If the selection of Vi is not making any of its unvisited neighbours unreachable then
                #     (i) add it to the initial path Pi
                #     (ii) make Vi as vs
                vi = v
                break

    if vi is not None:
        path.append(vi)
        _greedy_dfs(g, vi, path, va)
    return


def _rotational_transform(g, path):
    # (1) Find a vertex adjacent to vx in the input graph, in path P. Let it be vertex b.
    vx = path[-1]

    adj_vx = [e.opposite(vx) for e in g.incident_edges(vx)]
    random.shuffle(adj_vx)

    for v in adj_vx:
        if v in path:
            _rotate_path(path, v)
            return True

    return False


def _rotate_path(path, b):
    # (2) Create a new path P',
    #     (a) by connecting b to e
    #     (b) by reversing the path from end to e
    i_b = path.index(b)
    if i_b < len(path) - 2:
        path[i_b + 1:] = path[-1:i_b:-1]

