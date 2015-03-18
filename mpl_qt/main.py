from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import sys
from PyQt4 import QtGui
from PyQt4 import Qt

import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
from matplotlib.figure import Figure

import mpl_qt.ui.main as uimain


class NavigationToolbar(NavigationToolbar2QTAgg):

    def __init__(self, canvas, parent):
        # (text, tooltip_text, image_file, name_of_method)
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            (None, None, None, None)
        )
        super(NavigationToolbar, self).__init__(canvas, parent)


class PlotWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.mpl_toolbar)

        self.on_draw()

    def on_draw(self):
        """ Redraws the figure
        """
        for ax in [self.ax1, self.ax2]:
            ax.clear()
            ax.grid(True)

        x = np.random.randint(low=-10, high=10, size=10)
        y = np.random.randint(low=-10, high=10, size=10)
        #self.ax1.scatter(x, y)
        self.ax1.quiver(x, y, x, y)
        self.ax1.set_aspect('equal')

        d = [23, 34, 84, 75, 23, 12]
        r = range(len(d))
        self.ax2.bar(
            left=r,
            height=d,
            width=0.3,
            align='center',
            alpha=0.44,
            picker=5)

        self.canvas.draw()

    def on_pick(self, event):
        """
        Parameters
        ----------
        event : matplotlib.backend_bases.PickEvent
        """
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        QtGui.QMessageBox.information(self, "Click!", msg)


class MainWindow(QtGui.QMainWindow, uimain.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.tabwidget = QtGui.QTabWidget(parent=self)
        self.plots = {
            'p1': PlotWidget(parent=self.tabwidget),
            'p2': PlotWidget(parent=self.tabwidget)
        }
        for tabname, tabplot in self.plots.iteritems():
            self.tabwidget.addTab(tabplot, tabname)

        self.horizontalLayout.insertWidget(0, self.tabwidget)

        data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}
        headers = []
        for i, (name, value_list) in enumerate(data.iteritems()):
            headers.append(name)
            for j, value in enumerate(value_list):
                item = QtGui.QTableWidgetItem(value)
                self.gridTableWidget.setItem(j, i, item)
                print(i, j, name, value)
        self.gridTableWidget.setHorizontalHeaderLabels(headers)
        self.gridTableWidget.resizeColumnsToContents()
        self.gridTableWidget.resizeRowsToContents()
