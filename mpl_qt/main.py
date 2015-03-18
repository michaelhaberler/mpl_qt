from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import sys
from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore

import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
from matplotlib.figure import Figure

import mpl_qt.ui.main as uimain
import mpl_qt.ui.inputdata as uiinput


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


class InputDataWindow(QtGui.QMainWindow, uiinput.Ui_MainWindow):
    """
    .. todo::
        QWidget or QMainWindow?
    """

    def __init__(self, parent=None):
        super(InputDataWindow, self).__init__(parent)
        self.setupUi(self)

        # plot tabs for grids
        self.tabwidget = QtGui.QTabWidget(parent=self)
        self.plots = {
            'p1': PlotWidget(parent=self.tabwidget),
            'p2': PlotWidget(parent=self.tabwidget)
        }
        for tabname, tabplot in self.plots.iteritems():
            self.tabwidget.addTab(tabplot, tabname)
        self.horizontalLayout.insertWidget(0, self.tabwidget)


class InputFile(object):

    def __init__(self, filename, multiplier, window_parent=None):
        self.filename = filename
        self.multiplier = multiplier
        self.window = InputDataWindow(parent=window_parent)


class MainWindow(QtGui.QMainWindow, uimain.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.actionOpen.triggered.connect(self.open)

        # containers for file data
        self.input_files = []

        # plot tabs for grids
        self.tabwidget = QtGui.QTabWidget(parent=self)
        self.plots = {
            'p1': PlotWidget(parent=self.tabwidget),
            'p2': PlotWidget(parent=self.tabwidget)
        }
        for tabname, tabplot in self.plots.iteritems():
            self.tabwidget.addTab(tabplot, tabname)
        self.horizontalLayout.insertWidget(0, self.tabwidget)

        # table for grids
        headers = ['Multiplier', 'Filename']
        self.gridTableWidget.setColumnCount(2)
        self.gridTableWidget.setHorizontalHeaderLabels(headers)
        self.gridTableWidget.setSelectionBehavior(
            Qt.QAbstractItemView.SelectRows)
        self.gridTableWidget.itemDoubleClicked.connect(self.table_item_clicked)

        self.update_ui()

    def update_ui(self):

        self.gridTableWidget.setRowCount(len(self.input_files))
        for i, input_data in enumerate(self.input_files):
            item = QtGui.QTableWidgetItem(str(input_data.multiplier))
            self.gridTableWidget.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(input_data.filename)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.gridTableWidget.setItem(i, 1, item)
            print(i, input_data.filename)

        #self.gridTableWidget.setVerticalHeaderLabels(self.data.keys())
        self.gridTableWidget.resizeColumnsToContents()
        self.gridTableWidget.resizeRowsToContents()

    @QtCore.pyqtSlot()
    def open(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, 'Open File', '.')
            #self, 'Open File', '.', '(*.bin)')

        if filename:
            self.input_files.append(InputFile(filename, +1.0, self))
            self.input_files[-1].window.show()
            self.update_ui()

    @QtCore.pyqtSlot(Qt.QTableWidgetItem)
    def table_item_clicked(self, item):
        selected_text = item.text()
        try:
            input_file = next(item for item in self.input_files
                              if item.filename == selected_text)
        except StopIteration as e:
            print("Couldn't find selected item \"{}\".".format(selected_text))
            return

        if input_file.window.isHidden():
            input_file.window.show()
        else:
            print(input_file, " is already visible")
