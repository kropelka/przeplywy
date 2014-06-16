# -*- coding: utf-8 -*-
__author__ = 'karoru'
import sys
import math
from gi.repository import Gtk
import dinic
import networkx as nx
from matplotlib import use as mpluse
mpluse('GTK3Agg')
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
import matplotlib.pyplot as plt
import numpy
import thread
import glib
f = plt.figure()

class ViewableNetworkFlow(dinic.NetworkFlow):
    layout = {}
    def show(self, reset_layout):
        plt.hold(False)
        g = nx.Graph()
        etykiety = {}
        for u in range(0, self.wierzcholki):
            g.add_nodes_from(range(self.wierzcholki))
        for u in range(0,self.wierzcholki):
            for v in self.za[u]:
                if self.przeplyw == None:
                    etykiety[(u, v)] = str(self.c[u,v])
                else:
                    etykiety[(u, v)] = str(self.przeplyw[u,v]) + "/" + str(self.c[u,v])
                g.add_edge(u, v)
        print str(etykiety)
        if (reset_layout==True or not(self.layout)):
            self.layout = nx.spring_layout(g)
        nx.draw(g, pos=self.layout)
        nx.draw_networkx_edge_labels(g, pos=self.layout, edge_labels=etykiety)
        f.canvas.draw()

class GraphTesting:
    def stat_show(self, t, s1, s2, title1, title2, titlex):
        ax = f.add_subplot(2, 1, 1)
        ax.set_title(title1)
        ax.set_xlabel(titlex)
        ax.plot(t, s1)
        ax= f.add_subplot(2,1,2)
        ax.set_title(title2)
        ax.set_xlabel(titlex)
        ax.plot(t, s2)
        f.canvas.draw()

    def const_v(self, n, maks_cap, tries):
        max_e = int(n*(n-1)/2)
        results = max_e * [0.0]
        results_by_t = int(n*(n-1)/2) * [0.0]
        #t = numpy.arange(0, n, 1)
        t = [float(x) for x in range(0,int(n*(n-1)/2))]
        progress_bar = app.builder.get_object("test_progress")
        progress_bar.set_pulse_step(1.0/max_e)
        progress_bar.set_fraction(0.0)
        for j in range(3, int(n*(n-1)/2)):
            calc_time = dinic.randomizowana_proba_dinica(n, j, tries, maks_cap)
            results[j] = calc_time
            if j>3:
                results[j] = results[j]/results[3]
            results_by_t[j] = results[j] /j
            #s = results[t]
            progress_bar.pulse()
            while Gtk.events_pending():
                Gtk.main_iteration()
        self.stat_show(t, results, results_by_t, r'$T(|E|)$ przy $|V|=$const', r'$T(|E|)/|E|$', r'$|E|$')
        return results
    def const_e(self, n, maks_cap, tries):
        ax = f.add_subplot(2, 1, 1)
        seq = []
        i = 1
        while len(seq) <= n:
            seq.extend(i*[i+1])
            i += 1
        min_v = seq[n]+1
        t = []
        results = []
        results_by_t2 = []
        first_y = 0
        progress_bar = app.builder.get_object("test_progress")
        progress_bar.set_pulse_step(1.0/(n-min_v))
        progress_bar.set_fraction(0.0)
        for j in range(min_v, n):
            calc_time = dinic.randomizowana_proba_dinica(j, n, tries, maks_cap)
            t.append(float(j))
            if j==min_v:
                first_y = calc_time
                results.append(calc_time)
            else:
                results.append(calc_time/first_y)
            results_by_t2.append(calc_time/(first_y*j))
            progress_bar.pulse()
            while Gtk.events_pending():
                Gtk.main_iteration()
        self.stat_show(t, results, results_by_t2, r'$T(|V|)$ przy $|E|=$const', r'$T(|V|)/|V|$', r'$|V|$')



    def few_edges(self, n, maks_cap, tries):
        progress_bar = app.builder.get_object("test_progress")
        progress_bar.set_pulse_step(1.0/n)
        progress_bar.set_fraction(0.0)
        t = [float(x) for x in range(0, n)]
        results = [0.0 for x in range(0, n)]
        results_by_t2 = [0.0 for x in range(0, n)]
        for j in range(3, n):
            calc_time = dinic.randomizowana_proba_dinica(j, j, tries, maks_cap)
            results[j] = calc_time
            if j>3:
                results[j] = results[j]/results[3]
            results_by_t2[j] = results[j]/(j*j)
            progress_bar.pulse()
            while Gtk.events_pending():
                Gtk.main_iteration()
        self.stat_show(t, results, results_by_t2, r'$T(|V|)$ przy $|E| = O(|V|)$', r'$T(|V|)/|V|^2$', r'$|V|$')

    def many_edges(self, n, maks_cap, tries):
        progress_bar = app.builder.get_object("test_progress")
        progress_bar.set_pulse_step(1.0/n)
        progress_bar.set_fraction(0.0)
        t = [float(x) for x in range(0, n)]
        results = [0.0 for x in range(0, n)]
        results_by_t3 = [0.0 for x in range(0, n)]
        for j in range(3, n):
            calc_time = dinic.randomizowana_proba_dinica(j, j*j/2, tries, maks_cap)
            results[j] = calc_time
            if j>3:
                results[j] = results[j]/results[3]
            results_by_t3[j] = results[j]/(j*j*j)
            progress_bar.pulse()
            while Gtk.events_pending():
                Gtk.main_iteration()
        self.stat_show(t, results, results_by_t3, r'$T(|V|)$ przy $|E| = \Omega(|V|^2)$', r'$T(|V|)/|V|^3$', r'$|V|$')


class UIHandler:
    def onDeleteWindow(self, *args):
        box = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION, flags = Gtk.DialogFlags.MODAL, buttons = Gtk.ButtonsType.YES_NO,
                                message_format = u"Czy na pewno chcesz zakończyć pracę programu?", )
        response = box.run()
        box.destroy()
        print str(response)
        if response == Gtk.ResponseType.YES:
            Gtk.main_quit(*args)

    def onQuit(self, menubar):
        box = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION, flags = Gtk.DialogFlags.MODAL, buttons = Gtk.ButtonsType.YES_NO,
                                message_format = u"Czy na pewno chcesz zakończyć pracę programu?", )
        response = box.run()
        box.destroy()
        print str(response)
        if response == Gtk.ResponseType.YES:
            Gtk.main_quit()

    def onGraphShowButton(self, button):
        current_network.show(False)

    def onRandomGraphButton(self, button):
        choice_dialog = app.builder.get_object("random_network_dialog")
        response = choice_dialog.run()
        v = app.builder.get_object("vertices_box").get_value_as_int()
        e = app.builder.get_object("edges_box").get_value_as_int()
        max_cap = app.builder.get_object("maxcap_box").get_value_as_int()
        choice_dialog.hide()
        if response == 1:
            current_network.wylosuj(v, e, max_cap)

    def onnextStepClicked(self, widget):
        dinic.do_next_step = True

    def onBigGraphTest(self, menupos):
        mode_dialog = app.builder.get_object("testing_dialog")
        response = mode_dialog.run()
        v = int(app.builder.get_object("test_vertices").get_text())
        e = int(app.builder.get_object("test_edges").get_text())
        tries = int(app.builder.get_object("no_tries").get_text())
        max_cap = int(app.builder.get_object("max_test_cap").get_text())
        testtype_choice = app.builder.get_object("test_type").get_active()
        if response == 1:
            which_one = { 0: lambda: GraphTesting().const_v(v, max_cap, tries),
                            1: lambda:GraphTesting().const_e(e, max_cap, tries),
                            2: lambda:GraphTesting().few_edges(v, max_cap, tries),
                            3: lambda:GraphTesting().many_edges(v, max_cap, tries)}
            which_one[testtype_choice]()
        mode_dialog.hide()
    def onToggleStepByStep(self, checkbox, data=None):
        if checkbox.get_active():
            dinic.step_by_step = True
            print 'Wlaczono prace krokowa!'
        else:
            dinic.step_by_step = False


    def onMaxFlowButton(self, button):
        source = int(app.builder.get_object("source_entry").get_text())
        target = int(app.builder.get_object("target_entry").get_text())
        if source == target:
            box = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING, buttons = Gtk.ButtonsType.OK,
                                    message_format = u"Przepływ nie może kończyć i zaczynać się w tym samym wierzchołku.")
            box.run()
            box.destroy()
        else:
            thread.start_new_thread(current_network.maxflow, (source, target))




class DinicGTK:
    def update_textfield(self, stream, cond):
        print "Dupa"
        if cond == glib.IO_IN:
            char = stream.read(1)
            self.textbuff.insert_at_cursor(char)
            return True
        else:
            return False

    def __init__(self):
        self.gladefile = "sieci_gui.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(UIHandler())
        self.window = self.builder.get_object("main_window")
        self.window.connect("delete-event", UIHandler().onDeleteWindow)
        self.canvas = FigureCanvas(f)
        self.canvas.set_size_request(1000, 800)
        self.builder.get_object("graphscreen").add_with_viewport(self.canvas)
        toolbar = NavigationToolbar(self.canvas, self.window)
        self.builder.get_object("toolbar_box").pack_start(toolbar, False, False, 0)
        self.textbuff = self.builder.get_object("algorithm_log")
        print str(self.textbuff)
        glib.io_add_watch(sys.stdout, glib.IO_IN, self.update_textfield)
        self.window.show_all()

#        self.window = self.wTree.get_widget("main_window")
#        if self.window:
#            self.window.connect("destroy", gtk.main_quit)

if __name__ == "__main__":

    current_network = ViewableNetworkFlow()
    app = DinicGTK()
    Gtk.main()

