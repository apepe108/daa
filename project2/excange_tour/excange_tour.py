import random
import math

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
        edited = _2_3opt(g, hc, num_cycle=math.log2(g.vertex_count()))

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


def _2_3opt(g, hc, num_cycle):
    """Call the 2 opt algorithm until you get a 2opt-optimal solution, then call the 3-opt algorithm until you get an
    optimal 3-opt solution. If there are no more improvements, it re-executes on the rotated cycle and, if there are no
    improvements here, it returns the cycle found and its cost.

    :param g: the graph on which to search for the minimum Hamiltonian cycle;
    :param hc: list containing a starting Hamiltonian cycle that will be replaced with an improved cycle, if reduced.
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


def _populate_graph4():
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
    ang.add_change('CHW', 0.17)

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
    bgn.add_change('DOP', 0.06)
    bgn.add_change('CHE', 0.72)

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
    bnd.add_change('DKK', 0.18)

    bob = Currency('BOB')
    bob.add_change('BOV', 0.01)
    bob.add_change('BAM', 0.08)
    bob.add_change('BSD', 0.25)
    bob.add_change('BTN', 0.1)

    bov = Currency('BOV')
    bov.add_change('BMD', 0.07)
    bov.add_change('BND', 0.45)
    bov.add_change('BOB', 0.01)
    bov.add_change('DZD', 0.76)

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
    byn.add_change('GEL', 0.32)
    byn.add_change('FJD', 0.02)
    byn.add_change('GHS', 0.83)
    byn.add_change('GNF', 0.08)
    byn.add_change('GTQ', 0.71)

    bzd = Currency('BZD')
    bzd.add_change('CAD', 0.31)
    bzd.add_change('CLF', 0.1)
    bzd.add_change('BWP', 0.25)
    bzd.add_change('BYN', 0.05)
    bzd.add_change('CUC', 0.44)

    cad = Currency('CAD')
    cad.add_change('CDF', 0.89)
    cad.add_change('CHE', 0.06)
    cad.add_change('BZD', 0.31)
    cad.add_change('BYN', 0.63)
    cad.add_change('CLF', 0.77)

    cdf = Currency('CDF')
    cdf.add_change('CHF', 0.07)
    cdf.add_change('CHW', 0.67)
    cdf.add_change('CHE', 0.48)
    cdf.add_change('CAD', 0.89)
    cdf.add_change('ERN', 0.99)
    cdf.add_change('ETB', 0.1)
    cdf.add_change('FKP', 0.65)
    cdf.add_change('GEL', 0.05)

    che = Currency('CHE')
    che.add_change('CHW', 0.01)
    che.add_change('CDF', 0.48)
    che.add_change('CLF', 0.9)
    che.add_change('CAD', 0.06)
    che.add_change('BGN', 0.72)

    chf = Currency('CHF')
    chf.add_change('ANG', 0.85)
    chf.add_change('CHW', 0.71)
    chf.add_change('CDF', 0.07)
    chf.add_change('HNL', 0.34)
    chf.add_change('ERN', 0.07)

    chw = Currency('CHW')
    chw.add_change('AOA', 0.82)
    chw.add_change('CHF', 0.71)
    chw.add_change('CDF', 0.67)
    chw.add_change('CHE', 0.01)
    chw.add_change('ANG', 0.17)

    clf = Currency('CLF')
    clf.add_change('AOA', 0.99)
    clf.add_change('CHE', 0.9)
    clf.add_change('BZD', 0.1)
    clf.add_change('BWP', 0.96)
    clf.add_change('CAD', 0.77)

    clp = Currency('CLP')
    clp.add_change('DZD', 0.45)
    clp.add_change('CNY', 0.32)
    clp.add_change('CRC', 0.07)
    clp.add_change('JMD', 0.04)
    clp.add_change('ISK', 0.21)

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
    crc.add_change('CUP', 0.1)
    crc.add_change('ILS', 0.9)
    crc.add_change('KHR', 0.86)
    crc.add_change('JMD', 0.79)

    cuc = Currency('CUC')
    cuc.add_change('COU', 0.99)
    cuc.add_change('COP', 0.1)
    cuc.add_change('BWP', 0.1)
    cuc.add_change('DOP', 0.58)
    cuc.add_change('DJF', 0.21)
    cuc.add_change('BZD', 0.44)

    cup = Currency('CUP')
    cup.add_change('DKK', 0.87)
    cup.add_change('CZK', 0.3)
    cup.add_change('ILS', 0.06)
    cup.add_change('JPY', 0.29)
    cup.add_change('IDR', 0.65)
    cup.add_change('CRC', 0.1)

    cve = Currency('CVE')
    cve.add_change('CZK', 0.99)
    cve.add_change('DJF', 0.77)
    cve.add_change('BYN', 0.33)
    cve.add_change('DOP', 0.09)
    cve.add_change('GNF', 0.12)
    cve.add_change('GIP', 0.39)
    cve.add_change('GTQ', 0.5)

    czk = Currency('CZK')
    czk.add_change('CUP', 0.3)
    czk.add_change('DKK', 0.08)
    czk.add_change('DJF', 0.83)
    czk.add_change('CVE', 0.99)
    czk.add_change('GTQ', 0.06)
    czk.add_change('HKD', 0.21)
    czk.add_change('IDR', 0.34)
    czk.add_change('HUF', 0.05)
    czk.add_change('HTG', 0.78)
    czk.add_change('KWD', 0.41)

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
    dkk.add_change('BND', 0.18)

    dop = Currency('DOP')
    dop.add_change('CUC', 0.58)
    dop.add_change('CVE', 0.09)
    dop.add_change('BGN', 0.06)

    dzd = Currency('DZD')
    dzd.add_change('BMD', 0.59)
    dzd.add_change('CNY', 0.83)
    dzd.add_change('CLP', 0.45)
    dzd.add_change('BOV', 0.76)

    egp = Currency('EGP')
    egp.add_change('HNL', 0.55)
    egp.add_change('ERN', 0.08)
    egp.add_change('ETB', 0.47)
    egp.add_change('MVR', 0.14)
    egp.add_change('MRU', 0.31)

    ern = Currency('ERN')
    ern.add_change('CHF', 0.07)
    ern.add_change('HNL', 0.38)
    ern.add_change('EGP', 0.08)
    ern.add_change('ETB', 0.73)
    ern.add_change('CDF', 0.79)

    etb = Currency('ETB')
    etb.add_change('EGP', 0.47)
    etb.add_change('ERN', 0.73)
    etb.add_change('CDF', 0.1)
    etb.add_change('FKP', 0.7)
    etb.add_change('GMD', 0.94)
    etb.add_change('FJD', 0.85)
    etb.add_change('MRU', 0.03)
    etb.add_change('MMK', 0.11)

    fjd = Currency('FJD')
    fjd.add_change('ETB', 0.85)
    fjd.add_change('GMD', 0.03)
    fjd.add_change('BYN', 0.02)
    fjd.add_change('GHS', 0.55)
    fjd.add_change('MMK', 0.18)
    fjd.add_change('MDL', 0.61)

    fkp = Currency('FKP')
    fkp.add_change('CDF', 0.65)
    fkp.add_change('ETB', 0.7)
    fkp.add_change('GMD', 0.39)
    fkp.add_change('GEL', 0.62)

    gel = Currency('GEL')
    gel.add_change('CDF', 0.05)
    gel.add_change('FKP', 0.62)
    gel.add_change('GMD', 0.73)
    gel.add_change('GNF', 0.1)
    gel.add_change('BYN', 0.32)

    ghs = Currency('GHS')
    ghs.add_change('FJD', 0.55)
    ghs.add_change('BYN', 0.83)
    ghs.add_change('GNF', 0.68)
    ghs.add_change('GIP', 0.09)
    ghs.add_change('MDL', 0.73)

    gip = Currency('GIP')
    gip.add_change('GHS', 0.09)
    gip.add_change('GMD', 0.85)
    gip.add_change('GNF', 0.39)
    gip.add_change('CVE', 0.39)
    gip.add_change('GYD', 0.01)
    gip.add_change('MAD', 0.16)
    gip.add_change('LYD', 0.07)
    gip.add_change('LSL', 0.67)

    gmd = Currency('GMD')
    gmd.add_change('ETB', 0.94)
    gmd.add_change('FJD', 0.03)
    gmd.add_change('GIP', 0.85)
    gmd.add_change('GEL', 0.73)
    gmd.add_change('FKP', 0.39)

    gnf = Currency('GNF')
    gnf.add_change('BYN', 0.08)
    gnf.add_change('GEL', 0.1)
    gnf.add_change('GHS', 0.68)
    gnf.add_change('GIP', 0.39)
    gnf.add_change('GYD', 0.38)
    gnf.add_change('GTQ', 0.05)
    gnf.add_change('CVE', 0.12)

    gtq = Currency('GTQ')
    gtq.add_change('GNF', 0.05)
    gtq.add_change('GYD', 0.07)
    gtq.add_change('HKD', 0.1)
    gtq.add_change('CZK', 0.06)
    gtq.add_change('CVE', 0.5)
    gtq.add_change('BYN', 0.71)

    gyd = Currency('GYD')
    gyd.add_change('GIP', 0.01)
    gyd.add_change('GNF', 0.28)
    gyd.add_change('GTQ', 0.07)
    gyd.add_change('HKD', 0.53)
    gyd.add_change('HRK', 0.3)
    gyd.add_change('HTG', 0.98)
    gyd.add_change('LKR', 0.2)

    hkd = Currency('HKD')
    hkd.add_change('GYD', 0.53)
    hkd.add_change('GTQ', 0.1)
    hkd.add_change('CZK', 0.21)
    hkd.add_change('HRK', 0.66)

    hnl = Currency('HNL')
    hnl.add_change('CHF', 0.34)
    hnl.add_change('EGP', 0.55)
    hnl.add_change('ERN', 0.38)

    hrk = Currency('HRK')
    hrk.add_change('KGS', 0.14)
    hrk.add_change('KRW', 0.51)
    hrk.add_change('KWD', 0.6)
    hrk.add_change('HKD', 0.66)
    hrk.add_change('GYD', 0.3)
    hrk.add_change('LSL', 0.95)
    hrk.add_change('LKR', 0.14)
    hrk.add_change('KZT', 0.28)
    hrk.add_change('LBP', 0.51)

    htg = Currency('HTG')
    htg.add_change('CZK', 0.78)
    htg.add_change('GYD', 0.98)
    htg.add_change('KGS', 0.06)
    htg.add_change('KWD', 0.17)

    huf = Currency('HUF')
    huf.add_change('IDR', 0.21)
    huf.add_change('CZK', 0.05)
    huf.add_change('KWD', 0.13)
    huf.add_change('KRW', 0.9)
    huf.add_change('JOD', 0.36)

    idr = Currency('IDR')
    idr.add_change('CUP', 0.65)
    idr.add_change('CZK', 0.34)
    idr.add_change('HUF', 0.21)
    idr.add_change('KRW', 0.15)
    idr.add_change('JOD', 0.5)
    idr.add_change('INR', 0.12)
    idr.add_change('IQD', 0.88)

    ils = Currency('ILS')
    ils.add_change('CUP', 0.06)
    ils.add_change('CRC', 0.9)
    ils.add_change('IRR', 0.06)
    ils.add_change('IQD', 0.65)

    inr = Currency('INR')
    inr.add_change('IDR', 0.12)
    inr.add_change('JOD', 0.18)
    inr.add_change('KPW', 0.20)
    inr.add_change('IQD', 0.01)

    iqd = Currency('IQD')
    iqd.add_change('ILS', 0.75)
    iqd.add_change('IDR', 0.88)
    iqd.add_change('INR', 0.01)
    iqd.add_change('JPY', 0.68)
    iqd.add_change('KHR', 0.21)

    irr = Currency('IRR')
    irr.add_change('ILS', 0.06)
    irr.add_change('KHR', 0.71)
    irr.add_change('JMD', 0.73)

    isk = Currency('ISK')
    isk.add_change('CLP', 0.21)
    isk.add_change('JMD', 0.56)
    isk.add_change('KHR', 0.88)
    isk.add_change('KMF', 0.7)

    jmd = Currency('JMD')
    jmd.add_change('CLP', 0.04)
    jmd.add_change('CRC', 0.79)
    jmd.add_change('IRR', 0.73)
    jmd.add_change('KES', 0.81)
    jmd.add_change('ISK', 0.56)

    jod = Currency('JOD')
    jod.add_change('INR', 0.18)
    jod.add_change('IDR', 0.5)
    jod.add_change('HUF', 0.36)
    jod.add_change('KRW', 0.67)
    jod.add_change('KPW', 0.16)
    jod.add_change('JPY', 0.13)

    jpy = Currency('JPY')
    jpy.add_change('KES', 0.08)
    jpy.add_change('IQD', 0.68)
    jpy.add_change('CUP', 0.29)
    jpy.add_change('JOD', 0.13)
    jpy.add_change('KPW', 0.17)

    kes = Currency('KES')
    kes.add_change('JMD', 0.81)
    kes.add_change('JPY', 0.08)
    kes.add_change('KMF', 0.36)

    kgs = Currency('KGS')
    kgs.add_change('KRW', 0.29)
    kgs.add_change('KWD', 0.99)
    kgs.add_change('HTG', 0.06)
    kgs.add_change('HRK', 0.14)

    khr = Currency('KHR')
    khr.add_change('KMF', 0.67)
    khr.add_change('ISK', 0.88)
    khr.add_change('IRR', 0.71)
    khr.add_change('CRC', 0.86)
    khr.add_change('IQD', 0.21)
    khr.add_change('KPW', 0.99)

    kmf = Currency('KMF')
    kmf.add_change('ISK', 0.7)
    kmf.add_change('KES', 0.36)
    kmf.add_change('KHR', 0.67)

    kpw = Currency('KPW')
    kpw.add_change('JPY', 0.17)
    kpw.add_change('INR', 0.20)
    kpw.add_change('JOD', 0.16)
    kpw.add_change('KRW', 0.1)
    kpw.add_change('KHR', 0.99)

    krw = Currency('KRW')
    krw.add_change('KPW', 0.1)
    krw.add_change('JOD', 0.67)
    krw.add_change('IDR', 0.15)
    krw.add_change('HUF', 0.9)
    krw.add_change('KWD', 0.12)
    krw.add_change('HRK', 0.51)
    krw.add_change('KGS', 0.29)

    kwd = Currency('KWD')
    kwd.add_change('KRW', 0.12)
    kwd.add_change('HUF', 0.13)
    kwd.add_change('CZK', 0.41)
    kwd.add_change('HTG', 0.17)
    kwd.add_change('HRK', 0.6)
    kwd.add_change('KGS', 0.99)

    kyd = Currency('KYD')
    kyd.add_change('KRW', 0.96)
    kyd.add_change('KGS', 0.4)
    kyd.add_change('LBP', 0.18)
    kyd.add_change('KZT', 0.74)

    kzt = Currency('KZT')
    kzt.add_change('KYD', 0.74)
    kzt.add_change('LBP', 0.63)
    kzt.add_change('HRK', 0.28)
    kzt.add_change('LAK', 0.04)
    kzt.add_change('MYR', 0.29)
    kzt.add_change('MOP', 0.15)

    lak = Currency('LAK')
    lak.add_change('KZT', 0.04)
    lak.add_change('LBP', 0.75)
    lak.add_change('LKR', 0.16)
    lak.add_change('LRD', 0.13)

    lbp = Currency('LBP')
    lbp.add_change('KYD', 0.18)
    lbp.add_change('HRK', 0.51)
    lbp.add_change('LAK', 0.75)
    lbp.add_change('KZT', 0.63)

    lkr = Currency('LKR')
    lkr.add_change('LAK', 0.16)
    lkr.add_change('HRK', 0.14)
    lkr.add_change('GYD', 0.2)
    lkr.add_change('LRD', 0.31)

    lrd = Currency('LRD')
    lrd.add_change('LAK', 0.13)
    lrd.add_change('LKR', 0.31)
    lrd.add_change('LSL', 0.09)
    lrd.add_change('LYD', 0.19)
    lrd.add_change('MYR', 0.49)

    lsl = Currency('LSL')
    lsl.add_change('GIP', 0.67)
    lsl.add_change('MAD', 0.9)
    lsl.add_change('LYD', 0.3)
    lsl.add_change('LRD', 0.09)
    lsl.add_change('HRK', 0.95)

    lyd = Currency('LYD')
    lyd.add_change('LRD', 0.19)
    lyd.add_change('LSL', 0.3)
    lyd.add_change('GIP', 0.07)
    lyd.add_change('MAD', 0.76)
    lyd.add_change('MYR', 0.88)

    mad = Currency('MAD')
    mad.add_change('GIP', 0.16)
    mad.add_change('LSL', 0.9)
    mad.add_change('LYD', 0.76)
    mad.add_change('MYR', 0.03)
    mad.add_change('MGA', 0.14)
    mad.add_change('MKD', 0.26)
    mad.add_change('MDL', 0.46)

    mdl = Currency('MDL')
    mdl.add_change('MAD', 0.46)
    mdl.add_change('GHS', 0.73)
    mdl.add_change('FJD', 0.61)
    mdl.add_change('MMK', 0.01)

    mga = Currency('MGA')
    mga.add_change('MAD', 0.14)
    mga.add_change('MMK', 0.8)
    mga.add_change('MXN', 0.27)
    mga.add_change('MXV', 0.66)

    mkd = Currency('MKD')
    mkd.add_change('MYR', 0.17)
    mkd.add_change('MAD', 0.26)
    mkd.add_change('MMK', 0.71)
    mkd.add_change('MNT', 0.14)
    mkd.add_change('MWK', 0.49)

    mmk = Currency('MMK')
    mmk.add_change('MNT', 0.67)
    mmk.add_change('MKD', 0.71)
    mmk.add_change('MGA', 0.8)
    mmk.add_change('MDL', 0.01)
    mmk.add_change('FJD', 0.18)
    mmk.add_change('ETB', 0.11)
    mmk.add_change('MRU', 0.08)
    mmk.add_change('MVR', 0.17)

    mnt = Currency('MNT')
    mnt.add_change('MMK', 0.67)
    mnt.add_change('MKD', 0.14)
    mnt.add_change('MXN', 0.4)
    mnt.add_change('MWK', 0.77)
    mnt.add_change('MVR', 0.16)
    mnt.add_change('MRU', 0.28)

    mop = Currency('MOP')
    mop.add_change('KZT', 0.15)
    mop.add_change('MUR', 0.57)
    mop.add_change('MXV', 0.44)

    mru = Currency('MRU')
    mru.add_change('EGP', 0.31)
    mru.add_change('MVR', 0.59)
    mru.add_change('MNT', 0.28)
    mru.add_change('MMK', 0.08)
    mru.add_change('ETB', 0.03)

    mur = Currency('MUR')
    mur.add_change('MVR', 0.73)
    mur.add_change('MWK', 0.6)
    mur.add_change('MOP', 0.57)

    mvr = Currency('MVR')
    mvr.add_change('EGP', 0.14)
    mvr.add_change('MRU', 0.59)
    mvr.add_change('MMK', 0.17)
    mvr.add_change('MNT', 0.16)
    mvr.add_change('MWK', 0.94)
    mvr.add_change('MUR', 0.73)

    mwk = Currency('MWK')
    mwk.add_change('MNT', 0.77)
    mwk.add_change('MKD', 0.49)
    mwk.add_change('MXN', 0.26)
    mwk.add_change('MUR', 0.6)
    mwk.add_change('MVR', 0.94)

    mxn = Currency('MXN')
    mxn.add_change('MXV', 0.19)
    mxn.add_change('MGA', 0.27)
    mxn.add_change('MNT', 0.4)
    mxn.add_change('MWK', 0.26)

    mxv = Currency('MXV')
    mxv.add_change('MYR', 0.26)
    mxv.add_change('MGA', 0.66)
    mxv.add_change('MXN', 0.19)
    mxv.add_change('MOP', 0.44)

    myr = Currency('MYR')
    myr.add_change('KZT', 0.29)
    myr.add_change('LRD', 0.49)
    myr.add_change('LYD', 0.88)
    myr.add_change('MAD', 0.03)
    myr.add_change('MKD', 0.17)
    myr.add_change('MXV', 0.26)

    return {aed, afn, all_, amd, ang, aoa, ars, aud, awg, azn, bam, bbd, bdt, bgn, bhd, bif, bmd, bnd, bob, bov, brl,
            bsd, btn, bwp, byn, bzd, cad, cdf, che, chf, chw, clf, clp, cny, cop, cou, crc, cuc, cup, cve, czk, djf,
            dkk, dop, dzd, egp, ern, etb, fjd, fkp, gel, ghs, gip, gmd, gnf, gtq, gyd, hkd, hnl, hrk, htg, huf, idr,
            ils, inr, iqd, irr, isk, jmd, jod, jpy, kes, kgs, khr, kmf, kpw, krw, kwd, kyd, kzt, lak, lbp, lkr, lrd,
            lsl, lyd, mad, mdl, mga, mkd, mmk, mnt, mop, mru, mur, mvr, mwk, mxn, mxv, myr}


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

    print('\n\n------------ GRAPH 4 -----------------')
    # print('\nBrute force:')
    # start_time = datetime.now()
    # print(excange_tour_brute_force(_populate_graph3()))
    # end_time = datetime.now()
    # print('founded in {}'.format(end_time - start_time))

    C4 = _populate_graph4()
    do_local_search(C4)
