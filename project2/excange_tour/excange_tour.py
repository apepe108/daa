import random

from TdP_collections.graphs.graph import Graph
from project1.currency import Currency
from project2.excange_tour.hybridham import hybridHAM

from datetime import datetime


def excange_tour(C):
    """A local search algorithm that takes in input a set of Currency objects and looks for
    an exchange tour of minimal rate.

    :param C: a set of Currency objects.
    :return list representing the computed Hamiltonian cycle or None if the set made a non Hamiltonian graph."""
    g, V = _create_graph(C)

    hc = []
    found = hybridHAM(g, hc)
    if not found:
        return None
    # print('founded first', datetime.now())  # ------------------------------------------------------------ DEBUG PRINT

    edited = True
    while edited:
        edited = _2_3opt(g, hc, num_cycle=len(hc) + 1)

    return hc


def get_cost(C, hc):
    g, V = _create_graph(C)

    cost = 0
    for i in range(len(hc)):
        cost += g.get_edge(V[hc[i].element().code()], V[hc[(i + 1) % len(hc)].element().code()]).element()
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


# ---------------------------------------------------------------------------------------------------------------------
# -------------- TRY TO REMOVE NUM CYCLE OPERATING 2-3 OPT ON DOUBLE SIZE ARRAY ---------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def _2_3opt(g, hc, num_cycle):
    """Call the 2 opt algorithm until you get a 2opt-optimal solution, then call the 3-opt algorithm until you get an
    optimal 3-opt solution. If there are no more improvements, it re-executes on the rotated cycle and, if there are no
    improvements here, it returns the cycle found and its cost.

    :param g: the graph on which to search for the minimum Hamiltonian cycle;
    :param hc: list containing a starting Hamiltonian cycle that will be replaced with an improved cycle, if reduced.
    :returns: a boolean indicating whether the algorithm has found a better solution."""

    cnt = 0
    edited = False

    while cnt < num_cycle:
        edited = _2opt(g, hc)
        if edited:
            cnt = 0
        else:
            edited = _3opt(g, hc)
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
    for i in range(len(hc) - 2):
        for j in range(i + 1, len(hc) - 1):
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
    for i in range(len(hc) - 3):
        for j in range(i + 1, len(hc) - 2):
            for k in range(j + 1, len(hc) - 1):
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


# ------------------------ GRAPHS FOR TESTING --------------------------------------------------------------------------


def _populate_graph1():
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

    return {usd, gbp, eur, cny, jpy}


def _populate_graph2():
    gbp = Currency('GBP')
    gbp.add_change('BDT', 0.66)
    gbp.add_change('AED', 0.2)
    gbp.add_change('USD', 0.09)
    gbp.add_change('EUR', 0.31)
    gbp.add_change('CNY', 0.05)

    cny = Currency('CNY')
    cny.add_change('GBP', 0.05)
    cny.add_change('EUR', 0.87)
    cny.add_change('ILS', 0.34)
    cny.add_change('JPY', 0.11)

    eur = Currency('EUR')
    eur.add_change('GBP', 0.31)
    eur.add_change('CNY', 0.87)
    eur.add_change('DOP', 0.15)
    eur.add_change('USD', 0.3)

    ils = Currency('ILS')
    ils.add_change('DOP', 0.15)
    ils.add_change('CNY', 0.34)
    ils.add_change('LAB', 0.6)
    ils.add_change('JOD', 0.05)

    dop = Currency('DOP')
    dop.add_change('EUR', 0.15)
    dop.add_change('ILS', 0.15)
    dop.add_change('JOD', 0.11)
    dop.add_change('USD', 0.2)

    aed = Currency('AED')
    aed.add_change('GBP', 0.2)
    aed.add_change('USD', 0.15)
    aed.add_change('JPY', 0.4)
    aed.add_change('ETB', 0.4)
    aed.add_change('BDT', 0.48)

    usd = Currency('USD')
    usd.add_change('AED', 0.15)
    usd.add_change('GBP', 0.09)
    usd.add_change('EUR', 0.3)
    usd.add_change('DOP', 0.2)
    usd.add_change('JPY', 0.43)

    jod = Currency('JOD')
    jod.add_change('DOP', 0.11)
    jod.add_change('ILS', 0.05)
    jod.add_change('LAB', 0.4)

    lab = Currency('LAB')
    lab.add_change('ILS', 0.6)
    lab.add_change('JOD', 0.4)

    etb = Currency('ETB')
    etb.add_change('AED', 0.4)
    etb.add_change('GIP', 0.3)
    etb.add_change('CAD', 0.5)

    gip = Currency('GIP')
    gip.add_change('ETB', 0.3)
    gip.add_change('CAD', 0.25)

    cad = Currency('CAD')
    cad.add_change('ETB', 0.5)
    cad.add_change('GIP', 0.25)
    cad.add_change('JPY', 0.06)
    cad.add_change('BDT', 0.85)

    bdt = Currency('BDT')
    bdt.add_change('GBP', 0.66)
    bdt.add_change('AED', 0.48)
    bdt.add_change('CAD', 0.85)
    bdt.add_change('JPY', 0.12)

    jpy = Currency('JPY')
    jpy.add_change('BDT', 0.12)
    jpy.add_change('CAD', 0.06)
    jpy.add_change('AED', 0.4)
    jpy.add_change('USD', 0.43)
    jpy.add_change('CNY', 0.11)

    return {gbp, cny, eur, ils, dop, aed, usd, jod, lab, etb, gip, cad, bdt, jpy}


def _populate_graph3():
    aed = Currency('AED')
    aed.add_change('AFN', 0.10)
    aed.add_change('ALL', 0.20)
    aed.add_change('AWG', 0.50)

    afn = Currency('AFN')
    afn.add_change('AED', 0.10)
    afn.add_change('AMD', 0.40)
    afn.add_change('AUD', 0.60)
    afn.add_change('ANG', 0.90)
    afn.add_change('AWG', 0.60)

    all_ = Currency('ALL')
    all_.add_change('AMD', 0.30)
    all_.add_change('AED', 0.20)
    all_.add_change('AWG', 0.80)
    all_.add_change('AZN', 0.31)
    all_.add_change('BDT', 0.08)

    amd = Currency('AMD')
    amd.add_change('AWG', 0.70)
    amd.add_change('AFN', 0.40)
    amd.add_change('ALL', 0.30)
    amd.add_change('AUD', 0.12)
    amd.add_change('ARS', 0.48)
    amd.add_change('AOA', 0.30)
    amd.add_change('BHD', 0.01)
    amd.add_change('BAM', 0.06)
    amd.add_change('BDT', 0.1)
    amd.add_change('BBD', 0.23)

    ang = Currency('ANG')
    ang.add_change('AFN', 0.90)
    ang.add_change('ARS', 0.15)
    ang.add_change('AOA', 0.43)
    ang.add_change('AUD', 0.51)
    ang.add_change('CHF', 0.85)

    aoa = Currency('AOA')
    aoa.add_change('AMD', 0.30)
    aoa.add_change('ANG', 0.43)
    aoa.add_change('ARS', 0.05)
    aoa.add_change('BGN', 0.43)
    aoa.add_change('BHD', 0.65)
    aoa.add_change('CHW', 0.82)
    aoa.add_change('CLF', 0.99)

    ars = Currency('ARS')
    ars.add_change('AMD', 0.48)
    ars.add_change('AUD', 0.24)
    ars.add_change('AOA', 0.05)
    ars.add_change('ANG', 0.15)

    aud = Currency('AUD')
    aud.add_change('AFN', 0.6)
    aud.add_change('ANG', 0.51)
    aud.add_change('AMD', 0.12)
    aud.add_change('ARS', 0.24)

    awg = Currency('AWG')
    awg.add_change('AED', 0.50)
    awg.add_change('AFN', 0.60)
    awg.add_change('AMD', 0.70)
    awg.add_change('ALL', 0.80)

    azn = Currency('AZN')
    azn.add_change('ALL', 0.31)
    azn.add_change('BAM', 0.75)
    azn.add_change('BBD', 0.03)
    azn.add_change('BMD', 0.06)
    azn.add_change('BND', 0.48)

    bam = Currency('BAM')
    bam.add_change('BGN', 0.31)
    bam.add_change('AMD', 0.06)
    bam.add_change('AZN', 0.75)
    bam.add_change('BBD', 0.95)
    bam.add_change('BOB', 0.08)
    bam.add_change('BTN', 0.63)

    bbd = Currency('BBD')
    bbd.add_change('AZN', 0.03)
    bbd.add_change('BAM', 0.95)
    bbd.add_change('AMD', 0.23)

    bdt = Currency('BDT')
    bdt.add_change('ALL', 0.08)
    bdt.add_change('AMD', 0.1)

    bgn = Currency('BGN')
    bgn.add_change('BAM', 0.31)
    bgn.add_change('AOA', 0.43)
    bgn.add_change('BHD', 0.03)
    bgn.add_change('BIF', 0.1)
    bgn.add_change('BTN', 0.56)
    bgn.add_change('BRL', 0.08)

    bhd = Currency('BHD')
    bhd.add_change('BGN', 0.03)
    bhd.add_change('AOA', 0.65)
    bhd.add_change('AMD', 0.01)
    bhd.add_change('BIF', 0.15)

    bif = Currency('BIF')
    bif.add_change('BGN', 0.1)
    bif.add_change('BHD', 0.15)

    bmd = Currency('BMD')
    bmd.add_change('AZN', 0.06)
    bmd.add_change('BND', 0.1)
    bmd.add_change('BOV', 0.07)
    bmd.add_change('DZD', 0.59)

    bnd = Currency('BND')
    bnd.add_change('BMD', 0.1)
    bnd.add_change('BOV', 0.45)
    bnd.add_change('AZN', 0.48)
    bnd.add_change('BSD', 0.03)
    bnd.add_change('BWP', 0.73)
    bnd.add_change('CNY', 0.83)
    bnd.add_change('COP', 0.09)

    bob = Currency('BOB')
    bob.add_change('BOV', 0.01)
    bob.add_change('BAM', 0.08)
    bob.add_change('BSD', 0.25)
    bob.add_change('BTN', 0.1)

    bov = Currency('BOV')
    bov.add_change('BMD', 0.07)
    bov.add_change('BND', 0.45)
    bov.add_change('BOB', 0.01)

    brl = Currency('BRL')
    brl.add_change('BGN', 0.08)
    brl.add_change('BTN', 0.82)
    brl.add_change('BSD', 0.93)

    bsd = Currency('BSD')
    bsd.add_change('BRL', 0.93)
    bsd.add_change('BOB', 0.25)
    bsd.add_change('BND', 0.03)

    btn = Currency('BTN')
    btn.add_change('BAM', 0.63)
    btn.add_change('BOB', 0.1)
    btn.add_change('BGN', 0.56)
    btn.add_change('BRL', 0.82)

    bwp = Currency('BWP')
    bwp.add_change('CLF', 0.96)
    bwp.add_change('BZD', 0.25)
    bwp.add_change('BND', 0.73)
    bwp.add_change('COP', 0.96)
    bwp.add_change('CUC', 0.1)

    byn = Currency('BYN')
    byn.add_change('BZD', 0.05)
    byn.add_change('CAD', 0.63)
    byn.add_change('CVE', 0.33)

    bzd = Currency('BZD')
    bzd.add_change('CAD', 0.31)
    bzd.add_change('CLF', 0.1)
    bzd.add_change('BWP', 0.25)
    bzd.add_change('BYN', 0.05)

    cad = Currency('CAD')
    cad.add_change('CDF', 0.89)
    cad.add_change('CHE', 0.06)
    cad.add_change('BZD', 0.31)
    cad.add_change('BYN', 0.63)

    cdf = Currency('CDF')
    cdf.add_change('CHF', 0.07)
    cdf.add_change('CHW', 0.67)
    cdf.add_change('CHE', 0.48)
    cdf.add_change('CAD', 0.89)

    che = Currency('CHE')
    che.add_change('CHW', 0.01)
    che.add_change('CDF', 0.48)
    che.add_change('CLF', 0.9)
    che.add_change('CAD', 0.06)

    chf = Currency('CHF')
    chf.add_change('ANG', 0.85)
    chf.add_change('CHW', 0.71)
    chf.add_change('CDF', 0.07)

    chw = Currency('CHW')
    chw.add_change('AOA', 0.82)
    chw.add_change('CHF', 0.71)
    chw.add_change('CDF', 0.67)
    chw.add_change('CHE', 0.01)

    clf = Currency('CLF')
    clf.add_change('AOA', 0.99)
    clf.add_change('CHE', 0.9)
    clf.add_change('BZD', 0.1)
    clf.add_change('BWP', 0.96)

    clp = Currency('CLP')
    clp.add_change('DZD', 0.45)
    clp.add_change('CNY', 0.32)
    clp.add_change('CRC', 0.07)

    cny = Currency('CNY')
    cny.add_change('BND', 0.83)
    cny.add_change('DZD', 0.83)
    cny.add_change('COP', 0.06)
    cny.add_change('CLP', 0.32)
    cny.add_change('COU', 0.78)

    cop = Currency('COP')
    cop.add_change('BND', 0.09)
    cop.add_change('BWP', 0.96)
    cop.add_change('CUC', 0.1)
    cop.add_change('COU', 0.59)
    cop.add_change('CNY', 0.06)

    cou = Currency('COU')
    cou.add_change('CNY', 0.78)
    cou.add_change('COP', 0.59)
    cou.add_change('CUC', 0.99)
    cou.add_change('DKK', 0.69)

    crc = Currency('CRC')
    crc.add_change('CLP', 0.07)
    crc.add_change('DKK', 0.21)

    cuc = Currency('CUC')
    cuc.add_change('COU', 0.99)
    cuc.add_change('COP', 0.1)
    cuc.add_change('BWP', 0.1)
    cuc.add_change('DOP', 0.58)
    cuc.add_change('DJF', 0.21)

    cup = Currency('CUP')
    cup.add_change('DKK', 0.87)
    cup.add_change('CZK', 0.3)

    cve = Currency('CVE')
    cve.add_change('CZK', 0.99)
    cve.add_change('DJF', 0.77)
    cve.add_change('BYN', 0.33)
    cve.add_change('DOP', 0.09)

    czk = Currency('CZK')
    czk.add_change('CUP', 0.3)
    czk.add_change('DKK', 0.08)
    czk.add_change('DJF', 0.83)
    czk.add_change('CVE', 0.99)

    djf = Currency('DJF')
    djf.add_change('CUC', 0.21)
    djf.add_change('CVE', 0.77)
    djf.add_change('CZK', 0.83)
    djf.add_change('DKK', 0.91)

    dkk = Currency('DKK')
    dkk.add_change('COU', 0.69)
    dkk.add_change('CRC', 0.21)
    dkk.add_change('DJF', 0.91)
    dkk.add_change('CZK', 0.08)
    dkk.add_change('CUP', 0.87)

    dop = Currency('DOP')
    dop.add_change('CUC', 0.58)
    dop.add_change('CVE', 0.09)

    dzd = Currency('DZD')
    dzd.add_change('BMD', 0.59)
    dzd.add_change('CNY', 0.83)
    dzd.add_change('CLP', 0.45)

    return {aed, afn, all_, amd, ang, aoa, ars, aud, awg, azn, bam, bbd, bdt, bgn, bhd, bif, bmd, bnd, bob, bov, brl,
            bsd, btn, bwp, byn, bzd, cad, cdf, che, chf, chw, clf, clp, cny, cop, cou, crc, cuc, cup, cve, czk, djf,
            dkk, dop, dzd}


# -------------- BRUTE FORCE METHODS -----------------------------------------------------------------------------------


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


def excange_tour_brute_force(C):
    """A local search algorithm that takes in input a set of Currency objects and looks for
    an exchange tour of minimal rate."""
    g, V = _create_graph(C)

    min_cost = min_cycle = None
    for hc in _hamiltonian_brute_force(g):
        if min_cost is None or hc[1] < min_cost:
            min_cycle, min_cost = hc
    return min_cycle, min_cost


# --------------------- DRIVER TEST ------------------------------------------------------------------------------------

if __name__ == '__main__':
    def do_local_search(C):
        print('\nLocal Search')
        start_time = datetime.now()
        tour = excange_tour(C)
        end_time = datetime.now()
        print('founded in {}'.format(end_time - start_time))
        print('tour:{}\ncost:{}'.format(tour, get_cost(C, tour)))

    print('-------- GRAPH 1 -----------------')
    # print('\nBrute force:')
    # start_time = datetime.now()
    # print(excange_tour_brute_force(_populate_graph1()))
    # end_time = datetime.now()
    # print('founded in {}'.format(end_time - start_time))

    C1 = _populate_graph1()
    do_local_search(C1)

    print('\n\n------------ GRAPH 2 -----------------')
    # print('\nBrute force:')
    # start_time = datetime.now()
    # print(excange_tour_brute_force(_populate_graph2()))
    # end_time = datetime.now()
    # print('founded in {}'.format(end_time - start_time))

    C2 = _populate_graph2()
    do_local_search(C2)

    print('\n\n------------ GRAPH 3 -----------------')
    # print('\nBrute force:')
    # start_time = datetime.now()
    # print(excange_tour_brute_force(_populate_graph3()))
    # end_time = datetime.now()
    # print('founded in {}'.format(end_time - start_time))

    C3 = _populate_graph3()
    do_local_search(C3)
