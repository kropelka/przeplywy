# -*- coding: utf-8 -*-
__author__ = 'karoru'


from collections import deque
from numpy import zeros
import networkx as nx
import random
import time
import json

#step_by_step = False
#do_next_step = False



class NetworkFlow(object):
    def __init__(self):
        self.za = []
        self.wierzcholki = 0
        self.c = None
        self.przeplyw = None
        self.wartosc = 0
        self.step_by_step = False
        self.do_next_step = False
        self.zorientowany = False
    def wylosuj(self, n, m, maks_cap, orient=False):
        (self.za, self.c) = self.losowy_graf(n, m, maks_cap, orient)
        self.zorientowany = orient
        self.wierzcholki = n
    def maxflow(self, od, do):
        self.wartosc = self.dinic(self.za, self.c, od, do)
    def print_message(self, message):
        print message
    def losowy_graf(self, n, m, maks_cap, orient):
        g = nx.gnm_random_graph(n, m)
        graf = [ [] for x in range(0, n)]
    #    print str(graf)
        c = zeros((n, n))
        for i in range(0, n):
            for j in range(0,n):
                if i < j: # gererujemy graf nieskierowany
                    c[i,j] = random.randint(0, maks_cap)
                    if orient:
                        c[j,i] = c[i,j]
                    else:
                        c[j,i] = random.randint(0, maks_cap)
        if orient:
            self.zorientowany = True
        #print str(g.edges())
        for (u,v) in g.edges():
    #        print 'Dodajemy wierzcholek'
            (graf[u]).append(v)
            graf[v].append(u)
        #print str(graf)
    #    for u in range(0,n):
    #        for v in graf[u]:
    #            print str(u) + ' -> '+ str(v)
        return (graf, c)



    def dinic(self, graf, c, s, t):
        self.zorientowany = True
        #global do_next_step
        #global step_by_step
        kolejka = deque()
        calkowity_przeplyw = 0
        n = len(graf)
        faza = 0
        przeplyw = zeros((n, n))
        self.przeplyw = przeplyw
        while True:
            faza += 1
            kolejka.appendleft(s)
            dist = [-1]*n
            dist[s] = 0
            while kolejka:
                u = kolejka.pop()
                if self.step_by_step:
                    self.print_message('Faza dzialania algorytmu Dinica nr '+str(faza))
                    self.print_message('')
                    self.print_message('BFS na wierzcholku '+str(u)+', dist['+str(u)+'] = '+str(dist[u]))
                    self.print_message('Zawartosc kolejki: '+str(kolejka))
                    while not self.do_next_step:
                        time.sleep(0.001)
                    self.do_next_step = False
                for v in graf[u]:
                    if dist[v]==-1 and c[u,v] > przeplyw[u,v]: # jezeli wierzcholek nie jest nasycony i nie zostal jeszcze odwiedzony, to dodaj go do mozliwej sciezki
                        dist[v] = dist[u] + 1                  # blokujacej
                        kolejka.appendleft(v)
            if dist[t]==-1: # jezeli nie ma sciezki blokujacej od s do t, to zakoncz
                self.print_message(u"Znaleziono maksymalny przepływ o wartości "+str(calkowity_przeplyw))
                return calkowity_przeplyw
            if self.step_by_step:
                self.print_message(u"Podział sieci na warstwy:")
                for i in range(0, dist[t]+1):
                    tekst = "dist[v] = "+str(i) + " -> "
                    for v in range(n):
                        if dist[v]==i:
                            tekst = tekst + str(v) + " "
                    self.print_message(tekst)

                self.print_message(" ")
            ograniczenie = sum([c[s,v] for v in graf[s]])
            calkowity_przeplyw += self.dinic_krok(graf, dist, c, przeplyw, s, t, ograniczenie) # przepychamy maksymalny mozliwy przeplyw ze zrodla przez sciezki blokujace

    def dinic_krok(self, graf, dist, c, przeplyw, u, t, limit):
        #global step_by_step
        #global do_next_step
        if limit <=0: # jak nie ma przeplywu do przepchniecia, to zakoncz
            return 0
        if u==t:  # jezeli dotarlismy do ujscia, to konczymy
            return limit
        val = 0
        if self.step_by_step:
            self.print_message('Umieszczamy przeplyw '+str(limit)+' w sasiadach wierzcholka '+str(u))
            while not self.do_next_step:
                time.sleep(0.001)
            do_next_step = False
        for v in graf[u]:
            res = c[u,v] - przeplyw[u,v]   # wyznaczamy wartosc rezydualna przeplywu na krawedzi (u,v)
            if dist[v] == dist[u] + 1 and res>0:  # idziemy do nastepnej krawedzi na sciezce blokujacej
                if self.step_by_step:
                    self.print_message('Krawedz '+str(u)+'-'+str(v)+' na sciezce blokujacej')
                    self.print_message('Wywoluje dinic_krok dla s = '+str(v)+' i ograniczenia = '+str(min(limit-val, res)))
                    while not self.do_next_step:
                        time.sleep(0.001)
                av = self.dinic_krok(graf, dist, c, przeplyw, v, t, min(limit-val, res))  # rekurencyjnie umieszczamy tam reszte przeplywu
                przeplyw[u,v] += av
                przeplyw[v,u] -= av
                val += av
        if val==0:
            dist[u] = -1
        return val


    def randomizowana_proba_dinica(self, n, m, liczba_prob, maks_cap, orient=False):
        c = zeros((n, n))
        calk_czas = 0
        for i in range(1, liczba_prob):
            (g,c) = self.losowy_graf(n, m, maks_cap, orient)
            timer = time.clock()
            self.dinic(g, c, 0, n-1)
            timer = time.clock() - timer
            calk_czas += timer
        return calk_czas/liczba_prob

    def open_graph_file(file_name, g, c):
        plik = open(file_name, 'r')
        s = plik.readline()
        liczba_wierzcholkow = int(s)
        for line in plik:
            print 'hello'
