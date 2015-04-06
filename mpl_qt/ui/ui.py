from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import numpy as np

from PySide import QtGui
from PySide import QtCore

import mpl_qt.ui.main as main
import mpl_qt.ui.plot as plot


class QuiverModel(object):

    def __init__(self, pxy, vxy):
        self.xy = pxy
        self.xydev = vxy


class MainWindow(QtGui.QMainWindow, main.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        gx, gy = np.meshgrid(np.linspace(-5, 5, 5), np.linspace(-5, 5, 5))
        pxy = np.array([gx.flatten(), gy.flatten()]).T
        phi = 0.5 * np.pi
        m = np.array([[np.cos(phi), np.sin(phi)],
                      [-np.sin(phi), np.cos(phi)]])
        pxy2 = np.dot(pxy, m) * 5
        vxy = pxy - pxy2

        self.model = QuiverModel(pxy, vxy)
        self.scatter_plot = plot.QuiverPlotWidget(parent=self, model=self.model)
        self.setCentralWidget(self.scatter_plot)
