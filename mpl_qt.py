# https://github.com/eliben/code-for-blog/blob/master/2009/qt_mpl_bars.py

import sys
from PyQt4 import QtCore, QtGui, uic

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import main


class MyWindowClass(QtGui.QMainWindow, main.Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.toggleButton.setCheckable(True)
        self.toggleButton.clicked.connect(self.toggleButton_clicked)

        dpi = 100
        #self.fig = Figure((5.0, 4.0), dpi=dpi)
        self.fig = Figure((10.0, 10.0))
        self.canvas = FigureCanvas(self.fig)

        self.canvas.setParent(self.mplFrame)
        self.axes = self.fig.add_subplot(111)

        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.mplFrame)

        self.textbox = QtGui.QLineEdit()
        self.textbox.setMinimumWidth(200)
        self.connect(self.textbox, QtCore.SIGNAL('editingFinished()'), self.on_draw)

        self.draw_button = QtGui.QPushButton("&Draw")
        self.connect(self.draw_button, QtCore.SIGNAL('clicked()'), self.on_draw)

        self.grid_cb = QtGui.QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.connect(self.grid_cb, QtCore.SIGNAL('stateChanged(int)'), self.on_draw)
        self.on_draw()


    def on_draw(self):
        """ Redraws the figure
        """
        self.data = [23, 34, 84, 75, 23, 12]

        x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()
        self.axes.grid(self.grid_cb.isChecked())

        self.axes.bar(
            left=x,
            height=self.data,
            width=0.3,
            align='center',
            alpha=0.44,
            picker=5)

        self.canvas.draw()

    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        #
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points

        QtGui.QMessageBox.information(self, "Click!", msg)


    def toggleButton_clicked(self, checked):
        print("clicked = ", checked)

    def pushButton_clicked(self):
        print("clicked!")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
