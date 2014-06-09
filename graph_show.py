import sys
import wx
from collections import deque
__author__ = 'karoru'
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

viewed_graph = nx.DiGraph()

import numpy

class SiecPrzeplywowa():
    def __init__(self, wierzcholki):
        self.n = wierzcholki
        self.cap = numpy.zeros((wierzcholki, wierzcholki))
        self.flow = numpy.zeros((wierzcholki, wierzcholki))
        self.przed = []
        self.za = []
        self.wierzcholki = set()
        for i in range(wierzcholki):
            self.przed.append([])
        for i in range(wierzcholki):
            self.za.append([])
    def show_on_graph(self):
        viewed_graph.clear()
        viewed_graph.add_nodes_from(range(self.n))
        for i in self.wierzcholki:
            for v in self.za[i]:
                viewed_graph.add_edge(i,v)
        nx.draw(viewed_graph)
    def dodaj_krawedz(self, pocz, kon):
        self.za[pocz].append(kon)
        self.przed[kon].append(pocz)
        self.wierzcholki.add(pocz)
        self.wierzcholki.add(kon)
    def pokaz_liste(self):
        print 'Ilosc wierzcholkow: '+str(self.n)
        print 'Lista krawedzi:'
        for i, lista in enumerate(self.za):
            for j in lista:
              print str(i)+' -> '+str(j)
    def ustal_pojemnosc(self, u, v, capp):
        self.cap[u, v] = capp
    def siec_rezydualna(self):
        res = SiecPrzeplywowa(self.n)
        dist = [0]
        osiagniete_wierzcholki = deque()
        osiagniete_wierzcholki.appendleft(0)
        for i in range(1, self.n):
            dist.append(sys.maxint)
        while osiagniete_wierzcholki:
            u = osiagniete_wierzcholki.pop()
            for v in self.za[u]:
                if(dist[u] < dist[v] and dist[v] <= dist[self.n-1] and self.cap[u,v] > self.flow[u,v]):
                    if(dist[v]==sys.maxint):
                        osiagniete_wierzcholki.appendleft(v)
                    dist[v] = dist[u] + 1
                    res.dodaj_krawedz(u,v)
                    res.cap[u,v] = self.cap[u,v] - self.flow[u,v]

            for v in self.przed[u]:
                if(dist[u] < dist[v] and dist[v] <= dist[self.n-1] and self.flow[v,u] > 0):
                    if(dist[v]==sys.maxint):
                        osiagniete_wierzcholki.appendleft(v)
                    if res.cap[u,v]==0:
                        res.dodaj_krawedz(u,v)
                    res.cap[u,v] = res.cap[u,v] + self.flow[v,u]
            res.show_on_graph()
        return res

    def pseudomax(self):
        zerowe_wierzcholki = []
        potwe = [0 for x in range(self.n)]
        potwy = [0 for x in range(self.n)]
        pot = [0 for x in range(self.n)]
        ladunek = [0 for x in range(self.n)]
        for v in self.wierzcholki:
            potwe[v] = 0
            potwy[v] = 0
            if u == 0:
                potwe[v] = sys.maxint
            else:
                for u in self.przed[v]:
                  potwe[v] = potwe[v] + self.cap[u,v]
            if u == self.n-1:
                potwy[v] = sys.maxint
            else:
                for u in self.za[v]:
                    potwy[v] = potwy[v] + self.cap[v,u]
            pot[v] = min(potwe[v], potwy[v])
            ladunek[v] = 0
            if pot[v]==0:
                zerowe_wierzcholki.append(v)
        niezerowe_wierzcholki = self.wierzcholki.copy()
        while niezerowe_wierzcholki:
            while zerowe_wierzcholki:
                v = zerowe_wierzcholki.pop()
                niezerowe_wierzcholki.remove(v)





class OknoGrafu(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.przycisk = wx.Button(self, -1, "Refresh")
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.przycisk, 1, wx.RIGHT)
        self.SetSizer(self.sizer)
        self.Fit()
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.przycisk)
    def onButtonClick(self, event):
        self.fig.clear()
        self.canvas.Refresh()


if __name__ == '__main__':
    matplotlib.use('WxAgg')
    siec = SiecPrzeplywowa(7)
    siec.dodaj_krawedz(0,1)
    siec.dodaj_krawedz(1,6)
    siec.dodaj_krawedz(0,2)
    siec.dodaj_krawedz(2,5)
    siec.dodaj_krawedz(5,6)
    siec.dodaj_krawedz(0,4)
    siec.dodaj_krawedz(4,3)
    siec.dodaj_krawedz(3,6)
    siec.dodaj_krawedz(5,3)
    siec.dodaj_krawedz(2,4)
    siec.dodaj_krawedz(2,3)
    siec.dodaj_krawedz(3,2)
    siec.ustal_pojemnosc(0,1,1)
    siec.ustal_pojemnosc(1,6,2)
    siec.ustal_pojemnosc(0,2,1)
    siec.ustal_pojemnosc(2,5,2)
    siec.ustal_pojemnosc(5,6,2)
    siec.ustal_pojemnosc(0,4,2)
    siec.ustal_pojemnosc(4,3,2)
    siec.ustal_pojemnosc(3,6,1)
    siec.ustal_pojemnosc(2,4,1)
    siec.ustal_pojemnosc(2,3,1)
    siec.ustal_pojemnosc(3,2,1)
    siec.ustal_pojemnosc(5,3,2)
    app = wx.App(False)
    fr = wx.Frame(None, wx.ID_ANY, "Takie tam")
    panel = OknoGrafu(fr)
    siec.show_on_graph()
    fr.Show()
    drugasiec = siec.siec_rezydualna()
    app.MainLoop()
    print 'Sieci przeplywowe'

    drugasiec = siec.siec_rezydualna()
    drugasiec.pokaz_liste()

