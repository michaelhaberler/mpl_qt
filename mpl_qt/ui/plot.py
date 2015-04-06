from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import sys
import numpy as np

from PySide import QtGui
from PySide import QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.figure import Figure


class PlotWidget(QtGui.QWidget):
    """Base class for plot widgets.
    """

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.mpl_toolbar = NavigationToolbar2QT(self.canvas, self)

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.mpl_toolbar)

        self.on_draw()

    def on_draw(self):
        """(Re-)draw the figure.
        """
        self.ax.clear()
        self.canvas.draw()

    def on_pick(self, event):
        """
        Parameters
        ----------
        event : matplotlib.backend_bases.PickEvent
        """
        msg = "You've clicked :\n {}".format(event)
        QtGui.QMessageBox.information(self, "Click!", msg)


class ScatterPlotWidget(PlotWidget):
    """
    Attributes
    ----------
    model :
        Has attribute xy (array of shape = (n, 2)).
    """

    def __init__(self, parent=None, model=None):
        self.model = model
        super(ScatterPlotWidget, self).__init__(parent)

    def on_draw(self):
        self.ax.clear()

        xy = self.model.xy
        self.ax.scatter(xy[:, 0], xy[:, 1], picker=True)

        self.canvas.draw()

    def on_pick(self, event):
        """
        Parameters
        ----------
        event : matplotlib.backend_bases.PickEvent
        """
        i = event.ind
        xy = self.model.xy
        msg = "You've clicked on coords:\n {}".format(xy[i])
        QtGui.QMessageBox.information(self, "Click!", msg)


class QuiverPlotWidget(PlotWidget):
    """
    Attributes
    ----------
    model :
        Has attributes xy, xydev (arrays of shape = (n, 2)) and unit (str).
    """


    def __init__(self, parent=None, model=None):
        self.model = model
        key_sample = self.model.xydev[(self.model.xydev[:, 0] != 0) |
                                      (self.model.xydev[:, 1] != 0)]
        self._key_length = np.sqrt(np.mean(np.sum(key_sample**2, axis=1)))
        self._scale = 1.0
        self._unit = ""
        super(QuiverPlotWidget, self).__init__(parent)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self.on_draw()

    @property
    def key_length(self):
        return self._key_length

    @key_length.setter
    def key_length(self, length):
        self._key_length = length
        self.on_draw()

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit
        self.on_draw()

    def on_draw(self):
        self.ax.clear()

        xy = self.model.xy
        xydev = self.model.xydev
        qax = self.ax.quiver(xy[:, 0], xy[:, 1],
                             xydev[:, 0], xydev[:, 1],
                             units="xy",
                             scale=self.scale,
                             picker=True)

        self.ax.quiverkey(qax, 1.05, 1.05,
                          U=self.key_length,
                          coordinates="axes",
                          label="{:2.3e} {}".format(self.key_length, self.unit),
                          linewidths=(1,),
                          edgecolors=('k'),
                          color="r",
                          labelpos="S")

        self.ax.set_xlabel(self.unit)
        self.ax.set_ylabel(self.unit)

        self.canvas.draw()
