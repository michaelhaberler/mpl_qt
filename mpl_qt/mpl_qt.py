# https://github.com/eliben/code-for-blog/blob/master/2009/qt_mpl_bars.py

import sys
from PyQt4 import QtCore, QtGui, uic

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import main


class MyNavigationToolbar(NavigationToolbar):

    def __init__(self,canvas, parent):
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
        #NavigationToolbar2QTAgg.__init__(self, canvas, parent)
        super(MyNavigationToolbar, self).__init__(canvas, parent)


class MyWindowClass(QtGui.QMainWindow, main.Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.toggleButton.setCheckable(True)
        self.toggleButton.clicked.connect(self.toggleButton_clicked)

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mplFrame)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.mpl_toolbar = MyNavigationToolbar(self.canvas, self.mplFrame)

        self.verticalLayout = QtGui.QVBoxLayout(self.mplFrame)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.mpl_toolbar)

        self.on_draw()

    def on_draw(self):
        """ Redraws the figure
        """
        self.data = [23, 34, 84, 75, 23, 12]
        x = range(len(self.data))

        self.axes.clear()
        self.axes.grid()
        self.axes.bar(
            left=x,
            height=self.data,
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

    def toggleButton_clicked(self, checked):
        print("clicked = ", checked)

    def pushButton_clicked(self):
        print("clicked!")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
