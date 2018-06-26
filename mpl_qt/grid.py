"""Handle regular grids.

.. _definition_of_grid:

Definition of Grid
------------------

A grid is a sequence of evenly spaced points.
It is parameterized (overspecified) by a tuple containing the start value,
``start``, the end value ``end``, the size of spacing between two consecutive
points ``step``, and the total number of points ``num``.

.. code::

    (start, end, step, num)

========= ================
``var``   x
========= ================
``start`` :math:`x_0`
``end``   :math:`x_1`
``step``  :math:`\Delta x`
``num``   :math:`n+1`
========= ================

.. math::

    x_1 = x_0 + (n+1) \cdot \Delta x

or by an array of grid points

.. code::

    [x1, x2, x3, ..., xn]
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy as np
import quantities as pq


def grid_size(x, tolerance=0.001):
    """Calculate/Estimate grid parameters for array x: grid start, grid end, grid width,
    number of grid points.

    Use heuristic to account for missing or non-grid conforming values in x
    (tolerance).

    Parameters
    ----------
    tolerance : float
        Relative tolerance for step width.

    Returns
    -------
    (float, float, float, int) :
        (start, end, step, num) (see :ref:`definition_of_grid`)
    """
    if x.max() == x.min():
        return x.max(), x.max(), 0, 1
    dx = np.diff(np.sort(np.unique(x)))
    tolerance = tolerance * np.abs(x.max() - x.min()) / dx.shape[0]

    dx = dx[dx > tolerance]
    udx = np.unique(dx)
    if udx.shape == (1,):
        dx = udx[0]
    else:
        dx = np.median(dx)

    nx = np.round((x.max() - x.min()) / dx + 1).astype(np.int)
    x0 = x.min()
    x1 = x.max() #x0 + nx*dx
    return x0, x1, dx, nx

