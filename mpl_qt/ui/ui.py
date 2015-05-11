from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import numpy as np

from PySide import QtGui
from PySide import QtCore

import matplotlib
matplotlib.use("Qt4Agg")
matplotlib.rcParams['backend.qt4'] = 'PySide'

import mpl_qt.ui.main as main
import mpl_qt.ui.plot as plot


class QuiverModel(object):

    def __init__(self, pxy, vxy):
        self.xy = pxy
        self.xyvalue = vxy


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, pxy, vxy, *args):
        if pxy.shape != vxy.shape:
            raise ValueError("pxy and vxy have to be of same shape")
        super(TableModel, self).__init__(parent, *args)
        self.model = np.concatenate([pxy, vxy], axis=1)
        self.header = ["x", "y", "xvalue", "yvalue"]

    def rowCount(self, parent):
        return len(self.model)

    def columnCount(self, parent):
        return len(self.model[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return str(self.model[index.row(), index.column()])

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

#    def sort(self, col, order):
#        """sort table by given column number col"""
#        self.emit(SIGNAL("layoutAboutToBeChanged()"))
#        self.mylist = sorted(self.mylist,
#                             key=operator.itemgetter(col))
#        if order == Qt.DescendingOrder:
#            self.mylist.reverse()
#        self.emit(SIGNAL("layoutChanged()"))


class MainWindow(QtGui.QMainWindow, main.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # define model
        gx, gy = np.meshgrid(np.linspace(-5, 5, 5), np.linspace(-5, 5, 5))
        pxy = np.array([gx.flatten(), gy.flatten()]).T
        phi = 0.5 * np.pi
        m = np.array([[np.cos(phi), np.sin(phi)],
                      [-np.sin(phi), np.cos(phi)]])
        #pxy2 = np.dot(pxy, m) * 5
        pxy2 = pxy + np.array([1, 0])
        vxy = pxy - pxy2

        # set up views and signals and slots
        self.model = QuiverModel(pxy, vxy)
        self.quiver_plot = plot.QuiverPlotWidget(parent=self, model=self.model)
        self.scaleEdit.setText(str(self.quiver_plot.scale))
        self.scaleEdit.editingFinished.connect(self.on_edit_scale)
        self.keylengthEdit.setText(str(self.quiver_plot.key_length))
        self.keylengthEdit.editingFinished.connect(self.on_edit_key_length)
        self.tabWidget.addTab(self.quiver_plot, "plot")

        self.table_view = QtGui.QTableView()
        self.tmodel = TableModel(self, pxy, vxy)
        self.table_view.setModel(self.tmodel)
        self.tabWidget.addTab(self.table_view, "data")

    def on_edit_key_length(self):
        self.quiver_plot.key_length = float(self.keylengthEdit.text())

    def on_edit_scale(self):
        self.quiver_plot.scale = float(self.scaleEdit.text())
