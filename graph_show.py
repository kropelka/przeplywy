import sys
import wx
from collections import deque
__author__ = 'karoru'
import time
import networkx as nx
import threading
import Tkinter
import matplotlib
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot


#viewed_graph = nx.DiGraph()

import numpy

class Plotter():
    def __init__(self,fig):
        self.root = Tkinter.Tk()
        self.root.state("zoomed")

        self.fig = fig
        t = threading.Thread(target=self.PlottingThread,args=(fig,))
        t.start()

    def PlottingThread(self,fig):
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.root)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)

        toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg(canvas, self.root)
        toolbar.update()
        canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.root.mainloop()


class SiecPrzeplywowa():
    def __init__(self, wierzcholki):
        self.Widok = nx.DiGraph()
        self.n = wierzcholki
        self.cap = numpy.zeros((wierzcholki, wierzcholki))
        self.flow = numpy.zeros((wierzcholki, wierzcholki))
        self.przed = []
        self.za = []
        self.dist = [] # odległość wierzchołków od źródła w sieci rezydualnej
        self.wierzcholki = set()
        for i in range(wierzcholki):
            self.przed.append([])
        for i in range(wierzcholki):
            self.za.append([])
        self.odleglosc = 0
##        viewed_graph.clear()
#        viewed_graph.add_nodes_from(range(self.n))
#        for i in self.wierzcholki:
#            for v in self.za[i]:
#                viewed_graph.add_edge(i,v)
#        nx.draw(viewed_graph)
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
    def pokaz_przeplyw(self):
        for i in range(0, self.n):
            for j in range(0, self.n):
                print " "+ str(self.flow[i,j]) + " "
    def siec_rezydualna(self):
        res = SiecPrzeplywowa(self.n)
        osiagniete_wierzcholki = deque()
        osiagniete_wierzcholki.appendleft(0)
        for i in range(1, self.n):
            res.dist.append(sys.maxint)
        while osiagniete_wierzcholki:
            u = osiagniete_wierzcholki.pop()
            for v in self.za[u]:
                if(res.dist[u] < res.dist[v] and res.dist[v] <= res.dist[self.n-1] and self.cap[u,v] > self.flow[u,v]):
                    if(res.dist[v]==sys.maxint):
                        osiagniete_wierzcholki.appendleft(v)
                    res.dist[v] = res.dist[u] + 1
                    res.dodaj_krawedz(u,v)
                    res.cap[u,v] = self.cap[u,v] - self.flow[u,v]

            for v in self.przed[u]:
                if(res.dist[u] < res.dist[v] and res.dist[v] <= res.dist[self.n-1] and self.flow[v,u] > 0):
                    if(res.dist[v]==sys.maxint):
                        osiagniete_wierzcholki.appendleft(v)
                    if res.cap[u,v]==0:
                        res.dodaj_krawedz(u,v)
                    res.cap[u,v] = res.cap[u,v] + self.flow[v,u]
#            res.show_on_graph()
        res.odleglosc = res.dist[self.n-1]
        return res

    def mkm(self):
        potwe = [0 for x in range(self.n)]
        potwy = [0 for x in range(self.n)]
        pot = [0 for x in range(self.n)]
        Q = [0 for x in range(self.n)]
        for v in self.wierzcholki: # wyznacz potencjaly wierzcholkow grafu
            potwe[v] = 0
            potwy[v] = 0
            if v == 0:
                potwe[v] = sys.maxint
            else:
                for u in self.przed[v]:
                  potwe[v] = potwe[v] + self.cap[u,v]
            if v == self.n-1:
                potwy[v] = sys.maxint
            else:
                for u in self.za[v]:
                    potwy[v] = potwy[v] + self.cap[v,u]
            pot[v] = min(potwe[v], potwy[v])
            Q[v] = 0
        while len(self.wierzcholki) > 2: # dopoki w sieci rezydualnej sa krawedzie...
            min = sys.maxint
            vmin = 0
            for v in self.wierzcholki:
                if pot[v] < min:
                    min = pot[v]
                    vmin = v
            Q[v] = min
            for u in self.za[v]:
                if Q[v]>0:
                    Q[v] = Q[v] - self.cap[v,u]
                    Q[u] = Q[u] + self.cap[v,u]
                else:
                    break
            Q[v] = min
            for u in self.przed[v]:
                if Q[v]>0:
                    Q[v] = Q[v] - self.cap[u,v]
                    Q[u] = Q[u] - self.cap[v,u]







    def pseudomax(self):
        zerowe_wierzcholki = []
        potwe = [0 for x in range(self.n)]
        potwy = [0 for x in range(self.n)]
        pot = [0 for x in range(self.n)]
        ladunek = [0 for x in range(self.n)]
        for v in self.wierzcholki:
            potwe[v] = 0
            potwy[v] = 0
            if v == 0:
                potwe[v] = sys.maxint
            else:
                for u in self.przed[v]:
                  potwe[v] = potwe[v] + self.cap[u,v]
            if v == self.n-1:
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
                for u in self.przed[v]:
                    potwy[u] = potwy[u] - (self.cap[u, v] - self.flow[u, v])
                    self.za[u].remove(v)
                    self.przed[v].remove(u)
                    if pot[u] != 0:
                        pot[u] = min(potwe[u], potwy[u])
                        if pot[u] == 0:
                            zerowe_wierzcholki.append(u)
                for u in self.za[v]:
                    potwe[u] = potwe[u] - (self.cap[v,u] - self.flow[v, u])
                    self.przed[u].remove(v)
                    self.za[v].remove(u)
                    if pot[u] !=0:
                        pot[u] = min(potwe[u], potwy[u])
                        if pot[u] ==0:
                            zerowe_wierzcholki.append(u)
            if niezerowe_wierzcholki:
                p = sys.maxint
                r = 0
                delta = 0
                for v in niezerowe_wierzcholki:
                    if pot[v] < p:
                        p = pot[v]
                        r = v
                kolejka = deque()
                kolejka.append(r)
                ladunek[r] = p
                debugj = 0
                while True:
                    debugj +=1
                    print 'Przejscie nr '+str(debugj)
                    v = kolejka.pop()
                    potwe[v] -= ladunek[v]
                    potwy[v] -= ladunek[v]
                    pot[v] -= ladunek[v]
                    if pot[v] == 0:
                        zerowe_wierzcholki.append(v)
                    if v == self.n-1:
                        ladunek[v] = 0
                    else:
                        i = 0
                        u = self.za[v][i]
                        while ladunek[v]>0 and u in self.za[v]:
                            if ladunek[u]==0:
                                kolejka.appendleft(u)
                            delta = min(ladunek[v], self.cap[v,u] - self.flow[v,u])
                            self.flow[v,u] = self.flow[v,u] + delta
                            ladunek[v] -= delta
                            ladunek[u] += delta
                            if self.flow[v,u] == self.cap[v,u]:
                                self.za[v].remove(u)
                                self.przed[u].remove(v)
                            if ladunek[v]==0:
                                break
                    if v == self.n-1:
                        break
                kolejka.clear()
                kolejka.appendleft(r)
                ladunek[r] = p
                while True:
                    v = kolejka.pop()
                    i = self.za[v].__iter__()
                    if v != r:
                        potwe[v] -= ladunek[v]
                        potwy[v] -= ladunek[v]
                        pot[v] -= ladunek[v]
                        if pot[v] ==0:
                            zerowe_wierzcholki.append(v)
                    if v==0:
                        ladunek[v]=0
                    else:
                        while ladunek[v]>0 and u in self.przed[v]:
                                if ladunek[u]==0:
                                    kolejka.appendleft(u)
                                delta = min(ladunek[v], self.cap[u,v] - self.flow[u,v])
                                self.flow[u,v] += delta
                                ladunek[v] -= delta
                                ladunek[u] += delta
                                if self.flow[u,v] == self.cap[u,v]:
                                    self.przed[v].remove(u)
                                    self.za[u].remove(v)
                                if ladunek[v] ==0:
                                    break
                    if v==0:
                        break
    def dinic(self):
        for u in self.wierzcholki:
            for v in self.wierzcholki:
                self.flow[u,v] = 0
        while True:
            psa = self.siec_rezydualna()
            if psa.odleglosc < sys.maxint:
                psa.pseudomax()
                for u in psa.wierzcholki:
                    for v in psa.wierzcholki:
                        self.flow[u, v] += psa.flow[u,v]
                        if self.flow[u,v] > self.cap[u,v]:
                            self.flow[v, u] -= self.flow[u, v] - self.cap[u,v]
                            self.flow[u,v] = self.cap[u,v ]
            if self.odleglosc == sys.maxint:
                break



                    












#class OknoGrafu(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent)
#        self.fig = plt.figure()
#        self.canvas = FigureCanvas(self, -1, self.fig)
#        self.przycisk = wx.Button(self, -1, "Refresh")
#        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
#        self.sizer.Add(self.przycisk, 1, wx.RIGHT)
#        self.SetSizer(self.sizer)
#        self.Fit()
#        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.przycisk)
#    def onButtonClick(self, event):
#        self.fig.clear()
#        self.canvas.Refresh()


if __name__ == '__main__':
    fig = matplotlib.pyplot.figure()
    Plotter(fig)
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
    #app = wx.App(False)
    #fr = wx.Frame(None, wx.ID_ANY, "Takie tam")
    #panel = OknoGrafu(fr)
    #siec.show_on_graph()
    #fr.Show()
    #drugasiec = siec.siec_rezydualna()
    #app.MainLoop()
    #print 'Sieci przeplywowe'
    siec.dinic()
    siec.pokaz_przeplyw()
    #drugasiec = siec.siec_rezydualna()
    #drugasiec.pokaz_liste()

