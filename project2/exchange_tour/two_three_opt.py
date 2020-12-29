def two_three_opt(g, hc, num_cycle):
    """Call the 2 opt algorithm until you get a 2opt-optimal solution, then call the 3-opt algorithm until you get an
    optimal 3-opt solution. If there are no more improvements, it re-executes on the rotated cycle and, if there are no
    improvements here, it returns the cycle found and its cost.

    :param g: the graph on which to search for the minimum Hamiltonian cycle;
    :param hc: list containing a starting Hamiltonian cycle that will be replaced with an improved cycle, if reduced;
    :param num_cycle: number of rotations for the algorithm to execute as a termination criterion.
    :returns: a boolean indicating whether the algorithm has found a better solution."""

    cnt = 0
    edited = False

    while cnt < 1:
        edited = _2opt(g, hc) or _3opt(g, hc)
        if edited:
            cnt = 0
        else:
            _rotate(hc, 1 / num_cycle)
            cnt += 1

    return edited


def _2opt(g, hc):
    """The idea is the following:
    1) disconnect hc[i] - hc[i+1] and hc[j] - hc[j+1];
    2) try to reconnect hc[i] - hc[j] and hc[i+1] - hc[j+1], if it's possible and if the solution is better.

    A graphical representation is as follows:

        1..  hc[i]       hc[j]                  1..  hc[i]   -    hc[j]
                     x     |         ---->                          |
        2.. hc[j+1]     hc[i+1]                 2.. hc[j+1]  -   hc[i+1]

    :param g: the graph on which to search for the minimum Hamiltonian cycle;
    :param hc: list containing a starting Hamiltonian cycle that will be replaced with an improved cycle, if reduced.
    :returns: a boolean indicating whether the algorithm has found a better solution."""

    # print('\tstart 2opt:   ', hc)  # --------------------------------------------------------------------- DEBUG PRINT

    edited = False

    # for each excangable 2opt moves
    for i in range(len(hc) - 3):
        for j in range(i + 2, len(hc) - 1):
            old_e1, old_e2 = g.get_edge(hc[i], hc[i + 1]), g.get_edge(hc[j], hc[j + 1])
            new_e1, new_e2 = g.get_edge(hc[i], hc[j]), g.get_edge(hc[i + 1], hc[j + 1])

            # verify existance of edge ...
            # old edges exists!
            if new_e1 is not None and new_e2 is not None:
                # ...and, in the case, if it's a better solution.
                old_w = round(old_e1.element() + old_e2.element(), 10)
                new_w = round(new_e1.element() + new_e2.element(), 10)

                # print('\t\told {}, new {}'.format(old_w, new_w))  # -------------------------------------- DEBUG PRINT

                if old_w > new_w:
                    edited = True
                    hc[i + 1:j + 1] = hc[j:i:-1]

                    # print('\t\t\t', 'i:', i, 'j:', j, '\n\t\t\tr -> ', hc)  # ---------------------------- DEBUG PRINT

    return edited


def _3opt(g, hc):
    """The idea is the following:
    We do not want to use the 3 opt in its totality as a complexity O(n^3) would not be very acceptable, therefore,
    considering to run it only after the 2opt termination, we only take into account the 3opt cases, and in the case of
    large sequences for a limited length.

        1..  _   hc[i]      hc[j]       hc[k]                   1..  -   hc[i]       hc[j]       hc[k] _
                  |     /     |     /     |              -->                     \     |     \     |    \
               hc[i+1]     hc[j+1]     hc[k+1]  - ..2           2..  -  hc[i+1]     hc[j+1]     hc[k+1]  \
                                                                           \______________________________\

        1..  _   hc[i]      hc[j]       hc[k]                   1..  -   hc[i]       hc[j]   -   hc[k]
                  |     /     |     /     |              -->                     x           /
               hc[i+1]     hc[j+1]     hc[k+1]  - ..2                   hc[i+1]     hc[j+1]     hc[k+1]  - ..2
                                                                           \_______________________|

    :param g: g: the graph on which to search for the minimum Hamiltonian cycle;
    :param hc: list containing a starting Hamiltonian cycle that will be replaced with an improved cycle, if reduced.
    :returns: a boolean indicating whether the algorithm has found a better solution."""

    # print('\tstart 3opt:   ', hc)  # --------------------------------------------------------------------- DEBUG PRINT

    edited = False

    # for each excangable 3opt moves
    for i in range(len(hc) - 5):
        for j in range(i + 2, len(hc) - 3):
            for k in range(j + 2, len(hc) - 1):
                old_e1 = g.get_edge(hc[i], hc[i + 1])
                old_e2 = g.get_edge(hc[j], hc[j + 1])
                old_e3 = g.get_edge(hc[k], hc[k + 1])

                # first case
                new_e1 = g.get_edge(hc[i], hc[j + 1])
                new_e2 = g.get_edge(hc[j], hc[k + 1])
                new_e3 = g.get_edge(hc[k], hc[i + 1])

                # second case
                new_e4 = g.get_edge(hc[i], hc[j + 1])
                new_e5 = g.get_edge(hc[j], hc[k])
                new_e6 = g.get_edge(hc[i + 1], hc[k + 1])

                # verify existance of edge ...
                # old edges exists!
                if new_e1 is not None and new_e2 is not None and new_e3 is not None:
                    # ...and, in the case, if it's a better solution.
                    old_w = round(old_e1.element() + old_e2.element() + old_e3.element(), 10)
                    new_w = round(new_e1.element() + new_e2.element() + new_e3.element(), 10)

                    # print('\t\t', 'i:', i, 'j:', j, 'k:', k, 'sx old {}, new {}'.format(old_w, new_w))  # -DEBUG PRINT

                    if old_w > new_w:
                        edited = True
                        hc[i + 1:k + 1] = hc[j + 1:k + 1] + hc[i + 1:j + 1]

                        # print('\n\t\t\tr -> ', hc)  # ---------------------------------------------------- DEBUG PRINT

                elif new_e4 is not None and new_e5 is not None and new_e6 is not None:
                    # ...and, in the case, if it's a better solution.
                    old_w = round(old_e1.element() + old_e2.element() + old_e3.element(), 10)
                    new_w = round(new_e4.element() + new_e5.element() + new_e6.element(), 10)

                    # print('\t\t', 'i:', i, 'j:', j, 'k:', k, 'sx old {}, new {}'.format(old_w, new_w))  # -DEBUG PRINT

                    if old_w > new_w:
                        edited = True
                        hc[i + 1:k + 1] = hc[j + 1:k + 1] + hc[j:i:-1]

                        # print('\n\t\t\tr -> ', hc)  # ---------------------------------------------------- DEBUG PRINT

    return edited


def _rotate(hc, frac=0.33):
    """rotate the solution found by 'item' nodes, leaving the solution unchanged.

    :param hc: the list representing a Hamiltonian cycle that will be rotated;
    :param frac: percentage of solution to rotate;
    :return: the rotated Hamiltonian cycle."""
    n = round(len(hc) * frac)
    hc[:] = hc[n:] + hc[:n]
