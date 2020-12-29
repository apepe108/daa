import random


def hybridHAM(g, path):
    """HybridHAM algorithm based. The proposed algorithm works in three steps:
        (1) Create an initial path
        (2) Convert the initial path to Hamiltonian path.
        (3) Convert the Hamiltonian path to Hamiltonian cycle.

    :param g: the graph where to look for a Hamiltonian cycle;
    :param path: a list in which to save the path;
    :return True if a Hamiltonian cycle where found, otherwise false."""

    # From the input graph, create two arrays Va and Vd of vertices sorted in the increasing and decreasing
    # order of their degrees, respectively.
    def _by_degree(v):
        return g.degree(v)

    Va = []
    for vert in g.vertices():
        Va.append(vert)
    Va.sort(key=_by_degree)

    # -----------   Phase 1   --------------------
    # Create an initial path
    path[:] = []
    i = len(Va) - 1

    # Repeat Phase I for each of the highest degree vertex of the graph and select the longest Pi as initial path.
    while len(path) != g.vertex_count() and i > 0 and (i == len(Va) - 1 or Va[i] == Va[i + 1]):
        new_path = []

        # (1) Start from one of the highest degree vertex (first vertex in the array Vd). Let it be Vs.
        vs = Va[i]

        # 2) Add it to the initial path.
        new_path.append(vs)

        # (3) Repeat until vs becomes a dead end.
        _greedy_dfs(g, vs, new_path, Va)

        if len(new_path) > len(path):
            path[:] = new_path[:]
        i -= 1
    # //End of Phase 1
    # print('greedy_dfs:', path, len(path))  # ------------------------------------------------------------- DEBUG PRINT
    # (4) If |Pi| == n then go to Phase 3.

    # -----------   Phase 2   --------------------
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
    # print('hamiltonian_path:', path, len(path))  # ------------------------------------------------------- DEBUG PRINT

    # -----------   Phase 3   --------------------
    # Convert Hamiltonian path into Hamiltonian cycle

    # (8) Repeat until there is an edge connecting the first and last vertices of the path Ph.
    while g.get_edge(path[0], path[-1]) is None:
        # (a) Select the smallest degree end of the path Ph for rotational transformation
        d_front, d_back = g.degree(path[0]), g.degree(path[-1])

        # (b) Reverse Ph if the first vertex in Ph is having degree higher than the last vertex to make the smallest
        # degree vertex as the end vertex of the path. Let it be Vy.
        if d_front < d_back or (d_front == d_back and random.random() > 0.5):  # Upgrade: introduced probability change
            path.reverse()

        # (c) Apply rotational transformation to Ph using Vy, to get a new path.
        # (d) If rotational transformation could not be applied then either the graph is not having Hamiltonian Cycle or
        # the algorithm fails to identify the Hamiltonian path and so exit.
        if not _rotational_transform(g, path):
            return False

    # (9) Now Ph is the Hamiltonian cycle and return Ph.
    # print('hamiltonian_cycle:', path)  # ----------------------------------------------------------------- DEBUG PRINT
    # End of 3

    return True


def _greedy_dfs(g, vs, path, va):
    """Like the DFS algorithm, it loops through the graph. However, unlike DFS, it does not go through the same node
    twice. In addition, of the nodes adjacent to the current one, the one with the lowest degree is visited.

    :param g: the graph we are using in the Hamiltonian tour search;
    :param vs: the starting edge;
    :param path: the list into memorize the path;
    :param va: a list containing all the vertex in the graph, sorted by increasing degree."""
    # (a) Select the next smallest degree neighbour of Vs. Let it be Vi.
    vi = None

    for v in va:
        edge = g.get_edge(vs, v)
        if edge is not None:
            if v not in path:
                # if not _unreachable_vertex(g, path, v):
                vi = v
                break

    if vi is not None:
        path.append(vi)
        _greedy_dfs(g, vi, path, va)


def _unreachable_vertex(g, path, v):
    """Unreachable Vertex Heuristic NOT IMPLEMENTED!
    We agreed that, although this heuristic avoids the creation of dead ends, the performance decreases a
    lot compared to recovering them through step 2 (rotational transform)."""
    pass


def _rotational_transform(g, path):
    """(1) Find a vertex adjacent to the end path in the input graph, in path P. It then makes the new vertex the final
    part of the path.

    :param g: the graph we are using in the Hamiltonian tour search;
    :param path: the path on which to apply the rotational transform.
    :return True if the path is rotated. If the path is not rotatable, it returns False."""
    vx = path[-1]

    adj_vx = [e.opposite(vx) for e in g.incident_edges(vx)]
    random.shuffle(adj_vx)

    for v in adj_vx:
        if v in path:
            _rotate_path(path, v)
            return True

    return False


def _rotate_path(path, b):
    """(2) Create a new path P',
           (a) by connecting b to e
           (b) by reversing the path from end to e
    
    :param path: The path represented by a list of vertices to rotate;
    :param b: The element to connect at the end of the loop."""
    i_b = path.index(b)
    if i_b < len(path) - 2:
        path[i_b + 1:] = path[-1:i_b:-1]
