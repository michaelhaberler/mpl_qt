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
        Has attributes xy and xydev (arrays of shape = (n, 2)).
    """


    def __init__(self, parent=None, model=None):
        self.model = model
        super(QuiverPlotWidget, self).__init__(parent)

    def on_draw(self):
        """
        .. todo::
            Rescale key on changing the widget size.
        """
        self.ax.clear()

        xy = self.model.xy
        xydev = self.model.xydev
        qax = self.ax.quiver(xy[:, 0], xy[:, 1],
                             xydev[:, 0], xydev[:, 1], picker=True)

        key_sample = xydev[(xydev[:, 0] != 0) |
                           (xydev[:, 1] != 0)]
        key_length = np.sqrt(np.mean(np.sum(key_sample**2, axis=1)))
        unit = 'm'
        label = unit
        self.ax.set_xlabel(label)
        self.ax.set_ylabel(label)
        self.ax.quiverkey(qax, 0.95, 0.95, U=key_length, coordinates="axes",
                          label="{:2.3e} {}".format(key_length, unit),
                          linewidths=(1,), edgecolors=('k'), color="r",
                          labelpos="S")

        self.canvas.draw()
