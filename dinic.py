__author__ = 'karoru'


from collections import deque
from numpy import zeros

def dinic(graf, c, s, t):
    kolejka = deque()
    calkowity_przeplyw = 0
    n = len(graf)
    faza = 0
    przeplyw = zeros((n,n))
    while True:
        faza += 1
        print 'Faza dzialania algorytmu Dinica nr '+str(faza)
        kolejka.appendleft(s)
        dist = [-1]*n
        dist[s] = 0
        while kolejka:
            u = kolejka.pop()
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

def graf