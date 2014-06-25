# -*- coding: utf-8 -*-
from gi.repository import Gtk
import dinic
import networkx as nx
from matplotlib import use as mpluse
mpluse('GTK3Agg')
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
import matplotlib.pyplot as plt
import thread
from gi.repository import Gdk
f = plt.figure()

class ConsoleLikeTextBuffer:
    def __init__(self):
        self.textbuff = Gtk.TextBuffer()
        self.end_iter = self.textbuff.get_end_iter()
    def get_text_buffer(self):
        return self.textbuff
    def append_line(self, message):
        self.textbuff.insert(self.end_iter, message + "\n")


class ViewableNetworkFlow(dinic.NetworkFlow):
    layout = {}
    dilayout = {}
    def __init__(self):
        super(ViewableNetworkFlow, self).__init__()
        self.console = ConsoleLikeTextBuffer()
    def print_message(self, message):
        self.console.append_line(message)

    def show(self, reset_layout):
        if not self.zorientowany:
            plt.hold(False)
            plt.tight_layout()
            g = nx.Graph()
            etykiety = {}
            for u in range(0, self.wierzcholki):
                g.add_nodes_from(range(self.wierzcholki))
            for u in range(0,self.wierzcholki):
                for v in self.za[u]:
                    if self.przeplyw == None:
                        etykiety[(u, v)] = str(self.c[u,v])
                    else:
                        etykiety[(u, v)] = str(self.przeplyw[u,v]) + "/" + str(self.przeplyw[v,u]) + "/" + str(self.c[u,v])
                    g.add_edge(u, v)
    #        print str(etykiety)
            if (reset_layout==True or not(self.layout)):
                self.layout = nx.spring_layout(g)
            nx.draw(g, pos=self.layout)
            nx.draw_networkx_edge_labels(g, pos=self.layout, edge_labels=etykiety)
            f.canvas.draw()
        else:
            self.show_directed(reset_layout)
    def show_directed(self, reset_layout):
        format_etykiety = lambda u,v: str(self.przeplyw[u,v]) + "/" + str(self.c[u,v]) if not self.przeplyw == None else "0.0/"+str(self.c[u,v])
        plt.hold(False)
        plt.tight_layout()
        g = nx.DiGraph()
        etykiety = {}
        for u in range(0, self.wierzcholki):
            g.add_nodes_from(range(self.wierzcholki))
        for u in range(0,self.wierzcholki):
            for v in self.za[u]:
                if ( self.c[u,v]>0 if self.przeplyw==None else  self.przeplyw[u, v] > 0):
                    etykiety[(u,v)] = format_etykiety(u,v)
                    g.add_edge(u,v)
                elif ( self.c[v,u]>0  if self.przeplyw==None else self.przeplyw[v, u] > 0):
                    etykiety[(v,u)] = format_etykiety(v,u)
                    g.add_edge(v,u)
        if (reset_layout==True or not (self.dilayout)):
            self.dilayout = nx.spring_layout(g)
        nx.draw(g, pos=self.dilayout)
        nx.draw_networkx_edge_labels(g, pos=self.dilayout, edge_labels=etykiety)
        f.canvas.draw()    


class GraphTesting:
    def stat_show(self, t, s1, s2, title1, title2, titlex):
        f.clf()
        ax = f.add_subplot(2, 1, 1)
        ax.set_title(title1)
        ax.set_xlabel(titlex)
        ax.plot(t, s1)
        ax= f.add_subplot(2,1,2)
        ax.set_title(title2)
        ax.set_xlabel(titlex)
        ax.plot(t, s2)
        f.canvas.draw()

    def const_v(self, n, maks_cap, tries, orient):
        max_e = int(n*(n-1)/2)
        results = max_e * [0.0]
        results_by_t = int(n*(n-1)/2) * [0.0]
        t = [float(x) for x in range(0,int(n*(n-1)/2))]
        progress_bar = app.builder.get_object("test_progress")
        progress_bar.set_pulse_step(1.0/max_e)
        progress_bar.set_fraction(0.0)
        for j in range(3, int(n*(n-1)/2)):
            calc_time = current_network.randomizowana_proba_dinica(n, j, tries, maks_cap, orient)
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
    def const_e(self, n, maks_cap, tries, orient):
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
            calc_time = current_network.randomizowana_proba_dinica(j, n, tries, maks_cap, orient)
            t.append(float(j))
            if j==min_v:
                first_y = calc_time
                results.append(calc_time)
            else:
                results.append(calc_time/first_y)
            results_by_t2.append(calc_time/(j))
            progress_bar.pulse()
            while Gtk.events_pending():
                Gtk.main_iteration()
        self.stat_show(t, results, results_by_t2, r'$T(|V|)$ przy $|E|=$const', r'$T(|V|)/|V|$', r'$|V|$')



    def few_edges(self, n, maks_cap, tries, orient):
        progress_bar = app.builder.get_object("test_progress")
        progress_bar.set_pulse_step(1.0/n)
        progress_bar.set_fraction(0.0)
        t = [float(x) for x in range(0, n)]
        results = [0.0 for x in range(0, n)]
        results_by_t2 = [0.0 for x in range(0, n)]
        for j in range(3, n):
            calc_time = current_network.randomizowana_proba_dinica(j, j, tries, maks_cap, orient)
            results[j] = calc_time
            if j>3:
                results[j] = results[j]/results[3]
            results_by_t2[j] = results[j]/(j)
            progress_bar.pulse()
            while Gtk.events_pending():
                Gtk.main_iteration()
        self.stat_show(t, results, results_by_t2, r'$T(|V|)$ przy $|E| = O(|V|)$', r'$T(|V|)/|V|$', r'$|V|$')

    def many_edges(self, n, maks_cap, tries, orient):
        progress_bar = app.builder.get_object("test_progress")
        progress_bar.set_pulse_step(1.0/n)
        progress_bar.set_fraction(0.0)
        t = [float(x) for x in range(0, n)]
        results = [0.0 for x in range(0, n)]
        results_by_t3 = [0.0 for x in range(0, n)]
        for j in range(3, n):
            calc_time = current_network.randomizowana_proba_dinica(j, j*j/2, tries, maks_cap, orient)
            results[j] = calc_time
            if j>3:
                results[j] = results[j]/results[3]
            results_by_t3[j] = results[j]/(j*j)
            progress_bar.pulse()
            while Gtk.events_pending():
                Gtk.main_iteration()
        self.stat_show(t, results, results_by_t3, r'$T(|V|)$ przy $|E| = \Omega(|V|^2)$', r'$T(|V|)/|V|^2$', r'$|V|$')


class UIHandler:
    def onDeleteWindow(self, *args):
        box = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION, flags = Gtk.DialogFlags.MODAL, buttons = Gtk.ButtonsType.YES_NO,
                                message_format = u"Czy na pewno chcesz zakończyć pracę programu?", )
        response = box.run()
        box.hide()
        if response == Gtk.ResponseType.YES:
            Gtk.main_quit(*args)

    def onQuit(self, menubar):
        box = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION, flags = Gtk.DialogFlags.MODAL, buttons = Gtk.ButtonsType.YES_NO,
                                message_format = u"Czy na pewno chcesz zakończyć pracę programu?", )
        response = box.run()
        box.hide()
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
        oriented = app.builder.get_object("orientedcheckbox").get_active()
        #print str(v)+' '+str(e)
        choice_dialog.hide()
        if response == 1:
            current_network.wylosuj(v, e, max_cap, oriented)

    def onnextStepClicked(self, widget):
        current_network.do_next_step = True
        current_network.show_directed(False)

    def onTestButtonClicked(self, button):
        mode_dialog = app.builder.get_object("testing_dialog")
        response = mode_dialog.run()
        mode_dialog.hide()
        testtype_choice = app.builder.get_object("test_type").get_active()
        if testtype_choice in {0, 2, 3}:
            v = int(app.builder.get_object("test_vertices").get_text())
        if testtype_choice==1:
            e = int(app.builder.get_object("test_edges").get_text())
        tries = int(app.builder.get_object("no_tries").get_text())
        max_cap = int(app.builder.get_object("max_test_cap").get_text())
        orienttest = app.builder.get_object("orienttestcheckbox").get_active()
        if response == 1:
            mode_dialog.show()
            which_one = { 0: lambda: GraphTesting().const_v(v, max_cap, tries, orienttest),
                            1: lambda:GraphTesting().const_e(e, max_cap, tries, orienttest),
                            2: lambda:GraphTesting().few_edges(v, max_cap, tries, orienttest),
                            3: lambda:GraphTesting().many_edges(v, max_cap, tries, orienttest)}
            which_one[testtype_choice]()
            mode_dialog.hide()
    def onToggleStepByStep(self, checkbox, data=None):
        if checkbox.get_active():
            current_network.step_by_step = True
        else:
            current_network.step_by_step = False


    def onMaxFlowButton(self, button):
        try:
            source = int(app.builder.get_object("source_entry").get_text())
            target = int(app.builder.get_object("target_entry").get_text())
            print str((source, target))
            if source >= current_network.wierzcholki or target >= current_network.wierzcholki or source==target:
                raise ValueError
        except ValueError:
            box = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING, buttons = Gtk.ButtonsType.OK,
                                    message_format = u"Nieprawidłowe wartości pól źródło/ujście.")
            box.run()
            box.destroy()
        else:
            thread.start_new_thread(current_network.maxflow, (source, target))




class DinicGTK:
    def __init__(self):
        self.gladefile = "sieci_gui.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(UIHandler())
        self.window = self.builder.get_object("main_window")
        self.window.connect("delete-event", UIHandler().onDeleteWindow)
        xmax = Gdk.Screen.get_default().get_width()
        ymax = Gdk.Screen.get_default().get_height()
        self.canvas = FigureCanvas(f)
        self.builder.get_object("graphscreen").add_with_viewport(self.canvas)
        self.builder.get_object("logscroll").set_size_request(int(0.3*xmax), int(0.65*ymax))
        self.builder.get_object("graphscreen").set_size_request(int(0.4*xmax), int(0.69*ymax))
        f.canvas.resize(int(0.35*xmax), int(0.68*ymax))
        toolbar = NavigationToolbar(self.canvas, self.window)
        self.builder.get_object("toolbar_box").pack_start(toolbar, False, False, 0)
        textview = self.builder.get_object("algorithm_log")
        textview.set_buffer(current_network.console.get_text_buffer())

        self.window.show_all()
#        self.window = self.wTree.get_widget("main_window")
#        if self.window:
#            self.window.connect("destroy", gtk.main_quit)

if __name__ == "__main__":

    current_network = ViewableNetworkFlow()
    app = DinicGTK()
    Gtk.main()

