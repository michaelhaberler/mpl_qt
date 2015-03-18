"""
http://stackoverflow.com/questions/1736015/debugging-a-pyqt4-app
"""

def debug_trace():
  '''Set a tracepoint in the Python debugger that works with Qt'''
  from PyQt4.QtCore import pyqtRemoveInputHook
  from ipdb import set_trace
  pyqtRemoveInputHook()
  set_trace()

__version__ = "0.1"
