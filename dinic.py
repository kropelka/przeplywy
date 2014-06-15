__author__ = 'karoru'


from collections import deque
from numpy import zeros
import networkx as nx
import random
import time


class NetworkFlow:
    def __init__(self):
        self.za = []
        self.wierzcholki = 0
        self.c = None
        self.przeplyw = None
        self.wartosc = 0
    def wylosuj(self, n, m, maks_cap):
        (self.za, self.c) = losowy_graf(n, m, maks_cap)
        self.wierzcholki = n
    def maxflow(self, od, do):
        (self.wartosc, self.przeplyw) = dinic(self.za, self.c, od, do)




def losowy_graf(n, m, maks_cap):
    g = nx.gnm_random_graph(n, m)
    graf = [[]]*n
    c = zeros((n, n))
    for i in range(0, n):
        for j in range(0,n):
            if i < j:
                c[i,j] = random.randint(0, maks_cap)
                c[j,i] = c[i,j]
    for (u,v) in g.edges():
        graf[u].append(v)
    return (graf, c)

step_by_step = False
do_next_step = False


def dinic(graf, c, s, t):
    global do_next_step
    global step_by_step
    kolejka = deque()
    calkowity_przeplyw = 0
    n = len(graf)
    faza = 0
    przeplyw = zeros((n,n))
    while True:
        faza += 1
#        print 'Faza dzialania algorytmu Dinica nr '+str(faza)
        kolejka.appendleft(s)
        dist = [-1]*n
        dist[s] = 0
        while kolejka:
            u = kolejka.pop()
            if step_by_step:
                while not do_next_step:
                    time.sleep(0.001)
                do_next_step = False
            print 'BFS na wierzcholku '+str(u)+', dist['+str(u)+'] = '+str(dist[u])
            for v in graf[u]:
                if dist[v]==-1 and c[u,v] > przeplyw[u,v]:
                    dist[v] = dist[u] + 1
                    kolejka.appendleft(v)
        if dist[t]==-1:
            return (calkowity_przeplyw, przeplyw)
        ograniczenie = sum([c[s,v] for v in graf[s]])
        calkowity_przeplyw += dinic_krok(graf, dist, c, przeplyw, s, t, ograniczenie)

def dinic_krok(graf, dist, c, przeplyw, u, t, limit):
    if limit <=0:
        return 0
    if u==t:
        return limit
    val = 0
    for v in graf[u]:
        res = c[u,v] - przeplyw[u,v]
        if dist[v] == dist[u] + 1 and res>0:
            av = dinic_krok(graf, dist, c, przeplyw, v, t, min(limit -val, res))
            przeplyw[u,v] += av
            przeplyw[v,u] -= av
            val += av
    if val==0:
        dist[u] = -1
    return val


def randomizowana_proba_dinica(n, m, liczba_prob, maks_cap):
    c = zeros((n, n))
    calk_czas = 0
    for i in range(1, liczba_prob):
        (g,c) = losowy_graf(n, m, maks_cap)
        timer = time.clock()
        dinic(g, c, 0, n-1)
        timer = time.clock() - timer
        calk_czas += timer
    return calk_czas/liczba_prob
