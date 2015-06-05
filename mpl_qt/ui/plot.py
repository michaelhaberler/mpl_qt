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
import matplotlib as mpl

import mpl_qt.grid as grid


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
        #self.canvas.setParent(self)
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
        Has attributes xy, xyvalue (arrays of shape = (n, 2)) and unit (str).
    """


    def __init__(self, parent=None, model=None):
        self.model = model
        key_sample = self.model.xyvalue[(self.model.xyvalue[:, 0] != 0) |
                                        (self.model.xyvalue[:, 1] != 0)]
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
        xyvalue = self.model.xyvalue
        qax = self.ax.quiver(xy[:, 0], xy[:, 1],
                             xyvalue[:, 0], xyvalue[:, 1],
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


class MeshplotWidget(PlotWidget):

    def __init__(self, parent=None, model=None):
        self.model = model
        self._scale = 1.0
        self._unit = ""
        super(MeshplotWidget, self).__init__(parent)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
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
        xyvalue = self.model.xyvalue

        # sort ascending 1) x 2) y
        i_srt = np.lexsort((xy[:, 0], xy[:, 1]))
        xy = xy[i_srt]
        xy2 = (xy + xyvalue * self.scale)[i_srt]

        # reshape data to extract grid tile corner arrays
        x0, x1, dx, nx = grid.grid_size(xy[:, 0])
        y0, y1, dy, ny = grid.grid_size(xy[:, 1])
        x = xy[:, 0].reshape(nx, ny)
        y = xy[:, 1].reshape(nx, ny)
        x2 = xy2[:, 0].reshape(nx, ny)
        y2 = xy2[:, 1].reshape(nx, ny)

        # exctract vertices and their path codes for grid tiles
        verts, codes = self._mesh_verts_codes(x, y)
        vertspath = mpl.path.Path(verts, codes)
        patch = mpl.patches.PathPatch(vertspath,
                                      facecolor='none',
                                      edgecolor='black',
                                      alpha=0.5)
        self.ax.add_patch(patch)

        verts2, codes2 = self._mesh_verts_codes(x2, y2)
        vertspath2 = mpl.path.Path(verts2, codes2)
        patch2 = mpl.patches.PathPatch(vertspath2,
                                      facecolor='none',
                                      edgecolor='red',
                                      alpha=0.5)
        self.ax.add_patch(patch2)

        # plot grid tile corner points
        #self.ax.plot(xy[:, 0], xy[:, 1], 'ko')
        #self.ax.plot(xy2[:, 0], xy2[:, 1], 'ro')

        # setup plot
        self.ax.set_xlim(min(x.min(), x2.min()),
                         max(x.max(), x2.max()))
        self.ax.set_ylim(min(y.min(), y2.min()),
                         max(y.max(), y2.max()))
        self.ax.set_xlabel(self.unit)
        self.ax.set_ylabel(self.unit)

        self.canvas.draw()

    def _mesh_verts_codes(self, x, y):
        """Calculate mesh vertices and their path codes from grid positions.

        Parameters
        ----------
        x, y : arrays with shape = (nx, ny)
            Grid positions.

        Returns
        -------
        verts : array with shape = (nx*ny*(1+3+1), 2)
            Vertex positions for mesh path codes.
        codes : array with shape = (nx*ny*(1+3+1),)
            Mesh path codes (1x mpl.path.Path.MOVETO, 3x mpl.path.Path.LINETO,
            1x mpl.path.Path.CLOSEPOLY)
        """
        lowerleftx = x[:-1, :-1].flatten()
        lowerrightx = x[:-1, 1:].flatten()
        lowerlefty = y[:-1, :-1].flatten()
        lowerrighty = y[:-1, 1:].flatten()
        #lowerlefty, lowerrighty
        upperleftx = x[1:, :-1].flatten()
        upperrightx = x[1:, 1:].flatten()
        upperlefty = y[1:, :-1].flatten()
        upperrighty = y[1:, 1:].flatten()

        nrects = (x.shape[0]-1) * (x.shape[1]-1)
        nverts = nrects * (1+3+1)
        verts = np.zeros((nverts, 2))

        codes = np.ones(nverts, int) * mpl.path.Path.LINETO
        codes[0::5] = mpl.path.Path.MOVETO
        codes[4::5] = mpl.path.Path.CLOSEPOLY

        verts[0::5,0] = lowerleftx
        verts[0::5,1] = lowerlefty
        verts[1::5,0] = upperleftx
        verts[1::5,1] = upperlefty
        verts[2::5,0] = upperrightx
        verts[2::5,1] = upperrighty
        verts[3::5,0] = lowerrightx
        verts[3::5,1] = lowerrighty

        return verts, codes

